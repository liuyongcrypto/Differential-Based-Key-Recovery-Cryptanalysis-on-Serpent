import numpy as np
from scipy.stats import norm
import math

def calculate_N(a, Ps, n, elp):
    """
    计算图片中的 N 值
    """
    # 1. 计算 ELP (Expected Linear Probability)
    # 根据图片公式: ELP = (p_u * p_r * (q * q_l)^2)^-2


    # 2. 定义正态分布反函数 phi^{-1}
    # norm.ppf 是 scipy 中对应的标准正态分布分位数函数
    phi_inv = norm.ppf

    # 3. 计算分子部分
    term1 = phi_inv(1 - 2 ** (-a - 1)) ** 2
    term2 = phi_inv(1 - Ps / 2) ** 2
    numerator = term1 - term2

    # 4. 计算分母部分
    denominator = (elp - 2 ** (-n)) * (phi_inv(1 - Ps / 2) ** 2)

    # 5. 计算 N
    N = numerator / denominator

    return N, elp


# --- 示例参数设置 (请根据你的实际论文/项目数据替换以下数值) ---
# params = {
#     "a": 2,  # Advantage
#     "Ps": 0.55,  # Success probability
#     "n": 128,  # 相关位宽或块大小
#     "elp": 2**(-118.5),  # 示例概率
# }

params = {
    "a": 4,  # Advantage
    "Ps": 0.55,  # Success probability
    "n": 128,  # 相关位宽或块大小
    "elp": 2**(-105.9),  # 示例概率
}

try:
    result_N, calc_elp = calculate_N(**params)

    # 计算以 2 为底的指数
    # 如果值小于等于 0，log 运算会报错，所以加个判断
    log2_elp = math.log2(calc_elp) if calc_elp > 0 else float('-inf')
    log2_N = math.log2(result_N) if result_N > 0 else float('-inf')

    print(f"计算结果 (2进制对数形式):")
    print(f"---" * 10)
    print(f"ELP: {calc_elp:.4e} (约等于 2^{log2_elp:.2f})")
    print(f"N  : {result_N:.4e} (约等于 2^{log2_N:.2f})")

except Exception as e:
    print(f"计算出错: {e}")



exponent = math.log2((6**5) * (1/19) * (5/32))

print(f"Result: 2^{exponent:.2f}")