import matplotlib.pyplot as plt
import random

def CDF(A, a, u):
    """
    计算给定均匀随机数u的CDF逆函数值。
    
    :param A: 参数A
    :param a: 参数a
    :param u: 均匀分布随机数，范围在[0,1]
    :return: 对应的CDF逆函数值
    """
    n = (a - 2 * A) / (a - A)
    k = (1 - n) * a**(n - 1)
    return (u * (1 - n) / k)**(1 / (1 - n))

# 设置参数
A = 10
a = 100

# 生成几个均匀分布的随机数
random_uniforms = [random.uniform(0, 1) for _ in range(100)]

# 计算对应的CDF逆函数值
random_values = [CDF(A, a, u) for u in random_uniforms]

# 输出频率分布图
plt.hist(random_values, bins=20, density=True)
plt.xlabel('Random values')
plt.ylabel('Frequency')
plt.title('Frequency distribution of random values')
plt.show()

# 打印均值和方差
print('Mean:', sum(random_values) / len(random_values))
print('Variance:', sum([(x - sum(random_values) / len(random_values))**2 for x in random_values]) / len(random_values))