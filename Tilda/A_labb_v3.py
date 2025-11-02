def bit_length(x):
    """Calculate the minimum number of bits needed to represent a non-negative integer x."""
    if x == 0:
        return 1
    return x.bit_length()


def calculate_cost(start, end, mode, c, x):
    """Calculate the cost of encoding a block from start to end using the given mode."""
    block_size = end - start
    if mode == 1:
        # Mode 1: Use the maximum value in the block
        max_value = max(x[start:end])
        bit_size = bit_length(max_value)
        print(f"[Mode 1] Block: {x[start:end]}, Max Value: {max_value}, Bit Size: {bit_size}")
    elif mode == 2:
        # Mode 2: Use the maximum absolute difference
        max_diff = max(abs(x[i] - x[i - 1]) for i in range(start + 1, end))
        bit_size = bit_length(max_diff)
        print(f"[Mode 2] Block: {x[start:end]}, Max Diff: {max_diff}, Bit Size: {bit_size}")
    else:
        raise ValueError("Invalid mode")
    
    # Total cost = c + s * k
    total_cost = c + bit_size * block_size
    print(f"Total Cost for Mode {mode}: {total_cost}, Block Size: {block_size}")
    return total_cost, bit_size


def compression(N, c, x):
    # Initialize dp array to store the minimum cost to compress the list up to each element
    dp = [float('inf')] * (N + 1)
    dp[0] = 0

    # Track the block information for debugging purposes
    block_info = [{} for _ in range(N + 1)]

    # Iterate over each endpoint i
    for i in range(1, N + 1):
        print(f"\n[DP Update] Processing endpoint {i}:")
        # Consider all possible starting points j for the block ending at i-1
        for j in range(max(0, i - 30), i):  # Maximum block size is 30 (as per constraints)
            # Mode 1: Direct encoding
            cost_mode_1, bit_size_1 = calculate_cost(j, i, mode=1, c=c, x=x)
            if dp[j] + cost_mode_1 < dp[i]:
                dp[i] = dp[j] + cost_mode_1
                block_info[i] = {'mode': 1, 'start': j, 'end': i - 1, 'bit_size': bit_size_1}
                print(f"  [Update] Mode 1 chosen for block [{j}:{i-1}] with cost {dp[i]}")

            # Mode 2: Difference encoding (only valid if the block has at least 2 elements)
            if i - j > 1:
                cost_mode_2, bit_size_2 = calculate_cost(j, i, mode=2, c=c, x=x)
                if dp[j] + cost_mode_2 < dp[i]:
                    dp[i] = dp[j] + cost_mode_2
                    block_info[i] = {'mode': 2, 'start': j, 'end': i - 1, 'bit_size': bit_size_2}
                    print(f"  [Update] Mode 2 chosen for block [{j}:{i-1}] with cost {dp[i]}")

    # Debugging output for block information
    print("\n[Block Information]")
    for i in range(1, N + 1):
        if block_info[i]:
            print(f"Block ending at {i}: {block_info[i]}")

    # Final DP Table
    print("\n[Final DP Table]")
    for i in range(N + 1):
        print(f"dp[{i}] = {dp[i]}")

    # Backtrack to find block partitions
    print("\n[Block Partitions]")
    partitions = []
    idx = N
    while idx > 0:
        info = block_info[idx]
        if not info:
            break
        partitions.append((info['start'], info['end'], info['mode'], info['bit_size']))
        idx = info['start']
    
    # Reverse partitions to display in logical order
    partitions.reverse()
    for partition in partitions:
        start, end, mode, bit_size = partition
        print(f"Block: {x[start:end+1]} | Mode: {mode} | Bit Size: {bit_size}")
    
    return dp[N]


if __name__ == "__main__":
    try:
        # Input
        print("Enter the value of N (number of integers) and c (header cost):")
        N, c = map(int, input().strip().split())

        print(f"Enter the {N} integers in the list:")
        x = list(map(int, input().strip().split()))

        if len(x) != N:
            print("Error: The number of elements in the list x does not match the value of N.")
        else:
            # Output
            print("\nMinimum bits required:", compression(N, c, x))
    except ValueError as e:
        print("Input Error: Please make sure you enter the correct values.")
        print(f"Debug: {e}")

#1 2 3 4 5 3 1
#0 99 3 2 2 2 2 2
