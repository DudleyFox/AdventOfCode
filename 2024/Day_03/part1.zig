const std = @import("std");
const input = @embedFile("input.txt");

const OpName = enum { mul, div, add, sub, unknown, done };

const Expected = enum { m, u, l, open, num, comma, close };

const Operation = struct { op: OpName, n1: u32 = 0, n2: u32 = 0, token: [3]u8 = undefined, tokenIndex: u8 = 0, expected: Expected = Expected.m, nextPos: u32 = 0 };

// use a recursive descent parser like function

fn parse(position: u32, op: *Operation) Operation {
    if (position > input.len) {
        return Operation{ .op = OpName.done };
    }
    const x = input[position];
    switch (x) {
        'm' => {
            if (op.*.expected == Expected.m) {
                op.*.expected = Expected.u;
                op.*.nextPos = position + 1;
                return parse(position + 1, op);
            }
        },
        'u' => {
            if (op.*.expected == Expected.u) {
                op.*.expected = Expected.l;
                op.*.nextPos = position + 1;
                return parse(position + 1, op);
            }
        },
        'l' => {
            if (op.*.expected == Expected.l) {
                op.*.expected = Expected.open;
                op.*.nextPos = position + 1;
                return parse(position + 1, op);
            }
        },
        '(' => {
            if (op.*.expected == Expected.open) {
                op.*.expected = Expected.num;
                op.*.nextPos = position + 1;
                return parse(position + 1, op);
            }
        },
        '0'...'9' => {
            if (op.*.expected == Expected.num) {
                if (op.*.tokenIndex < 3) {
                    op.*.token[op.*.tokenIndex] = x;
                    op.*.tokenIndex += 1;
                    op.*.expected = Expected.num;
                    op.*.nextPos = position + 1;
                    return parse(position + 1, op);
                }
            }
        },
        ',' => {
            if (op.*.expected == Expected.num) {
                op.*.expected = Expected.num;
                op.*.n1 = std.fmt.parseInt(u32, op.*.token[0..op.*.tokenIndex], 10) catch 1001;
                op.*.tokenIndex = 0;
                op.*.nextPos = position + 1;
                return parse(position + 1, op);
            }
        },
        ')' => {
            if (op.*.expected == Expected.num) {
                op.*.expected = Expected.m;
                op.*.n2 = std.fmt.parseInt(u32, op.*.token[0..op.*.tokenIndex], 10) catch 1001;
                op.*.nextPos = position + 1;
                return op.*;
            }
        },
        else => {
            // let the switch fall out and return unknown
        },
    }
    std.debug.print("Expected {s}: got {c}\n", .{ @tagName(op.*.expected), x });

    return Operation{ .op = OpName.unknown, .nextPos = position + 1 };
}

fn Operate(op: Operation) u32 {
    return switch (op.op) {
        OpName.mul => op.n1 * op.n2,
        else => 0,
    };
}

pub fn main() anyerror!void {
    var currentPosition: u32 = 0;
    var sum: u32 = 0;
    while (currentPosition < input.len) {
        var op = Operation{ .op = OpName.mul, .nextPos = currentPosition, .n1 = 0, .n2 = 0, .tokenIndex = 0, .expected = Expected.m };
        op = parse(currentPosition, &op);
        currentPosition = op.nextPos;
        sum += Operate(op);
        std.debug.print("{s} {d} {d} {d}\n", .{ @tagName(op.op), op.n1, op.n2, sum });
    }
}
