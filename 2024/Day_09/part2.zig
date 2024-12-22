const std = @import("std");
const input = @embedFile("testinput.txt");
const BlockType = enum { FILE, FREE };
const DiskBlock = struct { fileId: i32, size: u32, blockType: BlockType, prev: ?*DiskBlock, next: ?*DiskBlock };
const DiskReference = struct { head: ?*DiskBlock, tail: ?*DiskBlock, maxFileId: i32 };
const printTheDisk = false;

fn inRange(toTest: u8, min: u8, max: u8) bool {
    return (toTest >= min and toTest <= max);
}

fn buildExpandedMap(allocator: anytype) !DiskReference {
    var disk = DiskReference{ .head = null, .tail = null, .maxFileId = 0 };
    var fileIndex: i32 = 0;
    var isFile = true;
    for (input) |c| {
        if (inRange(c, '0', '9')) {
            const x: u16 = c - '0';
            if (isFile) {
                if (disk.head == null) {
                    // the first one
                    disk.head = try allocator.create(DiskBlock);
                    disk.tail = disk.head;
                    disk.head.?.*.fileId = fileIndex;
                    disk.head.?.*.size = x;
                    disk.head.?.*.blockType = BlockType.FILE;
                    disk.head.?.*.next = null;
                    disk.head.?.*.prev = null;
                    disk.maxFileId = fileIndex;
                } else {
                    // subsequent blocks
                    const newBlock: *DiskBlock = try allocator.create(DiskBlock);
                    newBlock.*.fileId = fileIndex;
                    newBlock.*.size = x;
                    newBlock.*.blockType = BlockType.FILE;
                    newBlock.*.next = null;
                    newBlock.*.prev = disk.tail;
                    disk.tail.?.*.next = newBlock;
                    disk.tail = newBlock;
                    disk.maxFileId = fileIndex;
                }
                fileIndex += 1;
            } else {
                const newBlock: *DiskBlock = try allocator.create(DiskBlock);
                newBlock.*.fileId = -1;
                newBlock.*.size = x;
                newBlock.*.blockType = BlockType.FREE;
                newBlock.*.next = null;
                newBlock.*.prev = disk.tail;
                disk.tail.?.*.next = newBlock;
                disk.tail = newBlock;
            }
            isFile = !isFile;
        }
    }

    return disk;
}

fn findFileById(disk: DiskReference, id: i32) ?*DiskBlock {
    var tmp = disk.head;
    while (tmp != null) : (tmp = tmp.?.*.next) {
        if (tmp.?.*.fileId == id) {
            return tmp;
        }
    }
    return null;
}

fn findFreeBlock(disk: DiskReference, id: i32, requestedSize: u32) ?*DiskBlock {
    var tmp = disk.head;
    while (tmp != null) : (tmp = tmp.?.*.next) {
        const blockType = tmp.?.*.blockType;
        const size = tmp.?.*.size;
        if (tmp.?.*.fileId == id) {
            // don't go past ourselves
            return null;
        }
        if (blockType == BlockType.FREE and size >= requestedSize) {
            return tmp;
        }
    }
    return null;
}

fn coalesceFreeBlocks(disk: DiskReference, allocator: anytype) !void {
    // if we have contiguous free blocks merge them into one block
    // currently this does not update tail
    std.debug.print("Coalescing\n", .{});
    var tmp = disk.head;
    while (tmp != null) {
        const next = tmp.?.*.next;
        if (tmp.?.*.blockType == BlockType.FREE and next != null and next.?.*.blockType == BlockType.FREE) {
            std.debug.print("Coalescing two blocks\n", .{});
            tmp.?.*.size += next.?.*.size;
            tmp.?.*.next = next.?.*.next;
            if (next.?.*.next != null) {
                next.?.*.next.?.*.prev = tmp;
            }
            allocator.destroy(next.?);
        } else {
            tmp = tmp.?.*.next;
        }
    }
}

fn swapTwoBlocks(disk: *DiskReference, block1: *DiskBlock, block2: *DiskBlock) void {
    // Cases:
    // 1. Block1 is the head
    // 2. Block2 is the tail
    // 3. Block1 is the prev of Block2
    // 4. Block2 is the prev of Block1
    const block1Next = block1.*.next;
    const block1Prev = block1.*.prev;
    const block2Next = block2.*.next;
    const block2Prev = block2.*.prev;
    const isHead = block1 == disk.*.head.?;
    const isTail = block2 == disk.*.tail.?;
    if (block2 == block1Next) {
        // the two blocks are adjacent with block1 being first
        if (block1Prev != null) {
            block1Prev.?.*.next.? = block2;
        }
        if (block2Next != null) {
            block2Next.?.*.prev.? = block1;
        }

        block1.*.next = block2Next;
        block2.*.prev = block1Prev;

        block1.*.prev = block2;
        block2.*.next = block1;
    } else if (block1 == block2Next) {
        // already handled above. So just call again.
        return swapTwoBlocks(disk, block2, block1);
    } else {
        // the two blocks are not adjacent
        block1.*.next = block2Next;
        block1.*.prev = block2Prev;
        block2.*.next = block1Next;
        block2.*.prev = block1Prev;
        if (block2Next != null) {
            block2Next.?.*.prev = block1;
        }
        if (block2Prev != null) {
            block2Prev.?.*.next = block1;
        }
        if (block1Next != null) {
            block1Next.?.*.prev = block2;
        }
        if (block1Prev != null) {
            block1Prev.?.*.next = block2;
        }
    }
    if (isHead) {
        disk.*.head = block2;
    }
    if (isTail) {
        disk.*.tail = block1;
    }
}

fn compressDisk(disk: *DiskReference, allocator: anytype) !void {
    // currently this does not update tail.
    var fileId = disk.maxFileId;
    while (fileId > 0) : (fileId -= 1) {
        const fileBlock = findFileById(disk.*, fileId);
        std.debug.print("Attempting to move file {d} of size {d}\n", .{ fileId, fileBlock.?.*.size });
        if (fileId == 3695) {
            printDisk(disk.*, true);
        }
        // technically we should check for null on fileblack,
        // but this is contstrained data.
        const freeBlock = findFreeBlock(disk.*, fileId, fileBlock.?.*.size);
        if (freeBlock != null) {
            swapTwoBlocks(disk, freeBlock.?, fileBlock.?);
            const delta = freeBlock.?.*.size - fileBlock.?.*.size;
            freeBlock.?.*.size -= delta;
            if (delta != 0) {
                // We need to add a freeblock to the end of the moved fileBlock
                const newBlock: *DiskBlock = try allocator.create(DiskBlock);
                newBlock.*.size = delta;
                newBlock.*.blockType = BlockType.FREE;
                newBlock.*.fileId = -1;
                newBlock.*.prev = fileBlock;
                newBlock.*.next = fileBlock.?.*.next;
                fileBlock.?.*.next = newBlock;
                if (newBlock.*.next != null) {
                    newBlock.*.next.?.*.prev = newBlock;
                }
            }
            // now coalesce the free blocks if needed:
            try coalesceFreeBlocks(disk.*, allocator);
        }
        printDisk(disk.*, false);
    }
}

fn u2i(in: usize) i64 {
    return @as(i64, @intCast(in));
}

fn computeCheckSum(disk: DiskReference) i64 {
    var position: i64 = 0;
    var tmp = disk.head;
    var checkSum: i64 = 0;
    while (tmp != null) : (tmp = tmp.?.*.next) {
        const blockType = tmp.?.*.blockType;
        switch (blockType) {
            BlockType.FILE => {
                for (0..tmp.?.*.size) |_| {
                    const id = tmp.?.*.fileId;
                    checkSum += position * id;
                    position += 1;
                }
            },
            BlockType.FREE => {
                position += tmp.?.*.size;
            },
        }
    }
    return checkSum;
}

fn printDisk(disk: DiskReference, force: bool) void {
    if (printTheDisk or force) {
        var tmp = disk.head;
        while (tmp != null) : (tmp = tmp.?.*.next) {
            const id = tmp.?.*.fileId;
            const size = tmp.?.*.size;
            if (tmp.?.*.blockType == BlockType.FILE) {
                for (0..size) |_| {
                    std.debug.print("{d}|", .{id});
                }
            } else {
                for (0..size) |_| {
                    std.debug.print(".", .{});
                }
            }
        }
        std.debug.print("\n", .{});
    }
}

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();
    for (input) |c| {
        std.debug.print("{u}", .{c});
    }
    std.debug.print("\n", .{});
    var disk = try buildExpandedMap(allocator);
    defer {
        var next: ?*DiskBlock = null;
        while (disk.head != null) {
            next = disk.head.?.*.next;
            allocator.destroy(disk.head.?);
            disk.head = next;
        }
    }
    std.debug.print("\n", .{});
    try compressDisk(&disk, allocator);
    const checkSum = computeCheckSum(disk);
    std.debug.print("Checksum: {d}\n", .{checkSum});
}
