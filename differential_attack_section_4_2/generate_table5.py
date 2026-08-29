import math
from itertools import product


def rol(x, n, bits=32):
    """32-bit rotate left."""
    n %= bits
    return ((x << n) | (x >> (bits - n))) & ((1 << bits) - 1)


# Basic sets
AAA_sets = [
    [0xd, 0x3, 0x5, 0x6, 0x7, 0xb, 0xc],
    [0xc, 0xf, 0x9, 0xa, 0xd, 0xe],
    [0xd, 0x3, 0x5, 0x6, 0x7, 0xb, 0xc],
    [0xd, 0x3, 0x5, 0x6, 0x7, 0xb, 0xc],
    [0xe, 0x3, 0x5, 0x6, 0x7, 0xb, 0xc],
    [0x4, 0x1, 0x6, 0x8, 0x9, 0xb, 0xd],
    [0x4, 0x2, 0x5, 0x8, 0xa, 0xb, 0xe],
    [0xc, 0xf, 0x1, 0x2, 0x5, 0x6],
    [0xd, 0x3, 0x5, 0x6, 0x7, 0xb, 0xc],
    [0x4, 0x1, 0x6, 0x8, 0xa, 0xb, 0xe],
    [0xc, 0xf, 0x1, 0x2, 0x5, 0x6],
    [0xa, 0x1, 0x2, 0x3, 0x7, 0xb, 0xc]
]

BBB_sets = [
    [2, 3, 3, 3, 3, 3, 3],
    [2, 2, 3, 3, 3, 3],
    [2, 3, 3, 3, 3, 3, 3],
    [2, 3, 3, 3, 3, 3, 3],
    [2, 3, 3, 3, 3, 3, 3],
    [2, 3, 3, 3, 3, 3, 3],
    [2, 3, 3, 3, 3, 3, 3],
    [2, 2, 3, 3, 3, 3],
    [2, 3, 3, 3, 3, 3, 3],
    [2, 3, 3, 3, 3, 3, 3],
    [2, 2, 3, 3, 3, 3],
    [2, 3, 3, 3, 3, 3, 3]
]


# Subsets
AA_sets = [
    [0xd], [0xc, 0xf], [0xd], [0xd], [0xe], [0x4],
    [0x4], [0xc, 0xf], [0xd], [0x4], [0xc, 0xf], [0xa]
]

BB_sets = [
    [2], [2, 2], [2], [2], [2], [2],
    [2], [2, 2], [2], [2], [2, 2], [2]
]


MASK = 0xFFFFFFFF
COUNT = 100.0
ANSWER_IN = 0
ANSWER_OUT = 0

LIMIT = (3 * 3) + (2 * 8)  # 25

HM = [
    1, 12, 12, 10,
    6, 12, 12, 10,
    10, 8, 8, 12,
    10, 8, 8, 4
]


# Use a set to record visited configurations and avoid redundant computations
# when different choices of i0, i1, ... generate the same A_sets structure.
visited_configs = set()


for i0 in range(12):

    # for i1 in range(i0 + 1, 12):
    #     for i2 in range(i1 + 1, 12):
    #         for i3 in range(i2 + 1, 12):
    #             for i4 in range(i3 + 1, 12):

    print(i0)

    # 1. Dynamically construct the 12 input groups
    current_loops = []

    for i in range(12):

        if i == i0:
            a_src, b_src = AAA_sets[i], BBB_sets[i]
        else:
            a_src, b_src = AA_sets[i], BB_sets[i]

        # Pack (value, corresponding B value) into tuples
        # to completely eliminate the need for .index().
        current_loops.append(list(zip(a_src, b_src)))

    # Convert to tuples and store them in a set for deduplication.
    # This prevents different choices of i0, i1, ... from generating
    # exactly the same input configuration.
    config_signature = tuple(
        tuple(item) for item in current_loops
    )

    if config_signature in visited_configs:
        continue

    visited_configs.add(config_signature)

    # 2. Expand all combinations of the 12 input groups
    for (
        item0, item1, item2, item3, item4, item5,
        item6, item7, item8, item9, item10, item11
    ) in product(*current_loops):

        # Calculate the total B-weight if needed.
        #
        # P = (
        #     item0[1] + item1[1] + item2[1] +
        #     item3[1] + item4[1] + item5[1] +
        #     item6[1] + item7[1] + item8[1] +
        #     item9[1] + item10[1] + item11[1]
        # )
        #
        # if P > LIMIT:
        #     continue

        # Extract the actual A values
        A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11 = (
            item0[0], item1[0], item2[0], item3[0], item4[0], item5[0],
            item6[0], item7[0], item8[0], item9[0], item10[0], item11[0]
        )

        # Preserve the original bit concatenation order
        IN = (
            (A11 << 124) |
            (A10 << 108) |
            (A9 << 96) |
            (A8 << 88) |
            (A7 << 76) |
            (A6 << 64) |
            (A5 << 48) |
            (A4 << 44) |
            (A3 << 32) |
            (A2 << 20) |
            (A1 << 8) |
            (A0 << 0)
        )

        # -------------------------------------------------
        # Convert 128-bit state to bitslice representation
        # -------------------------------------------------
        X0 = X1 = X2 = X3 = 0

        for i in range(32):

            nibble = (IN >> (124 - 4 * i)) & 0xF

            X0 |= ((nibble >> 0) & 1) << (31 - i)
            X1 |= ((nibble >> 1) & 1) << (31 - i)
            X2 |= ((nibble >> 2) & 1) << (31 - i)
            X3 |= ((nibble >> 3) & 1) << (31 - i)

        # -------------------------------------------------
        # Serpent inverse linear transformation
        # -------------------------------------------------
        X2 = rol(X2, 10)  # 32 - 22
        X0 = rol(X0, 27)  # 32 - 5

        X2 = (X2 ^ X3 ^ ((X1 << 7) & MASK)) & MASK
        X0 = (X0 ^ X1 ^ X3) & MASK

        X3 = rol(X3, 25)  # 32 - 7
        X1 = rol(X1, 31)  # 32 - 1

        X3 = (X3 ^ X2 ^ ((X0 << 3) & MASK)) & MASK
        X1 = (X1 ^ X0 ^ X2) & MASK

        X2 = rol(X2, 29)  # 32 - 3
        X0 = rol(X0, 19)  # 32 - 13

        # -------------------------------------------------
        # Convert bitslice representation back to
        # a 128-bit state
        # -------------------------------------------------
        OUT = 0
        result = 1

        for i in range(32):

            nibble = (
                (((X0 >> (31 - i)) & 1) << 0)
                | (((X1 >> (31 - i)) & 1) << 1)
                | (((X2 >> (31 - i)) & 1) << 2)
                | (((X3 >> (31 - i)) & 1) << 3)
            )

            result *= HM[nibble]
            OUT |= nibble << (124 - 4 * i)

        # Compare and record the smaller value
        log2_res = math.log2(result)

        if COUNT > log2_res:

            COUNT = log2_res
            ANSWER_IN = IN
            ANSWER_OUT = OUT

            print(f"COUNT = {COUNT}")
            print(f"ANSWER_IN = {ANSWER_IN:032x}")
            print(f"ANSWER_OUT = {ANSWER_OUT:032x}")

            print(
                f"B_weights = "
                f"{[item[1] for item in (item0, item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11)]}"
            )


print("\n--- Final Result ---")
print(f"COUNT = {COUNT}")
print(f"ANSWER_IN = {ANSWER_IN:032x}")
print(f"ANSWER_OUT = {ANSWER_OUT:032x}")