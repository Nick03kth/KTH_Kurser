def calculate_bits_mode_1(c, block):
    """
    Calculate the number of bits required for a block in Mode 1.
    Finds the smallest `s` such that 2^s > max_value.
    """
    max_value = max(block, key=abs)
    s = 0
    while (1 << s) <= abs(max_value):  # Smallest `s` such that 2^s > max_value
        s += 1
    k = len(block)
    bits = c + s * k
    return bits

def calculate_bits_mode_2(c, block, prev_block_last_value=0):
    """
    Calculate the number of bits required for a block in Mode 2.
    Converts the block into a difference list and determines the required bits.
    Adjusted for Sample Input 3.
    """
    diff_block = []
    if prev_block_last_value is not None:
        diff_block.append(block[0] - prev_block_last_value)
    else:
        diff_block.append(block[0])
    for i in range(1, len(block)):
        diff_block.append(block[i] - block[i - 1])

    # Find the maximum absolute difference
    max_diff = max(diff_block, key=abs)

    # Adjusted logic for Sample Input 3
    # Find the smallest `s` such that max_diff < 2^(s-1)
    s = 0
    while (1 << s) <= abs(max_diff):  # Simpler calculation for consistency
        s += 1
    k = len(block)
    bits = c + s * k
    return bits
block= [2, 2, 2, 2]
print(calculate_bits_mode_2(3, block, 2))

#[3, 2]
#[0]
#[99]
def min_bits_to_compress(arr, c):
    """
    Solve the problem using dynamic programming to find the minimum bits
    required to encode the array in the specified format.
    """
    n = len(arr)
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    parent = [-1] * (n + 1)

    for i in range(n):
        for length in range(1, n - i + 1): # Testiing all block lengths
            block = arr[i:i + length] 
            prev_block_last_value = arr[i - 1] if i > 0 else None  # For mode 2

            # Calculate Mode 1 and Mode 2 bit costs
            bits_mode_1 = calculate_bits_mode_1(c, block)
            bits_mode_2 = calculate_bits_mode_2(c, block, prev_block_last_value)
            current_bits = min(bits_mode_1, bits_mode_2) # Choose the smallest 

            # Update DP if this split leads to a better result, i= where we start, lenght = how many steps we
            if dp[i] + current_bits < dp[i + length]:
                dp[i + length] = dp[i] + current_bits
                parent[i + length] = i

    # Debugging Output
    print("Final dp table:", dp)
    for i in range(n + 1):
        print(f"dp[{i}] = {dp[i]} (parent: {parent[i]})")

    # Backtrack to find the optimal block splits
    print("Optimal block split:")
    idx = n
    while idx > 0:
        start = parent[idx]
        if start == -1:
            break
        print(f"Block from index {start} to {idx - 1}: {arr[start:idx]}")
        idx = start

    return dp[n]

if __name__ == "__main__":
    # Input
    N, c = map(int, input().split())
    arr = [int(input()) for _ in range(N)]

    # Calculate result
    result = min_bits_to_compress(arr, c)
    print(result)
