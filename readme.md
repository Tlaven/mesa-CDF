# 红包分配模拟

[English](./README-en.md) | 简体中文

这个项目使用基于代理的建模技术来模拟一群人之间的“红包”分配过程，查看一个人在不同的抢夺位置上获得的红包金额的分布，并模拟不同抢夺位置的红包分配结果。该模拟是基于 [Mesa](https://mesa.readthedocs.io/en/stable/) 框架构建的，这使得创建和可视化基于代理的模型变得模块化和简单。

## 快速开始
### 环境依赖

在运行项目之前，您需要安装Python和Poetry（用于管理虚拟环境和依赖项）。可以通过以下命令安装Poetry：

```bash
pip install poetry
```

### 安装依赖和设置虚拟环境

克隆项目后，您可以使用以下命令创建虚拟环境并安装依赖：

```bash
# 克隆项目
git clone <your-repo-url>

# 进入项目目录
cd <your-repo-directory>

# 使用Poetry安装依赖并创建虚拟环境
poetry install
```

## 测试的概率分布
![测试的概率分布情况](./images/PDF_test.png)

## 测试的随机数生成分布
![测试的随机数生成分布情况](./images/CDF_test.png)