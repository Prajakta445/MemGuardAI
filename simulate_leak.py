
import time

# Controlled memory-growth test
memory_blocks = []
BLOCK_SIZE_MB = 5
MAX_BLOCKS = 20

print("MemGuard AI - Memory Growth Test")
print("Allocating memory gradually.")
print("Press Ctrl+C to stop.\n")

try:
    for count in range(1, MAX_BLOCKS + 1):
        block = bytearray(BLOCK_SIZE_MB * 1024 * 1024)

        # Touch each memory page so the allocation is backed by RAM.
        for offset in range(0, len(block), 4096):
            block[offset] = 1

        memory_blocks.append(block)

        allocated_mb = count * BLOCK_SIZE_MB

        print(
            f"Step {count}/{MAX_BLOCKS}: "
            f"Allocated approximately {allocated_mb} MB"
        )

        time.sleep(2)

    print("\nTest completed.")
    print("Allocated approximately 100 MB.")
    input("Press Enter to release memory and exit...")

except KeyboardInterrupt:
    print("\nTest stopped.")

finally:
    memory_blocks.clear()
    print("Test memory released.")
