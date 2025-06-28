const std = @import("std");

const Foo = struct {
    fixture: u8,
    xfer: u16,

    pub fn setFxFer(self: *Foo, f: u8, x: u16) void {
        self.fixture = f;
        self.xfer = x;
    }
};

fn fooList() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();
    var foos = std.ArrayList(Foo).init(allocator);
    _ = try foos.append(Foo{ .fixture = 1, .xfer = 2 });
    _ = try foos.append(Foo{ .fixture = 1, .xfer = 2 });
    _ = try foos.append(Foo{ .fixture = 1, .xfer = 2 });
    for (foos.items, 0..) |f, i| {
        f.setFxFer(i, i * 2);
        std.debug.print("\t{} {}\n", f);
    }
}

pub fn main() void {
    var t = Foo{ .fixture = 0, .xfer = 0 };
    t.setFxFer(1, 2);
    std.debug.print("{} {}\n", t);
    try fooList();
}
