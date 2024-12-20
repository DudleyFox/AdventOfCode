const std = @import("std");
const printTheMap = true;
const input = @embedFile("input.txt");
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
    var sum: u32 = 0;
    if (printTheMap) {
        // clear screen move cursor to top left
        // std.debug.print("\x1B[2J\x1B[H", .{});
        for (0..dim.y) |y| {
            for (0..dim.x) |x| {
                const c = antennaMap[x][y];
                sum += if (c != '.') 1 else 0;
                std.debug.print("{u}", .{c});
            }
            std.debug.print("\n", .{});
        }
    }
    std.debug.print("Unique Frequences: {d} Antinodes: {d}\n", .{ uF, sum });
}

fn u2i(in: usize) isize {
    return @as(isize, @intCast(in));
}

fn i2u(in: isize) usize {
    return @as(usize, @intCast(in));
}

fn buildFrequencyPositions(uniqueFrequencies: u8, allocator: anytype) !Frequencies {
    var freqPosse: []FreqPos = try allocator.alloc(FreqPos, uniqueFrequencies);
    const TmpS = struct { count: usize, positions: []Position };
    var map = std.AutoHashMap(u8, TmpS).init(allocator);
    defer {
        var iter = map.iterator();
        while (iter.next()) |entry| {
            allocator.free(entry.value_ptr.positions);
        }
        map.deinit();
    }
    for (0..dim.x) |x| {
        for (0..dim.y) |y| {
            const c = antennaMap[x][y];
            if (c != '.') {
                if (map.contains(c)) {
                    var t = map.get(c);
                    const index = t.?.count;
                    t.?.positions[index] = Position{ .x = u2i(x), .y = u2i(y) };
                    t.?.count += 1;
                    try map.put(c, t.?);
                } else {
                    var t = TmpS{ .count = 0, .positions = try allocator.alloc(Position, 100) };
                    const index = t.count;
                    t.positions[index] = Position{ .x = u2i(x), .y = u2i(y) };
                    t.count += 1;
                    try map.put(c, t);
                }
            }
        }
    }

    var index: usize = 0;
    var iter = map.iterator();
    while (iter.next()) |entry| {
        const t = entry.value_ptr;
        const c = entry.key_ptr;
        const newEntry = FreqPos{ .freq = c.*, .positions = try allocator.alloc(Position, t.*.count) };
        for (0..t.*.count) |i| {
            newEntry.positions[i] = t.*.positions[i];
        }
        freqPosse[index] = newEntry;
        index += 1;
    }

    return Frequencies{ .freqs = freqPosse };
}

fn setAtPos(pos: Position, c: u8) bool {
    // std.debug.print("Place {u} at {d},{d}\n", .{ c, pos.x, pos.y });
    if (pos.x < 0 or pos.y < 0 or pos.x >= dim.x or pos.y >= dim.y) {
        // we are off the map, so do nothing
        return false;
    }
    const x = i2u(pos.x);
    const y = i2u(pos.y);
    antennaMap[x][y] = c;
    return true;
}

fn placeAntinodesForP1P2(pos1: Position, pos2: Position) void {
    const deltaX = pos1.x - pos2.x;
    const deltaY = pos1.y - pos2.y;
    var antiNode = Position{ .x = pos1.x, .y = pos1.y };
    var carryOn = true;
    while (carryOn) {
        antiNode = Position{ .x = antiNode.x + deltaX, .y = antiNode.y + deltaY };
        carryOn = setAtPos(antiNode, '#');
    }

    antiNode = Position{ .x = pos2.x, .y = pos2.y };
    carryOn = true;
    while (carryOn) {
        antiNode = Position{ .x = antiNode.x - deltaX, .y = antiNode.y - deltaY };
        carryOn = setAtPos(antiNode, '#');
    }
    // std.debug.print("Placing for {u} p1: {d},{d} p2: {d},{d} delta: {d},{d}\n", .{ freq, pos1.x, pos1.y, pos2.x, pos2.y, deltaX, deltaY });
}

fn placeAntinodes(frequencies: Frequencies) void {
    for (frequencies.freqs) |fpos| {
        for (0..fpos.positions.len - 1) |i| {
            const pos1 = fpos.positions[i];
            for (i + 1..fpos.positions.len) |j| {
                const pos2 = fpos.positions[j];
                placeAntinodesForP1P2(pos1, pos2);
            }
        }
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
            allocator.free(f.positions);
        }
        allocator.free(frequencies.freqs);
    }

    for (frequencies.freqs) |f| {
        std.debug.print("{u}\n", .{f.freq});
        for (f.positions) |pos| {
            std.debug.print("\t{d},{d}\n", .{ pos.x, pos.y });
        }
    }

    placeAntinodes(frequencies);
    printMap(uniqueFrequencies);
}
