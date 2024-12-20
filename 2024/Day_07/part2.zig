const std = @import("std");
const input = @embedFile("input.txt");
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

fn recurseOperators(operatorsNeeded: usize, operators: []u8, length: usize, currentOperators: []u8, equation: Equation) bool {
    if (length == operatorsNeeded) {
        const result = apply(equation, currentOperators);
        // std.debug.print("Result for:\n", .{});
        // printEquation(equation);
        // std.debug.print("Operands {d} {} {u}\n\n", .{ result, result == equation.result, currentOperators });
        return result == equation.result;
    }
    var intermediateResult = false;
    for (operators) |op| {
        currentOperators[length] = op;
        intermediateResult = recurseOperators(operatorsNeeded, operators, length + 1, currentOperators, equation) or intermediateResult;
    }

    return intermediateResult;
}

fn lexicalConcat(a: u64, b: u64) u64 {
    const exponent = (std.math.log(u64, 10, b) + 1);
    const front = a * std.math.pow(u64, 10, exponent);
    const result = front + b;
    // // std.debug.print("{} {} {} {}\n", .{ a, b, front, result });
    return result;
}

fn apply(equation: Equation, operators: []u8) u64 {
    // std.debug.print("Applying {s} to ", .{operators});
    // printEquation(equation);
    const operands = equation.operands;
    var total: u64 = operands[0];
    for (operators, 0..) |op, i| {
        switch (op) {
            '+' => total = total + operands[i + 1],
            '*' => total = total * operands[i + 1],
            '|' => total = lexicalConcat(total, operands[i + 1]),
            else => {
                std.debug.print("Unknown operator {u}\n", .{op});
            },
        }
    }
    return total;
}

fn testEquation(equation: Equation, allowedOperators: []u8) !bool {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();
    var currentOperators = try allocator.alloc(u8, equation.operands.len - 1);
    for (0..currentOperators.len) |i| {
        currentOperators[i] = 0;
    }
    defer allocator.free(currentOperators);

    return recurseOperators(equation.operands.len - 1, allowedOperators, 0, currentOperators, equation);
}

fn sumPossibleEquations() !u64 {
    var lines = std.mem.split(u8, input, "\n");
    var total: u64 = 0;
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();
    var allowedOperators = try allocator.alloc(u8, 3);
    defer allocator.free(allowedOperators);
    allowedOperators[0] = '+';
    allowedOperators[1] = '*';
    allowedOperators[2] = '|'; // the website uses ||, but | is finr for my purposes

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
