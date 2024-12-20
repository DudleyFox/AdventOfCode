const std = @import("std");
const printTheMap = true;
const input = @embedFile("testinput.txt");
const Dimensions = struct { x: u32, y: u32 };
const dim = computeDimensions();
var antennaMap: [dim.x][dim.y]u8 = buildAntennaMap();
const Position = struct { x: isize, y: isize };
const FreqPos = struct { freq: u8, positions: []Position };
const Frequencies = struct { freqs: []FreqPos };

fn buildAntennaMap() [dim.x][dim.y]u8 {
    @setEvalBranchQuota(150 * 150);
    comptime var lines = std.mem.split(u8, input, "\n");
    var count: u32 = 0;
    var theArray: [dim.x][dim.y]u8 = undefined;
    while (lines.next()) |line| {
        if (line.len > 0) {
            for (line, 0..) |c, i| {
                theArray[i][count] = c;
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

fn computeUniqueFrequencies() u8 {
    var counts: [256]u8 = undefined;
    @memset(&counts, 0);

    for (0..dim.x) |x| {
        for (0..dim.y) |y| {
            const c = antennaMap[x][y];
            counts[c] = 1;
        }
    }

    var sum: u8 = 0;
    for (counts) |count| {
        sum += count;
    }

    sum = sum - 1; // don't count '.'

    return sum;
}

fn printMap(uF: u8) void {
    // clear screen move cursor to top left
    if (printTheMap) {
        std.debug.print("\x1B[2J\x1B[H", .{});
        for (0..dim.y) |y| {
            for (0..dim.x) |x| {
                std.debug.print("{u}", .{antennaMap[x][y]});
            }
            std.debug.print("\n", .{});
        }
    }
    std.debug.print("Unique Frequences {d}\n", .{uF});
}

// const Position = struct { x: isize, y: isize };
// const FreqPos = struct { freq: u8, positions: []Position};
// const Frequencies = struct { freqs: []FreqPos };
//

fn buildFrequencyPositions(uniqueFrequencies: u8, allocator: anytype) !Frequencies {
    var freqPosse: []FreqPos = try allocator.alloc(FreqPos, uniqueFrequencies);
    var index: usize = 0;
    for (dim.x) |x| {
        for (dim.y) |y| {}
    }
}

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();
    const uniqueFrequencies = computeUniqueFrequencies();
    printMap(uniqueFrequencies);
    const frequencies: Frequencies = try buildFrequencyPositions(uniqueFrequencies, allocator);
    defer {
        for (frequencies.freqs) |f| {
            allocator.free(f);
        }
        allocator.free(frequencies.freqs);
    }

    for (frequencies.freq) |f| {
        std.debug.print("{u}\n", .{f.freq});
    }
}
