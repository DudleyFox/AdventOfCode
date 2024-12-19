const std = @import("std");
const input = @embedFile("testinput.txt");
const ParseErrors = error{tooManyParts};

const Equation = struct { result: u64, operands: []u64 };

fn parseToEquation(allocator: anytype, lineToParse: []const u8) !Equation {
    var count: u64 = 0;
    var total: u64 = 0;
    var operands = std.ArrayList(u64).init(allocator);
    defer operands.deinit();
    var parts = std.mem.split(u8, lineToParse, ":");
    while (parts.next()) |part| {
        if (part.len > 0) {
            if (count == 0) {
                total = try std.fmt.parseInt(u64, part, 10);
            } else if (count == 1) {
                var operandParts = std.mem.split(u8, part, " ");
                while (operandParts.next()) |operand| {
                    if (operand.len > 0) {
                        const op: u64 = try std.fmt.parseInt(u64, operand, 10);
                        _ = try operands.append(op);
                    }
                }
            } else {
                return ParseErrors.tooManyParts;
            }
        }
        count += 1;
    }

    const equation = Equation{ .result = total, .operands = try allocator.alloc(u64, operands.items.len) };
    @memcpy(equation.operands, operands.items);

    return equation;
}

fn printEquation(equation: Equation) void {
    std.debug.print("{d} = {d}\n", .{ equation.result, equation.operands });
}

fn generateOperators(operandsLen: usize, operators: []u8, allocator: anytype) ![][]u8 {
    const operatorStringLength = operandsLen - 1;
    const operatorListLength = std.math.pow(u64, operators.len, operatorStringLength);
    var list = try allocator.alloc([]u8, operatorListLength);
    for (0..operatorListLength) |i| {
        list[i] = try allocator.alloc(u8, operatorStringLength);
        for (0..operatorStringLength) |j| {
            const index = i * j;
            list[i][j] = operators[index % operators.len];
        }
    }
    return list;
}

fn apply(equation: Equation, operators: []u8) u64 {
    const operands = equation.operands;
    var total: u64 = operands[0];
    for (operators, 0..) |op, i| {
        switch (op) {
            '+' => total = total + operands[i + 1],
            '*' => total = total * operands[i + 1],
            else => {
                std.debug.print("Unknown operator {u}\n", .{op});
            },
        }
    }
    return total;
}

fn testEquation(equation: Equation, allowedOperators: []u8) !bool {
    var isValid = false;
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();
    const operatorsList = try generateOperators(equation.operands.len, allowedOperators, allocator);
    defer {
        for (0..operatorsList.len) |i| {
            allocator.free(operatorsList[i]);
        }
        allocator.free(operatorsList);
    }
    for (operatorsList) |ops| {
        std.debug.print("Testing Ops {s}\n", .{ops});
        const result: u64 = apply(equation, ops);
        const isEqual = equation.result == result;
        isValid = isValid or isEqual;
        if (isEqual) {
            printEquation(equation);
            std.debug.print("Works for {s}\n\n", .{ops});
        }
    }

    return isValid;
}

fn sumPossibleEquations() !u64 {
    var lines = std.mem.split(u8, input, "\n");
    var total: u64 = 0;
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();
    var allowedOperators = try allocator.alloc(u8, 2);
    defer allocator.free(allowedOperators);
    allowedOperators[0] = '+';
    allowedOperators[1] = '*';

    while (lines.next()) |line| {
        if (line.len > 0) {
            const equation = try parseToEquation(allocator, line);
            defer allocator.free(equation.operands);
            if (try testEquation(equation, allowedOperators[0..])) {
                total += equation.result;
            }
        }
    }
    return total;
}

pub fn main() !void {
    const result = try sumPossibleEquations();
    std.debug.print("{d}\n", .{result});
}
