const std = @import("std");
const input = @embedFile("input.txt");

fn inRange(toTest: u8, min: u8, max: u8) bool {
    return (toTest >= min and toTest <= max);
}

fn printStones(stones: []u64) void {
    for (stones) |n| {
        std.debug.print("{d} ", .{n});
    }
    std.debug.print("\n", .{});
}

fn isEvenDigits(n: u64) bool {
    const exponent = (std.math.log(u64, 10, n) + 1);
    return exponent & 1 == 0;
}

fn splitInTwo(n: u64) [2]u64 {
    var numbers: [2]u64 = undefined;
    const exponent = (std.math.log(u64, 10, n) + 1);
    const pow = std.math.pow(u64, 10, exponent / 2);
    numbers[0] = n / pow;
    numbers[1] = n % pow;
    return numbers;
}

fn blink75Times(allocator: anytype) !void {
    var stones = std.ArrayList(u64).init(allocator);
    const clean = std.mem.trim(u8, input, " \n");
    var iter = std.mem.split(u8, clean, " ");
    while (iter.next()) |n| {
        if (n.len > 0) {
            const number = try std.fmt.parseInt(u64, n, 10);
            try stones.append(number);
        }
    }

    for (0..75) |i| {
        var newStones = std.ArrayList(u64).init(allocator);
        for (stones.items) |stone| {
            if (stone == 0) {
                try newStones.append(1);
            } else if (isEvenDigits(stone)) {
                const numbers = splitInTwo(stone);
                try newStones.append(numbers[0]);
                try newStones.append(numbers[1]);
            } else {
                try newStones.append(stone * 2024);
            }
        }
        stones.deinit();
        stones = newStones;
        //printStones(stones.items);
        std.debug.print("Blinked {d} times {d} stones\n", .{ i + 1, stones.items.len });
    }

    std.debug.print("After 25 blinks we have {d} stones\n", .{stones.items.len});
    stones.deinit();
}

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();
    for (input) |c| {
        std.debug.print("{u}", .{c});
    }
    std.debug.print("\n", .{});
    try blink75Times(allocator);
}
