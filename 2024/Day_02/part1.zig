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

fn isSafe(line: anytype) u32 {
    var it = std.mem.split(u8, line, " ");
    var last: i32 = -1;
    var initialSign: i32 = 0;
    while (it.next()) |i| {
        const num = std.fmt.parseInt(i32, i, 10) catch 0;
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
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    // const allocator = gpa.allocator();
    const file = try std.fs.cwd().openFile("input.txt", .{});
    defer file.close();
    const reader = file.reader();
    var buffer: [1024]u8 = undefined;
    var safe: u32 = 0;
    while (try nextLine(reader, &buffer) orelse null) |line| {
        const t = isSafe(line);
        safe += t;
        std.debug.print("Safe {d} {s}\n", .{ t, line });
    }
    std.debug.print("Safe: {d}\n", .{safe});
}
