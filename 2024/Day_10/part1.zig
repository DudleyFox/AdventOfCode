const std = @import("std");
const printTheMap = true;
const millisToSleep = 250;
const input = @embedFile("input.txt");
const Dimensions = struct { x: u32, y: u32 };
const dim = computeDimensions();
var trailMap: [dim.x][dim.y]u8 = buildTrailMap();
const Position = struct { x: isize, y: isize };

fn buildTrailMap() [dim.x][dim.y]u8 {
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

fn getAtPos(pos: Position) u8 {
    // wrap this in a function so all the int casting happend in one place;
    if (stillOnMap(pos)) {
        const x = @as(usize, @intCast(pos.x));
        const y = @as(usize, @intCast(pos.y));
        return trailMap[x][y];
    }

    return 200;
}

fn setAtPos(pos: Position, c: u8) void {
    // wrap this in a function so all the int casting happend in one place;
    if (stillOnMap(pos)) {
        const x = @as(usize, @intCast(pos.x));
        const y = @as(usize, @intCast(pos.y));
        trailMap[x][y] = c;
    }
}

fn stillOnMap(pos: Position) bool {
    return (pos.x < dim.x and pos.y < dim.y and pos.x >= 0 and pos.y >= 0);
}

fn printMap() void {
    // clear screen move cursor to top left
    if (printTheMap) {
        std.debug.print("\x1B[2J\x1B[H", .{});
        for (0..dim.y) |y| {
            for (0..dim.x) |x| {
                std.debug.print("{u}", .{trailMap[x][y]});
            }
            std.debug.print("\n", .{});
        }
    }
}

fn computeDelta(a: u8, b: u8) u8 {
    return if (a > b) a - b else b - a;
}

fn haveVisited(pos: Position, visted: anytype) bool {
    for (visted.items) |position| {
        if (pos.x == position.x and pos.y == position.y) {
            return true;
        }
    }
    return false;
}

fn hikeAllTrails(currentPos: Position, visited: anytype) !u32 {
    std.debug.print("Testing ", .{});
    printPos(currentPos);
    std.debug.print("\n", .{});
    const directions = [_]Position{ Position{ .x = 1, .y = 0 }, Position{ .x = -1, .y = 0 }, Position{ .x = 0, .y = 1 }, Position{ .x = 0, .y = -1 } };
    if (!stillOnMap(currentPos)) {
        return 0;
    }
    const currentValue = getAtPos(currentPos);

    if (currentValue == '9') {
        if (!haveVisited(currentPos, visited.*)) {
            try visited.*.append(currentPos);
            return 1;
        } else {
            return 0;
        }
    }

    var currentSum: u32 = 0;

    for (directions) |direction| {
        const newPos = Position{ .x = currentPos.x + direction.x, .y = currentPos.y + direction.y };
        const newValue = getAtPos(newPos);
        if (computeDelta(newValue, currentValue) == 1 and newValue > currentValue) {
            currentSum += try hikeAllTrails(newPos, visited);
        }
    }

    return currentSum;
}

fn u2i(in: usize) isize {
    return @as(isize, @intCast(in));
}

fn printPos(pos: Position) void {
    std.debug.print("{d},{d}", .{ pos.x, pos.y });
}

fn findNines() !u32 {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();
    var sum: u32 = 0;
    for (0..dim.y) |y| {
        for (0..dim.x) |x| {
            const c = trailMap[x][y];
            if (c == '0') {
                var visited = std.ArrayList(Position).init(allocator);
                defer visited.deinit();
                std.debug.print("Found Trailhead at ", .{});
                const pos = Position{ .x = u2i(x), .y = u2i(y) };
                printPos(pos);
                std.debug.print("\n", .{});
                sum += try hikeAllTrails(pos, &visited);
            }
        }
    }

    return sum;
}

pub fn main() !void {
    printMap();
    const sum = try findNines();
    std.debug.print("total {d}\n", .{sum});
}
