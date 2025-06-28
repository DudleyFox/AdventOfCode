const std = @import("std");
const Allocator = std.mem.Allocator;
const printTheMap = true;
const input = @embedFile("testinput.txt");
const Dimensions = struct { x: u32, y: u32 };
const dim = computeDimensions();
var gardenMap: [dim.x][dim.y]u8 = buildGardenMap();

const Position = struct { x: isize, y: isize };

const Region = struct {
    flower: u8,
    positions: std.ArrayList(Position),

    pub fn inRegion(self: *Region, flower: u8, pos: Position) bool {
        if (flower != self.flower) {
            return false;
        }
        if (self.positions.items.len == 0) {
            // nothing here yet, so add it
            return true;
        }
        for (self.positions.items) |p| {
            const xDelta = @abs(p.x - pos.x);
            const yDelta = @abs(p.y - pos.y);
            if ((xDelta == 0 and yDelta == 1) or (xDelta == 1 and yDelta == 0)) {
                return true;
            }
        }
        return false;
    }

    // Return true if we added the flower, false if we did not.
    fn addFlower(self: *Region, flower: u8, pos: Position) !bool {
        if (self.inRegion(flower, pos)) {
            _ = try self.positions.append(pos);
            return true;
        }
        return false;
    }

    fn print(self: *Region) void {
        std.debug.print("Region: {u} {d}\n", .{ self.*.flower, self.size });
    }
};

const Regions = struct {
    regions: std.ArrayList(Region),

    fn addRegion(self: Regions, region: Region) !void {
        _ = try self.regions.append(region);
    }
};

fn buildGardenMap() [dim.x][dim.y]u8 {
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
    // wrap this in a function so all the int casting happens in one place;
    if (stillOnMap(pos)) {
        const x = @as(usize, @intCast(pos.x));
        const y = @as(usize, @intCast(pos.y));
        return gardenMap[x][y];
    }

    return 0;
}

fn u2i(in: usize) isize {
    return @as(isize, @intCast(in));
}

fn setAtPos(pos: Position, c: u8) void {
    // wrap this in a function so all the int casting happens in one place;
    if (stillOnMap(pos)) {
        const x = @as(usize, @intCast(pos.x));
        const y = @as(usize, @intCast(pos.y));
        gardenMap[x][y] = c;
    }
}

fn stillOnMap(pos: Position) bool {
    return (pos.x < dim.x and pos.y < dim.y and pos.x >= 0 and pos.y >= 0);
}

fn buildRegions(allocator: Allocator) !Regions {
    var regions = Regions{ .regions = std.ArrayList(Region).init(allocator) };
    for (0..dim.y) |y| {
        for (0..dim.x) |x| {
            var added = false;
            const flower = gardenMap[x][y];
            const position = Position{ .x = u2i(x), .y = u2i(y) };
            for (regions.regions.items) |r| {
                added = try r.addFlower(flower, position);
                if (added) {
                    break;
                }
            }
            if (!added) { // it didn't fit in any region
                var region = Region{ .flower = flower, .positions = std.ArrayList(Position).init(allocator) };
                region.addFlower(flower, position);
                regions.addRegion(region);
            }
        }
    }
    return regions;
}

fn printMap() void {
    // clear screen move cursor to top left
    if (printTheMap) {
        std.debug.print("\x1B[2J\x1B[H", .{});
        for (0..dim.y) |y| {
            for (0..dim.x) |x| {
                std.debug.print("{u}", .{gardenMap[x][y]});
            }
            std.debug.print("\n", .{});
        }
    }
    // std.time.sleep(1000 * 1000 * millisToSleep);
}

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();
    printMap();
    const regions = try buildRegions(allocator);
    for (regions.regions.items) |r| {
        r.print();
    }
}
