const std = @import("std");
const printTheMap = true;
const printDebug = false;
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
const BreadCrumb = struct { pos: Position, facing: Facing };
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

fn printPossesAndFacings(index: usize, currentPos: Position, pastPos: Position, currentFacing: Facing, pastFacing: Facing) void {
    if (printDebug) {
        std.debug.print("Index: {d}\n", .{index});
        std.debug.print("Pos - Current: {d},{d} Past: {d},{d}\n", .{ currentPos.x, currentPos.y, pastPos.x, pastPos.y });
        std.debug.print("Facing - Current: {s} Past: {s}\n", .{ @tagName(currentFacing.name), @tagName(pastFacing.name) });
        std.debug.print("\n", .{});
    }
}

fn beenHereBefore(pos: Position, facing: Facing, breadCrumbs: []BreadCrumb, length: u32) bool {
    for (0..length) |index| {
        const breadCrumb = breadCrumbs[index];
        const pastPos = breadCrumb.pos;
        const pastFacing = breadCrumb.facing;
        printPossesAndFacings(index, pos, pastPos, facing, pastFacing);
        if (pastPos.x == pos.x and pastPos.y == pos.y and pastFacing.name == facing.name) {
            return true;
        }
    }
    return false;
}

fn findLoop(startingPos: Position, startingFacing: Facing) bool {
    var pos = Position{ .x = startingPos.x, .y = startingPos.y };
    var facing = Facing{ .name = startingFacing.name, .x = startingFacing.x, .y = startingFacing.y };
    var count: u32 = 0;
    var breadCrumbs: [dim.x * dim.y]BreadCrumb = undefined;

    while (stillOnMap(pos)) {
        if (beenHereBefore(pos, facing, &breadCrumbs, count)) {
            std.debug.print("Found Loop *****************\n", .{});
            return true;
        }
        // Learn how struct assignment/copy works.
        breadCrumbs[count] = BreadCrumb{ .pos = Position{ .x = pos.x, .y = pos.y }, .facing = Facing{ .name = facing.name, .x = facing.x, .y = facing.y } };
        count += 1;
        var newPos = Position{ .x = pos.x + facing.x, .y = pos.y + facing.y };
        if (stillOnMap(newPos)) {
            var spot = getAtPos(newPos);
            while (spot == '#' or spot == '0') {
                facing = turnRight(facing);
                newPos = Position{ .x = pos.x + facing.x, .y = pos.y + facing.y };
                spot = getAtPos(newPos);
            }
        }
        pos = newPos;
        if (count > dim.x * dim.y) {
            return true;
        }
    }
    std.debug.print("Walked off map with count of {d}\n", .{count});
    return false;
}

fn walk(startingPos: Position, startingFacing: Facing) void {
    var pos = Position{ .x = startingPos.x, .y = startingPos.y };
    var facing = Facing{ .name = startingFacing.name, .x = startingFacing.x, .y = startingFacing.y };

    while (stillOnMap(pos)) {
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
}

fn tryAllObstacles(pos: Position, facing: Facing) u32 {
    var sum: u32 = 0;
    setAtPos(pos, 'G'); // put the guard back;
    for (0..dim.y) |y| {
        for (0..dim.x) |x| {
            std.debug.print("Trying {d},{d}\n", .{ x, y });
            const currentPos = Position{ .x = @as(isize, @intCast(x)), .y = @as(isize, @intCast(y)) };
            const icon = getAtPos(currentPos);
            switch (icon) {
                'X' => {
                    setAtPos(currentPos, '0');
                    // printMap();
                    if (findLoop(pos, facing)) {
                        sum += 1;
                        std.debug.print("Placing Obstacle at {d},{d} creates a loop\n", .{ x, y });
                    } else {}
                    setAtPos(currentPos, 'X'); // make sure to set it back

                },
                '#' => {
                    // skip this one it already has an obstacle
                    std.debug.print("Obstacle already at {d},{d}\n", .{ x, y });
                },
                'G' => {
                    // can't put an obstacle on a guard
                    std.debug.print("Guard already at {d},{d}\n", .{ x, y });
                },
                '.' => {
                    // can't put an obstacle on a guard
                    std.debug.print("{d},{d} Is not on path\n", .{ x, y });
                },
                else => {
                    // can't put an obstacle on a guard
                    std.debug.print("Guard already at {d},{d}\n", .{ x, y });
                },
            }
        }
    }

    return sum;
}

fn printMap() void {
    // clear screen move cursor to top left
    for (0..dim.y) |y| {
        for (0..dim.x) |x| {
            std.debug.print("{u}", .{guardMap[x][y]});
        }
        std.debug.print("\n", .{});
    }
}

pub fn main() !void {
    const pos = try findGuardPosition();
    const facing = try getInitialFacing(pos);
    var result: u32 = 0;
    walk(pos, facing); // mark all the X's
    printMap();
    result = tryAllObstacles(pos, facing);
    std.debug.print("Found {d} obstacle placements\n", .{result});
}
