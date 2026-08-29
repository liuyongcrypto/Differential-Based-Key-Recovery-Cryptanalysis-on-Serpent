from math import log2

# Basic parameter settings
rb = 76
rf = 13.007

# Array B (20 elements in total)
B = [
    1,
    4,
    4 * 6,
    4 * 6 * 8,
    4 * 6 * (8**2),
    4 * 6 * (8**3),
    4 * 6 * (8**4),
    4 * 6 * (8**3) * (10**1),
    4 * 6 * (8**3) * (10**2),
    4 * 6 * (8**3) * (10**3),
    4 * 6 * (8**3) * (10**4),
    4 * 6 * (8**3) * (10**5),
    4 * 6 * (8**3) * (10**6),
    4 * 6 * (8**3) * (10**6) * (12**1),
    4 * 6 * (8**3) * (10**6) * (12**2),
    4 * 6 * (8**3) * (10**6) * (12**3),
    4 * 6 * (8**3) * (10**6) * (12**4),
    4 * 6 * (8**3) * (10**6) * (12**5),
    4 * 6 * (8**3) * (10**6) * (12**6),
    4 * 6 * (8**3) * (10**6) * (12**7),
]

# Array F (6 elements in total)
F = [
    1,
    4,
    4 * 10,
    4 * 10 * 11,
    4 * 10 * 11 * 11,
    4 * 10 * 11 * 11 * 11
]

RF = [
    1,
    4,
    4 * 6,
    4 * 6 * 7,
    4 * 6 * 7 * 7,
    4 * 6 * 7 * 7 * 7
]

# Precompute log2(7), approximately 2.80735
LOG2_7 = log2(7)

min_complexity = float("inf")
best_params = None

# Enumerate all combinations
for b in range(20):  # Iterate over all indices of B: 0 ~ 19
    for f in range(6):  # Iterate over all indices of F: 0 ~ 5
        rb_0 = 4 * b
        rb_1 = rb - rb_0
        rf_0 = log2(RF[f])
        rf_1 = rf - rf_0

        log2_Bb = log2(B[b])
        log2_Ff = log2(F[f])

        # p = 60.3
        p = 58.15

        # Calculate the log2 complexities of the three terms
        T1 = 66 + p + log2_Bb + log2_Ff

        T2 = min(
            141 + p + log2_Bb + log2_Ff - rb_0,
            16.007 + 2 * p + log2_Bb + log2_Ff - rf_0
        )

        T3 = (
            52.014
            + 2 * p
            + log2_Bb
            + log2_Ff
            - 2 * rb_0
            - 2 * rf_0
        )

        # T1 = 124.15 + log2_Bb + log2_Ff
        # T2 = min(251.15 + log2_Bb + log2_Ff - rb_0,
        #          139.0 + log2_Bb + log2_Ff - rf_0)
        # T3 = 183.3 + log2_Bb + log2_Ff - 2 * rb_0 - 2 * rf_0

        print(
            log2_Bb,
            log2_Ff,
            rb_0,
            rf_0,
            T1,
            T2,
            T3
        )

        # Key correction:
        # 7 * 2^T1 is represented as log2(7) + T1 in the logarithmic domain
        comp_T1 = LOG2_7 + T1
        comp_T2 = LOG2_7 + T2
        comp_T3 = T3

        # Compute the total complexity in the logarithmic domain
        current_min = log2(
            2**comp_T1 + 2**comp_T2 + 2**comp_T3
        )

        print(
            f"b={b:2d} (rb_0={rb_0:2d}), "
            f"f={f:1d} (rf_0={rf_0:.2f}) ->\n"
            f"  Complexity (log2): 2^{current_min:.2f}\n"
            f"  T1 complexity (log2): 2^{comp_T1:.2f}\n"
            f"  T2 complexity (log2): 2^{comp_T2:.2f}\n"
            f"  T3 complexity (log2): 2^{comp_T3:.2f}"
        )

        # Record the globally optimal solution
        if current_min < min_complexity:
            min_complexity = current_min
            best_params = (b, f, rb_0, rf_0)

print("\n" + "=" * 50)

print(
    f"Global minimum complexity: 2^{min_complexity:.2f} "
    f"(achieved at b={best_params[0]}, "
    f"f={best_params[1]}, "
    f"rb_0={best_params[2]}, "
    f"rf_0={best_params[3]:.2f})"
)

print(log2(4 * 6 * 8))
print(log2(4 * 10 * 11 * 11))