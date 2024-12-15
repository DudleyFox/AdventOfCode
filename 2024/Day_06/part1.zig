const std = @import("std");
const printTheMap = false;
const millisToSleep = 250;
const input = @embedFile("input.txt");
const Dimensions = struct { x: u32, y: u32 };
const dim = computeDimensions();
var guardMap: [dim.x][dim.y]u8 = buildGuardMap();
const Position = struct { x: isize, y: isize };
const FacingName = enum {
    NORTH,
    SOUTH,
    EAST,
    WEST,
};
const Facing = struct { name: FacingName, x: i8, y: i8 };
const GuardErrors = error{ UnknownFacing, GuardMissing };

fn buildGuardMap() [dim.x][dim.y]u8 {
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

fn findGuardPosition() !Position {
    for (0..dim.x) |x| {
        for (0..dim.y) |y| {
            const c = guardMap[x][y];
            switch (c) {
                '#' => {}, // pass
                '.' => {}, // pass
                else => return Position{ .x = @as(isize, @intCast(x)), .y = @as(isize, @intCast(y)) },
            }
        }
    }
    return GuardErrors.GuardMissing;
}

fn getAtPos(pos: Position) u8 {
    // wrap this in a function so all the int casting happend in one place;
    if (stillOnMap(pos)) {
        const x = @as(usize, @intCast(pos.x));
        const y = @as(usize, @intCast(pos.y));
        return guardMap[x][y];
    }

    return 0;
}

fn setAtPos(pos: Position, c: u8) void {
    // wrap this in a function so all the int casting happend in one place;
    if (stillOnMap(pos)) {
        const x = @as(usize, @intCast(pos.x));
        const y = @as(usize, @intCast(pos.y));
        guardMap[x][y] = c;
    }
}

fn getInitialFacing(pos: Position) !Facing {
    const g = getAtPos(pos);
    return switch (g) {
        '^' => Facing{ .name = FacingName.NORTH, .x = 0, .y = -1 },
        'v' => Facing{ .name = FacingName.SOUTH, .x = 0, .y = 1 },
        '>' => Facing{ .name = FacingName.EAST, .x = 1, .y = 0 },
        '<' => Facing{ .name = FacingName.WEST, .x = -1, .y = 0 },
        else => GuardErrors.UnknownFacing,
    };
}

fn stillOnMap(pos: Position) bool {
    return (pos.x < dim.x and pos.y < dim.y and pos.x >= 0 and pos.y >= 0);
}

fn turnRight(facing: Facing) Facing {
    return switch (facing.name) {
        FacingName.NORTH => Facing{ .name = FacingName.EAST, .x = 1, .y = 0 },
        FacingName.SOUTH => Facing{ .name = FacingName.WEST, .x = -1, .y = 0 },
        FacingName.EAST => Facing{ .name = FacingName.SOUTH, .x = 0, .y = 1 },
        FacingName.WEST => Facing{ .name = FacingName.NORTH, .x = 0, .y = -1 },
    };
}

fn walk(startingPos: Position, startingFacing: Facing) void {
    var pos = Position{ .x = startingPos.x, .y = startingPos.y };
    var facing = Facing{ .name = startingFacing.name, .x = startingFacing.x, .y = startingFacing.y };

    while (stillOnMap(pos)) {
        printMap(pos, facing);
        setAtPos(pos, 'X');
        var newPos = Position{ .x = pos.x + facing.x, .y = pos.y + facing.y };
        if (stillOnMap(newPos)) {
            while (getAtPos(newPos) == '#') {
                std.debug.print("Turning Right\n", .{});
                facing = turnRight(facing);
                newPos = Position{ .x = pos.x + facing.x, .y = pos.y + facing.y };
            }
        }
        pos = newPos;
    }
    printMap(pos, facing);
}

fn printMap(pos: Position, facing: Facing) void {
    // clear screen move cursor to top left
    if (printTheMap) {
        std.debug.print("\x1B[2J\x1B[H", .{});
        for (0..dim.y) |y| {
            for (0..dim.x) |x| {
                if (pos.x == x and pos.y == y) {
                    switch (facing.name) {
                        FacingName.NORTH => std.debug.print("^", .{}),
                        FacingName.SOUTH => std.debug.print("v", .{}),
                        FacingName.EAST => std.debug.print(">", .{}),
                        FacingName.WEST => std.debug.print("<", .{}),
                    }
                } else {
                    std.debug.print("{u}", .{guardMap[x][y]});
                }
            }
            std.debug.print("\n", .{});
        }
    }
    std.debug.print("Pos {d},{d}\n", .{ pos.x, pos.y });
    std.debug.print("Facing {s}: {d},{d}\n", .{ @tagName(facing.name), facing.x, facing.y });
    // std.time.sleep(1000 * 1000 * millisToSleep);
}

fn countPositions() u32 {
    var sum: u32 = 0;
    for (0..dim.y) |y| {
        for (0..dim.x) |x| {
            sum += if (guardMap[x][y] == 'X') 1 else 0;
        }
    }

    return sum;
}

pub fn main() !void {
    const pos = try findGuardPosition();
    const facing = try getInitialFacing(pos);
    walk(pos, facing);
    const uniquePositions = countPositions();
    std.debug.print("Visited {d}\n", .{uniquePositions});
}
