const std = @import("std");
const input = @embedFile("input.txt");

// The operation we have found
const OpName = enum { mul, do, dont, unknown, done };

// What we expect to come next
const Expected = enum { m, u, l, open, num, comma, close, d, o, n, tick, t };

// The operation to "run"
const Operation = struct { op: OpName, n1: u32 = 0, n2: u32 = 0 };

// The state of the "machine" Welcome to it
const MachineState = struct { enabled: bool = true, accumulator: u32 = 0 };

// State we keep as we parse
const ParseState = struct { n1: u32 = 0, n2: u32 = 0, token: [3]u8 = undefined, tokenIndex: u8 = 0, expected: Expected = Expected.m };

// The result of parsing out an Operation.
const ParseResult = struct { operation: Operation, nextPosition: u32 };

fn mul(position: u32, ps: *ParseState) ParseResult {
    const x = input[position];
    switch (x) {
        'm' => {
            if (ps.*.expected == Expected.m) {
                ps.*.expected = Expected.u;
                return mul(position + 1, ps);
            }
        },
        'u' => {
            if (ps.*.expected == Expected.u) {
                ps.*.expected = Expected.l;
                return mul(position + 1, ps);
            }
        },
        'l' => {
            if (ps.*.expected == Expected.l) {
                ps.*.expected = Expected.open;
                return mul(position + 1, ps);
            }
        },
        '(' => {
            if (ps.*.expected == Expected.open) {
                ps.*.expected = Expected.num;
                return mul(position + 1, ps);
            }
        },
        '0'...'9' => {
            if (ps.*.expected == Expected.num) {
                if (ps.*.tokenIndex < 3) {
                    ps.*.token[ps.*.tokenIndex] = x;
                    ps.*.tokenIndex += 1;
                    ps.*.expected = Expected.num;
                    return mul(position + 1, ps);
                }
            }
        },
        ',' => {
            if (ps.*.expected == Expected.num) {
                ps.*.expected = Expected.num;
                ps.*.n1 = std.fmt.parseInt(u32, ps.*.token[0..ps.*.tokenIndex], 10) catch 1001;
                ps.*.tokenIndex = 0;
                return mul(position + 1, ps);
            }
        },
        ')' => {
            if (ps.*.expected == Expected.num) {
                ps.*.expected = Expected.m;
                ps.*.n2 = std.fmt.parseInt(u32, ps.*.token[0..ps.*.tokenIndex], 10) catch 1001;
                return ParseResult{ .operation = Operation{
                    .op = OpName.mul,
                    .n1 = ps.*.n1,
                    .n2 = ps.*.n2,
                }, .nextPosition = position + 1 };
            }
        },
        else => {
            // let the switch fall out and return unknown
        },
    }
    std.debug.print("Expected {s}: got {c}\n", .{ @tagName(ps.*.expected), x });

    return ParseResult{ .operation = Operation{ .op = OpName.unknown }, .nextPosition = position };
}

fn dont(position: u32, ps: *ParseState) ParseResult {
    const x = input[position];
    switch (x) {
        'd' => {
            if (ps.*.expected == Expected.d) {
                ps.*.expected = Expected.o;
                return dont(position + 1, ps);
            }
        },
        'o' => {
            if (ps.*.expected == Expected.o) {
                ps.*.expected = Expected.n;
                return dont(position + 1, ps);
            }
        },
        'n' => {
            if (ps.*.expected == Expected.n) {
                ps.*.expected = Expected.tick;
                return dont(position + 1, ps);
            }
        },
        '\'' => {
            if (ps.*.expected == Expected.tick) {
                ps.*.expected = Expected.t;
                return dont(position + 1, ps);
            }
        },
        't' => {
            if (ps.*.expected == Expected.t) {
                ps.*.expected = Expected.open;
                return dont(position + 1, ps);
            }
        },
        '(' => {
            if (ps.*.expected == Expected.open) {
                ps.*.expected = Expected.close;
                return dont(position + 1, ps);
            }
        },
        ')' => {
            if (ps.*.expected == Expected.close) {
                ps.*.expected = Expected.close;
                return ParseResult{ .operation = Operation{ .op = OpName.dont }, .nextPosition = position + 1 };
            }
        },
        else => {
            // let the switch fall out and return unknown
        },
    }
    std.debug.print("Expected {s}: got {c}\n", .{ @tagName(ps.*.expected), x });
    return ParseResult{ .operation = Operation{ .op = OpName.unknown }, .nextPosition = position };
}

fn do(position: u32, ps: *ParseState) ParseResult {
    const x = input[position];
    switch (x) {
        'd' => {
            if (ps.*.expected == Expected.d) {
                ps.*.expected = Expected.o;
                return do(position + 1, ps);
            }
        },
        'o' => {
            if (ps.*.expected == Expected.o) {
                ps.*.expected = Expected.open;
                return do(position + 1, ps);
            }
        },
        '(' => {
            if (ps.*.expected == Expected.open) {
                ps.*.expected = Expected.close;
                return do(position + 1, ps);
            }
        },
        ')' => {
            if (ps.*.expected == Expected.close) {
                ps.*.expected = Expected.close;
                return ParseResult{ .operation = Operation{ .op = OpName.do }, .nextPosition = position };
            }
        },
        else => {
            // let the switch fall out and return unknown
        },
    }
    std.debug.print("Expected {s}: got {c}\n", .{ @tagName(ps.*.expected), x });
    return ParseResult{ .operation = Operation{ .op = OpName.unknown }, .nextPosition = position + 1 };
}

fn doOrDont(position: u32, ps: *ParseState) ParseResult {
    const result = do(position, ps);
    if (result.operation.op == OpName.unknown) {
        ps.*.expected = Expected.d;
        return dont(position, ps);
    }
    return result;
}

fn parse(position: u32, ps: *ParseState) ParseResult {
    if (position > input.len) {
        return ParseResult{ .operation = Operation{ .op = OpName.done }, .nextPosition = input.len + 1 };
    }

    const x = input[position];
    switch (x) {
        'm' => {
            ps.*.expected = Expected.m;
            return mul(position, ps);
        },
        'd' => {
            ps.expected = Expected.d;
            return doOrDont(position, ps);
        },
        else => return ParseResult{ .operation = Operation{ .op = OpName.unknown }, .nextPosition = position + 1 },
    }
}

fn Operate(op: Operation, ms: *MachineState) void {
    switch (op.op) {
        OpName.mul => {
            std.debug.print("*** Mul\n", .{});
            ms.*.accumulator += if (ms.*.enabled) op.n1 * op.n2 else 0;
        },
        OpName.do => {
            std.debug.print("*** Do\n", .{});
            ms.*.enabled = true;
        },
        OpName.dont => {
            std.debug.print("*** Don't\n", .{});
            ms.*.enabled = false;
        },
        else => {
            // if we don't know what it is, do nothing
        },
    }
    std.debug.print("Machine State: Enabled: {} Accumilator: {}\n", .{ ms.*.enabled, ms.*.accumulator });
}

pub fn main() anyerror!void {
    var currentPosition: u32 = 0;
    var ms = MachineState{};
    while (currentPosition < input.len) {
        var ps = ParseState{};
        const pr = parse(currentPosition, &ps);
        currentPosition = pr.nextPosition;
        std.debug.print("Pos {}\n", .{currentPosition});
        Operate(pr.operation, &ms);
    }
}
