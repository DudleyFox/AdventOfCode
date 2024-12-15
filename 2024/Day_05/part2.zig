const std = @import("std");
const input = @embedFile("input.txt");

const OrderingRule = struct { pg1: u16, pg2: u16 };
const UpdateList = struct { list: []u16 };

const ProblemData = struct { rules: []OrderingRule, updates: []UpdateList };

fn parseRule(rawRule: []const u8) OrderingRule {
    std.debug.print("{s}\n", .{rawRule});
    var index: u8 = 0;
    var tmp: [2]u16 = undefined;
    @memset(&tmp, 0);
    for (rawRule) |c| {
        switch (c) {
            '0'...'9' => tmp[index] = tmp[index] * 10 + (c - '0'),
            '|' => index += 1,
            else => {},
        }
    }

    return OrderingRule{ .pg1 = tmp[0], .pg2 = tmp[1] };
}

fn parseUpdateList(rawList: []const u8, allocator: anytype) !UpdateList {
    std.debug.print("Parsing update list: {s}\n", .{rawList});
    var items = std.mem.split(u8, rawList, ",");
    var list = std.ArrayList(u16).init(allocator);
    defer list.deinit();
    while (items.next()) |i| {
        const x = std.fmt.parseInt(u16, i, 10) catch 0;
        if (x > 0) {
            _ = list.append(x) catch 0;
        }
    }
    var result = try allocator.alloc(u16, list.items.len);
    for (list.items, 0..) |number, index| {
        result[index] = number;
    }
    return UpdateList{ .list = result };
}

fn readFile(allocator: anytype) !ProblemData {
    std.debug.print("readFile\n", .{});
    var lines = std.mem.split(u8, input, "\n");
    var countRules: bool = true;

    var rules = std.ArrayList([]const u8).init(allocator);
    defer rules.deinit();

    var updates = std.ArrayList([]const u8).init(allocator);
    defer updates.deinit();

    while (lines.next()) |line| {
        std.debug.print("{s}\n", .{line});
        if (line.len > 0) {
            if (countRules) {
                _ = rules.append(line) catch 0;
            } else {
                _ = updates.append(line) catch 0;
            }
        } else {
            countRules = false;
        }
    }

    var data = ProblemData{ .rules = try allocator.alloc(OrderingRule, rules.items.len), .updates = try allocator.alloc(UpdateList, updates.items.len) };

    for (rules.items, 0..) |raw, i| {
        data.rules[i] = parseRule(raw);
    }

    for (updates.items, 0..) |raw, i| {
        data.updates[i] = try parseUpdateList(raw, allocator);
    }

    return data;
}

fn in(pg: u16, pages: []u16) bool {
    for (pages) |page| {
        if (pg == page) return true;
    }
    return false;
}

fn followsRule(pages: []u16, rule: OrderingRule) bool {
    const before = rule.pg1;
    const after = rule.pg2;
    var beforeSeen = false;
    var valid = true;

    for (pages) |pg| {
        if (pg == before) {
            beforeSeen = true;
        }
        if (pg == after) {
            // if we have seen the before we are good, and this
            // will return true. Otherwise we have not seen it, and
            // this will return false;
            std.debug.print("\tFor rule {d}|{d}", .{ before, after });
            if (beforeSeen) {
                valid = valid and true;
                std.debug.print("\tValid\n\n", .{});
            } else {
                valid = false;
                std.debug.print("\tInvalid\n\n", .{});
            }
        }
    }
    return valid;
}

fn isUpdateListValid(list: UpdateList, rules: []OrderingRule) bool {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();
    var applicableRules = std.ArrayList(OrderingRule).init(allocator);
    defer applicableRules.deinit();
    for (rules) |rule| {
        if (in(rule.pg1, list.list) and in(rule.pg2, list.list)) {
            _ = applicableRules.append(rule) catch 0;
        }
    }

    for (applicableRules.items) |rule| {
        if (!followsRule(list.list, rule)) {
            // go ahead and fix it here, since we have the applicable rules
            std.mem.sort(u16, list.list, applicableRules.items, ascFromRules(u16));
            return false;
        }
    }
    return true;
}

fn printUpdateList(list: UpdateList) void {
    for (list.list) |i| {
        std.debug.print("{d},", .{i});
    }
    std.debug.print("\n", .{});
}

fn findInvalidUpdates(data: ProblemData, allocator: anytype) []UpdateList {
    var invalidUpdateLists = std.ArrayList(UpdateList).init(allocator);
    defer invalidUpdateLists.deinit();
    for (data.updates) |pages| {
        std.debug.print("Testing: ", .{});
        printUpdateList(pages);
        if (!isUpdateListValid(pages, data.rules)) {
            _ = invalidUpdateLists.append(pages) catch 0;
        }
    }

    std.debug.print("Invalid updates:\n", .{});
    for (invalidUpdateLists.items) |pages| {
        printUpdateList(pages);
    }
    std.debug.print("\n\n", .{});

    var fallback: [1]UpdateList = undefined;

    return invalidUpdateLists.toOwnedSlice() catch &fallback;
}

fn sumCenters(lists: []UpdateList) u32 {
    var sum: u32 = 0;
    for (lists) |list| {
        const length = list.list.len;
        const center = list.list[length / 2];
        sum += center;
        std.debug.print("{d} {d} {d} {d}\n", .{ center, sum, length, length / 2 });
    }
    return sum;
}

/// Use to generate a comparator function for a given type. e.g. `sort(u8, slice, {}, asc(u8))`.
pub fn asc(comptime T: type) fn (void, T, T) bool {
    return struct {
        pub fn inner(_: void, a: T, b: T) bool {
            return a < b;
        }
    }.inner;
}

fn ascFromRules(comptime T: type) fn ([]OrderingRule, T, T) bool {
    return struct {
        pub fn inner(rules: []OrderingRule, a: T, b: T) bool {
            for (rules) |rule| {
                if (a == rule.pg1 and b == rule.pg2) {
                    return true; // a is less than b (for sorting purposes)
                }
                if (a == rule.pg2 and b == rule.pg1) {
                    return false; // a is not less than b (for sorting purposes)
                }
            }
            return a < b;
        }
    }.inner;
}

pub fn main() anyerror!void {
    std.debug.print("Hello\n", .{});
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();
    const data = try readFile(allocator);
    defer {
        allocator.free(data.rules);
        for (data.updates) |update| {
            allocator.free(update.list);
        }
        allocator.free(data.updates);
    }

    for (data.rules) |r| {
        std.debug.print("{}|{}\n", .{ r.pg1, r.pg2 });
    }

    const lists = findInvalidUpdates(data, allocator);
    defer allocator.free(lists);

    std.debug.print("Center Sum {d}\n", .{sumCenters(lists)});
}
