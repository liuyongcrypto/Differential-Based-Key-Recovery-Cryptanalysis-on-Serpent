import math
from itertools import product

def rol(x, n, bits=32):
    """32-bit rotate left"""
    n %= bits
    return ((x << n) | (x >> (bits - n))) & ((1 << bits) - 1)

# Base sets
AAA_sets = [
    [0x3, 0x6, 0x9, 0xa, 0xc, 0xf],
    [0x7, 0x3, 0x6, 0x9, 0xa, 0xb, 0xd],
    [0x3, 0x6, 0x9, 0xa, 0xc, 0xf],
    [0x5, 0x7, 0x9, 0xb, 0xc, 0xd, 0xe, 0xf],
    [0xc, 0xe, 0x3, 0x5, 0xb, 0xd]
]

BBB_sets = [
    [2, 2, 3, 3, 3, 3],
    [2, 3, 3, 3, 3, 3, 3],
    [2, 2, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3],
    [2, 2, 3, 3, 3, 3]
]

# Subsets
AA_sets = [
    [0x3, 0x6],
    [0x7],
    [0x3, 0x6],
    [0x5, 0x7, 0x9, 0xb, 0xc, 0xd, 0xe, 0xf],
    [0xc, 0xe]
]

BB_sets = [
    [2, 2],
    [2],
    [2, 2],
    [3, 3, 3, 3, 3, 3, 3, 3],
    [2, 2]
]

MASK = 0xFFFFFFFF
COUNT = 100.0
ANSWER_IN = 0
ANSWER_OUT = 0
A = 1000
LIMIT = (3 * 3) + (2 * 8)  # 25
# HM = [1, 11, 10, 11, 4, 10, 10, 10, 11, 12, 11, 10, 10, 4, 10, 10]
HM = [1, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16]
HM_m = [1,7,6,7,4,7,6,7,7,8,7,6,7,4,7,6]
COUNT_m = 0

# Use a set to store combinations that have already been processed to avoid redundant work when different i0, i1 selections generate duplicate A_sets structures
visited_configs = set()

for i0 in range(5):
    for i1 in range(i0+1,5):
        for i2 in range(i1+1,5):
            # for i3 in range(i2+1,5):
                # for i4 in range(i3+1,5):
            print(i0)
            # 1. Dynamically construct the 12 groups of inputs for the current iteration
            current_loops = []
            for i in range(5):
                if i == i0 or i == i1 or i== i2:
                    a_src, b_src = AAA_sets[i], BBB_sets[i]
                else:
                    a_src, b_src = AA_sets[i], BB_sets[i]

                # Key optimization: pack (value, corresponding B value) into tuples to completely eliminate .index()
                current_loops.append(list(zip(a_src, b_src)))

            # Convert to a tuple and store it in the set to remove duplicate configurations, preventing different i0, i1 combinations from generating exactly the same input combinations
            config_signature = tuple(tuple(item) for item in current_loops)
            if config_signature in visited_configs:
                continue
            visited_configs.add(config_signature)


            # 2. Expand the 12-level product combinations
            for item0, item1, item2, item3, item4 in product(*current_loops):


                # Directly obtain the value of P by unpacking
                # P = (item0[1] + item1[1] + item2[1] + item3[1] + item4[1] + item5[1] +
                #      item6[1] + item7[1] + item8[1] + item9[1] + item10[1] + item11[1])
                #
                # if P > LIMIT:
                #     continue

                # Obtain the actual A cipher bit values
                A0, A1, A2, A3, A4 = (
                    item0[0], item1[0], item2[0], item3[0], item4[0]
                )

                # Note: preserve the bit concatenation order in the original code
                IN = (
                        (A4 << 124) |
                        (A3 << 108) | (A2 << 40) | (A1 << 20) | (A0 << 16)
                )
                # IN = 0xc000e000000000000000030000730000
                # -----------------------------
                # Convert 128-bit state -> bitslice
                # -----------------------------
                X0 = X1 = X2 = X3 = 0
                for i in range(32):
                    nibble = (IN >> (124 - 4 * i)) & 0xF
                    X0 |= ((nibble >> 0) & 1) << (31 - i)
                    X1 |= ((nibble >> 1) & 1) << (31 - i)
                    X2 |= ((nibble >> 2) & 1) << (31 - i)
                    X3 |= ((nibble >> 3) & 1) << (31 - i)

                # -----------------------------
                # Serpent INV_Linear Transformation
                # -----------------------------
                X0 = rol(X0, 13)
                X2 = rol(X2, 3)

                X1 = (X1 ^ X0 ^ X2) & MASK
                X3 = (X3 ^ X2 ^ ((X0 << 3) & MASK)) & MASK

                X1 = rol(X1, 1)
                X3 = rol(X3, 7)

                X0 = (X0 ^ X1 ^ X3) & MASK
                X2 = (X2 ^ X3 ^ ((X1 << 7) & MASK)) & MASK

                X0 = rol(X0, 5)
                X2 = rol(X2, 22)

                # -----------------------------
                # Convert bitslice -> 128-bit state
                # -----------------------------
                OUT = 0
                result = 1
                result_m = 1
                for i in range(32):
                    nibble = (
                            (((X0 >> (31 - i)) & 1) << 0)
                            | (((X1 >> (31 - i)) & 1) << 1)
                            | (((X2 >> (31 - i)) & 1) << 2)
                            | (((X3 >> (31 - i)) & 1) << 3)
                    )
                    result *= HM[nibble]
                    result_m *= HM_m[nibble]
                    OUT |= nibble << (124 - 4 * i)

                # Compare and record the smaller value
                log2_res = math.log2(result)
                log2_res_m = math.log2(result_m)
                M = 0
                if (log2_res_m - 1 < log2_res - 5):
                    M = log2_res - 5
                else:
                    M = log2_res_m - 1

                if (A > M):
                    A = M

                    COUNT = log2_res
                    COUNT_m = log2_res_m
                    ANSWER_IN = IN
                    ANSWER_OUT = OUT
                    print(f"COUNT = {COUNT}")
                    print(f"COUNT_m = {COUNT_m}")
                    print(f"ANSWER_IN = {ANSWER_IN:032x}")
                    print(f"ANSWER_OUT = {ANSWER_OUT:032x}")
                    print(f"B_weights={[item[1] for item in (item0, item1, item2, item3, item4)]}")

print("\n--- Final Result ---")
print(f"COUNT = {COUNT}")
print(f"COUNT_m = {COUNT_m}")
print(f"ANSWER_IN = {ANSWER_IN:032x}")
print(f"ANSWER_OUT = {ANSWER_OUT:032x}")