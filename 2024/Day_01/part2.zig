const std = @import("std");

const TwoLists = struct { list1: std.ArrayList(u32), list2: std.ArrayList(u32) };

fn nextLine(reader: anytype, buffer: []u8) !?[]u8 {
    const line = (try reader.readUntilDelimiterOrEof(buffer, '\n')) orelse return null;
    return line;
}

fn buildLists(reader: anytype, allocator: anytype) anyerror!TwoLists {
    var lists = TwoLists{
        .list1 = std.ArrayList(u32).init(allocator),
        .list2 = std.ArrayList(u32).init(allocator),
    };
    var buffer: [1024]u8 = undefined;

    while (try nextLine(reader, &buffer) orelse null) |line| {
        std.debug.print("{s}\n", .{line});
        var it = std.mem.split(u8, line, "   ");
        var count: u8 = 0;

        while (it.next()) |x| {
            if (count == 0) {
                const i = try std.fmt.parseInt(u32, x, 10);
                _ = try lists.list1.append(i);
            } else {
                const i = try std.fmt.parseInt(u32, x, 10);
                _ = try lists.list2.append(i);
            }
            count = count + 1;
        }
    }

    return lists;
}

pub fn main() anyerror!void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();
    const file = try std.fs.cwd().openFile("input.txt", .{});
    const reader = file.reader();
    var lists = try buildLists(reader, allocator);
    defer {
        lists.list1.deinit();
        lists.list2.deinit();
    }
    const slice1 = try lists.list1.toOwnedSlice();
    const slice2 = try lists.list2.toOwnedSlice();
    defer {
        allocator.free(slice1);
        allocator.free(slice2);
    }
    std.mem.sort(u32, slice1, {}, comptime std.sort.asc(u32));
    std.mem.sort(u32, slice2, {}, comptime std.sort.asc(u32));
    var sum: u64 = 0;
    for (slice1) |i| {
        var count: u64 = 0;
        for (slice2) |j| {
            if (i == j) {
                count += 1;
            } else if (j > i) {
                break;
            }
        }
        std.debug.print("Sim:{d}\n", .{i * count});
        sum = sum + (i * count);
    }
    std.debug.print("Similarity: {d}\n", .{sum});
    defer file.close();
}
