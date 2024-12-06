const std = @import("std");

fn nextLine(reader: anytype, buffer: []u8) !?[]u8 {
    const line = (try reader.readUntilDelimiterOrEof(buffer, '\n')) orelse return null;
    return line;
}

fn clamp(i: i32) i32 {
    return if (i < 0) -1 else 1;
}

fn didSwitch(i: i32, d: i32) bool {
    return if (i == 0) false else clamp(i) != clamp(d);
}

fn dampen(line: anytype) u32 {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();
    var list = std.ArrayList(i32).init(allocator);
    defer list.deinit();
    var it = std.mem.split(u8, line, " ");
    while (it.next()) |i| {
        const x = std.fmt.parseInt(i32, i, 10) catch 0;
        _ = list.append(x) catch 0;
    }

    if (isSafe(list) == 1) {
        return 1;
    }

    for (list.items, 0..) |_, n| {
        var innerList = std.ArrayList(i32).init(allocator);
        defer innerList.deinit();
        for (list.items, 0..) |i, j| {
            if (j != n) {
                _ = innerList.append(i) catch {};
            }
        }
        if (isSafe(innerList) == 1) {
            return 1;
        }
    }
    return 0;
}

fn isSafe(list: anytype) u32 {
    var last: i32 = -1;
    var initialSign: i32 = 0;
    for (list.items) |num| {
        if (last != -1) {
            const d = last - num;
            if (d == 0 or @abs(d) > 3 or didSwitch(initialSign, d)) {
                std.debug.print("Delta: {d} IS: {d} Switched {any}\n", .{ d, initialSign, didSwitch(initialSign, d) });
                return 0;
            }
            initialSign = clamp(d);
        }
        last = num;
    }
    return 1;
}

pub fn main() anyerror!void {
    const file = try std.fs.cwd().openFile("input.txt", .{});
    defer file.close();
    const reader = file.reader();
    var buffer: [1024]u8 = undefined;
    var safe: u32 = 0;
    while (try nextLine(reader, &buffer) orelse null) |line| {
        const t = dampen(line);
        safe += t;
        std.debug.print("Safe {d} {s}\n", .{ t, line });
    }
    std.debug.print("Safe: {d}\n", .{safe});
}
