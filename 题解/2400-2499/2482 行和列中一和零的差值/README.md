# 2482. 行和列中一和零的差值

Medium · [力扣原题](https://leetcode.cn/problems/difference-between-ones-and-zeros-in-row-and-column/)

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 动画（GIF）](2482%20行和列中一和零的差值%20·%20灵茶山艾府.gif) · [mp4 文件](2482%20行和列中一和零的差值%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 动画（GIF）](2482%20行和列中一和零的差值%20·%20yiduobo.gif) · [mp4 文件](2482%20行和列中一和零的差值%20·%20yiduobo.mp4) |

## 动画讲解

> 动图会循环播放；想暂停、拖进度条请下载上面表格里的 mp4 文件。

### 灵茶山艾府

![2482 行和列中一和零的差值 · 灵茶山艾府](2482%20行和列中一和零的差值%20·%20灵茶山艾府.gif)

### yiduobo

![2482 行和列中一和零的差值 · yiduobo](2482%20行和列中一和零的差值%20·%20yiduobo.gif)


## 题目描述

给你一个下标从 **0** 开始的 `m x n` 二进制矩阵 `grid` 。

我们按照如下过程，定义一个下标从 **0** 开始的 `m x n` 差值矩阵 `diff` ：

- 令第 `i` 行一的数目为 `onesRow_i` 。

- 令第 `j` 列一的数目为 `onesCol_j`<sub> </sub>。

- 令第 `i` 行零的数目为 `zerosRow_i` 。

- 令第 `j` 列零的数目为 `zerosCol_j` 。

- `diff[i][j] = onesRow_i + onesCol_j - zerosRow_i - zerosCol_j`

请你返回差值矩阵 `diff` 。

**示例 1：**

![](../../_assets/灵茶山艾府/692002e4c3b84489.png)

```
输入：grid = [[0,1,1],[1,0,1],[0,0,1]]
输出：[[0,0,4],[0,0,4],[-2,-2,2]]
解释：
- diff[0][0] = onesRow₀ + onesCol₀ - zerosRow₀ - zerosCol₀ = 2 + 1 - 1 - 2 = 0
- diff[0][1] = onesRow₀ + onesCol₁ - zerosRow₀ - zerosCol₁ = 2 + 1 - 1 - 2 = 0
- diff[0][2] = onesRow₀ + onesCol₂ - zerosRow₀ - zerosCol₂ = 2 + 3 - 1 - 0 = 4
- diff[1][0] = onesRow₁ + onesCol₀ - zerosRow₁ - zerosCol₀ = 2 + 1 - 1 - 2 = 0
- diff[1][1] = onesRow₁ + onesCol₁ - zerosRow₁ - zerosCol₁ = 2 + 1 - 1 - 2 = 0
- diff[1][2] = onesRow₁ + onesCol₂ - zerosRow₁ - zerosCol₂ = 2 + 3 - 1 - 0 = 4
- diff[2][0] = onesRow₂ + onesCol₀ - zerosRow₂ - zerosCol₀ = 1 + 1 - 2 - 2 = -2
- diff[2][1] = onesRow₂ + onesCol₁ - zerosRow₂ - zerosCol₁ = 1 + 1 - 2 - 2 = -2
- diff[2][2] = onesRow₂ + onesCol₂ - zerosRow₂ - zerosCol₂ = 1 + 3 - 2 - 0 = 2
```

**示例 2：**

![](../../_assets/灵茶山艾府/b552706933f9e8cc.png)

```
输入：grid = [[1,1,1],[1,1,1]]
输出：[[5,5,5],[5,5,5]]
解释：
- diff[0][0] = onesRow₀ + onesCol₀ - zerosRow₀ - zerosCol₀ = 3 + 2 - 0 - 0 = 5
- diff[0][1] = onesRow₀ + onesCol₁ - zerosRow₀ - zerosCol₁ = 3 + 2 - 0 - 0 = 5
- diff[0][2] = onesRow₀ + onesCol₂ - zerosRow₀ - zerosCol₂ = 3 + 2 - 0 - 0 = 5
- diff[1][0] = onesRow₁ + onesCol₀ - zerosRow₁ - zerosCol₀ = 3 + 2 - 0 - 0 = 5
- diff[1][1] = onesRow₁ + onesCol₁ - zerosRow₁ - zerosCol₁ = 3 + 2 - 0 - 0 = 5
- diff[1][2] = onesRow₁ + onesCol₂ - zerosRow₁ - zerosCol₂ = 3 + 2 - 0 - 0 = 5
```

**提示：**

- `m == grid.length`

- `n == grid[i].length`

- `1 <= m, n <= 10⁵`

- `1 <= m * n <= 10⁵`

- `grid[i][j]` 要么是 `0` ，要么是 `1` 。

---
[↑ 返回 2400-2499](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
