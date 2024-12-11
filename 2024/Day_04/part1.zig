const std = @import("std");
const input = @embedFile("input.txt");
const Dimensions = struct { x: u32, y: u32 };
const dim = computeDimensions();
const xmasArray: [dim.x][dim.y]u8 = buildXmasArray();

fn buildXmasArray() [dim.x][dim.y]u8 {
    @setEvalBranchQuota(150 * 150);
    comptime var lines = std.mem.split(u8, input, "\n");
    var count: u32 = 0;
    var theArray: [dim.x][dim.y]u8 = undefined;
    while (lines.next()) |line| {
        if (line.len > 0) {
            for (line, 0..) |c, i| {
                theArray[count][i] = c;
            }
            count += 1;
        }
    }

    return theArray;
}

fn computeDimensions() Dimensions {
    @setEvalBranchQuota(150 * 150);
    var lines = std.mem.split(u8, input, "\n");
    var count: u32 = 0;
    var length: u32 = 0;
    while (lines.next()) |line| {
        if (line.len > 0) {
            length = line.len;
            count += 1;
        }
    }

    return Dimensions{ .x = count, .y = length };
}

fn safeDec(i: u32, s: u32) u32 {
    return if (i < s) 0 else i - s;
}

fn safeInc(i: u32, a: u32, max: u32) u32 {
    return if (i + a > max - 1) max - 1 else i + a;
}

fn safeAdd(i: u32, j: i32, max: u32) u32 {
    return if (j < 0) safeDec(i, @abs(j)) else safeInc(i, @abs(j), max);
}

fn canAdd(i: u32, j: i32, max: u32) bool {
    return if ((j < 0 and @abs(j) > i) or (j >= 0 and i + @abs(j) > max - 1)) false else true;
}

fn getPossibleXmas(testArray: [dim.x][dim.y]u8, x: u32, y: u32, xDelta: i32, yDelta: i32) [4]u8 {
    var result: [4]u8 = undefined;
    for (0..4) |c| {
        if (canAdd(x, xDelta * @as(i32, @intCast(c)), dim.x) and
            canAdd(y, yDelta * @as(i32, @intCast(c)), dim.y))
        {
            const localX = safeAdd(x, xDelta * @as(i32, @intCast(c)), dim.x);
            const localY = safeAdd(y, yDelta * @as(i32, @intCast(c)), dim.y);
            result[c] = testArray[localX][localY];
        } else {
            result[c] = 'Y';
        }
    }
    std.debug.print("{},{}:{},{}:{s}\n", .{ x, y, xDelta, yDelta, result });
    return result;
}

fn countAtPosition(testArray: [dim.x][dim.y]u8, x: u32, y: u32) u32 {
    // count all occurrences of the word XMAS in the input, it can be in any direction
    // so from one starting position we could find 8 i=occurrences
    //                      S  S  S
    //                       A A A
    //                        MMM
    //                      SAMXMAS
    //                        MMM
    //                       A A A
    //                      S  S  S
    var count: u32 = 0;
    if (testArray[x][y] != 'X') return 0;
    count += if (std.mem.eql(u8, &getPossibleXmas(testArray, x, y, 0, 1), "XMAS")) 1 else 0;
    count += if (std.mem.eql(u8, &getPossibleXmas(testArray, x, y, 0, -1), "XMAS")) 1 else 0;
    count += if (std.mem.eql(u8, &getPossibleXmas(testArray, x, y, 1, 0), "XMAS")) 1 else 0;
    count += if (std.mem.eql(u8, &getPossibleXmas(testArray, x, y, -1, 0), "XMAS")) 1 else 0;
    count += if (std.mem.eql(u8, &getPossibleXmas(testArray, x, y, 1, 1), "XMAS")) 1 else 0;
    count += if (std.mem.eql(u8, &getPossibleXmas(testArray, x, y, 1, -1), "XMAS")) 1 else 0;
    count += if (std.mem.eql(u8, &getPossibleXmas(testArray, x, y, -1, 1), "XMAS")) 1 else 0;
    count += if (std.mem.eql(u8, &getPossibleXmas(testArray, x, y, -1, -1), "XMAS")) 1 else 0;
    return count;
}

pub fn main() anyerror!void {
    var total: u32 = 0;
    for (xmasArray, 0..) |row, i| {
        for (row, 0..) |_, j| {
            total += countAtPosition(xmasArray, @intCast(i), @intCast(j));
        }
    }
    std.debug.print("Found XMAS {d} times!\n", .{total});
}
