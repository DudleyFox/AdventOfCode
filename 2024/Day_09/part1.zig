const std = @import("std");
const input = @embedFile("input.txt");

fn inRange(toTest: u8, min: u8, max: u8) bool {
    return (toTest >= min and toTest <= max);
}

fn buildExpandedMap(allocator: anytype) ![]i64 {
    var map = std.ArrayList(i64).init(allocator);
    defer map.deinit();
    var fileIndex: i64 = 0;
    var isFile = true;
    for (input) |c| {
        if (inRange(c, '0', '9')) {
            const x: u16 = c - '0';
            if (isFile) {
                for (0..x) |_| {
                    try map.append(fileIndex);
                }
                fileIndex += 1;
            } else {
                for (0..x) |_| {
                    try map.append(-1);
                }
            }
            isFile = !isFile;
        }
    }

    return try map.toOwnedSlice();
}

fn compressMap(map: []i64) void {
    var frontIndex: usize = 0;
    var backIndex: usize = map.len - 1;
    while (frontIndex < backIndex) {
        // std.debug.print("{d}\n", .{map});
        while (map[frontIndex] != -1) {
            frontIndex += 1;
        }
        while (map[backIndex] == -1) {
            backIndex -= 1;
        }
        if (map[frontIndex] == -1 and map[backIndex] != -1 and frontIndex < backIndex) {
            map[frontIndex] = map[backIndex];
            map[backIndex] = -1;
        }
    }
}

fn u2i(in: usize) i64 {
    return @as(i64, @intCast(in));
}

fn computeCheckSum(map: []i64) i64 {
    var sum: i64 = 0;
    for (map, 0..) |value, i| {
        // std.debug.print("{d} {d}\n", .{ i, value });
        if (value > 0) {
            const m = u2i(i) * value;
            // std.debug.print("{d} {d} {d}\n", .{ i, value, m });
            sum += m;
        }
    }
    return sum;
}

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();
    for (input) |c| {
        std.debug.print("{u}", .{c});
    }
    std.debug.print("\n", .{});
    const expMap = try buildExpandedMap(allocator);
    defer allocator.free(expMap);
    std.debug.print("{d}\n", .{expMap});
    compressMap(expMap);
    const checkSum = computeCheckSum(expMap);
    std.debug.print("{d}", .{checkSum});
}
