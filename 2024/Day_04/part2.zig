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

fn isXmas(testArray: [dim.x][dim.y]u8, x: u32, y: u32) u32 {
    var r1: [2]u8 = undefined;
    var r2: [2]u8 = undefined;
    r1[0] = testArray[x - 1][y - 1];
    r1[1] = testArray[x + 1][y + 1];
    r2[0] = testArray[x - 1][y + 1];
    r2[1] = testArray[x + 1][y - 1];
    const r1Mas = (r1[0] == 'M' and r1[1] == 'S') or (r1[0] == 'S' and r1[1] == 'M');
    const r2Mas = (r2[0] == 'M' and r2[1] == 'S') or (r2[0] == 'S' and r2[1] == 'M');
    return if (r1Mas and r2Mas) 1 else 0;
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
    if (testArray[x][y] != 'A' or x == dim.x - 1 or y == dim.y - 1 or x == 0 or y == 0) return 0;
    return isXmas(testArray, x, y);
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
