const std = @import("std");
const input = @embedFile("testinput.txt");

const OpName = enum { mul, div, add, sub, unknown, done };

const Expected = enum { m, u, l, open, num, numOrComma, numOrClose, comma, close };

const Operation = struct { op: OpName, n1: u32, n2: u32, token: [3]u8, tokenCount: u8, expected: Expected, nextPos: u32 };

// use a recursive descent parser like set of functions

fn parse(position: u32, op: Operation) Operation {
    if (position > input.length) {
        return Operation{ .op = OpName.done };
    }
    switch (input[position]) {
        'm' => {
            if (op.expected == Expected.m) {
                op.expected = Expected.u;
                op.nextPos = position + 1;
                return parse(position + 1, op);
            }
        },
    }
}

pub fn main() anyerror!void {
    for (input) |i| {
        std.debug.print("{c}", .{i});
    }
}
