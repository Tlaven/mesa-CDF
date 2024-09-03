import numpy as np
import matplotlib.pyplot as plt

def probability_density_function(x, A, a):
    n = (a - 2 * A) / (a - A)
    k = (1 - n) * a**(n - 1)
    print(f'k={k}   n={n}')
    return k / x**n

# 设置参数
A = 10
a = 100

# 生成x值
x = np.linspace(0, a, 500)  # 避免x=0，因为x的指数会导致除零错误

# 计算PDF值
pdf_values = probability_density_function(x, A, a)

# 绘图
plt.figure(figsize=(8, 6))
plt.plot(x, pdf_values, label=f'A={A}, a={a}')
plt.xlabel('x')
plt.ylabel('Probability Density')
plt.title('Probability Density Function')
plt.legend()
plt.grid(True)
plt.show()
