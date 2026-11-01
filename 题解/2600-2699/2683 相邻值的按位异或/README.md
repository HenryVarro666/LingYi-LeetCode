# 2683. 相邻值的按位异或

Medium · 难度分 1518 · [力扣原题](https://leetcode.cn/problems/neighboring-bitwise-xor/)

所在刷题路径：灵神题单·位运算

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 动画（GIF）](2683%20相邻值的按位异或%20·%20灵茶山艾府.gif) · [mp4 文件](2683%20相邻值的按位异或%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 动画（GIF）](2683%20相邻值的按位异或%20·%20yiduobo.gif) · [mp4 文件](2683%20相邻值的按位异或%20·%20yiduobo.mp4) |

## 动画讲解

> 动图会循环播放；想暂停、拖进度条请下载上面表格里的 mp4 文件。

### 灵茶山艾府

![2683 相邻值的按位异或 · 灵茶山艾府](2683%20相邻值的按位异或%20·%20灵茶山艾府.gif)

### yiduobo

![2683 相邻值的按位异或 · yiduobo](2683%20相邻值的按位异或%20·%20yiduobo.gif)


## 题目描述

下标从 **0** 开始、长度为 `n` 的数组 `derived` 是由同样长度为 `n` 的原始 **二进制数组** `original` 通过计算相邻值的 **按位异或（⊕）**派生而来。

特别地，对于范围 `[0, n - 1]` 内的每个下标 `i` ：

- 如果 `i = n - 1` ，那么 `derived[i] = original[i] ⊕ original[0]`

- 否则 `derived[i] = original[i] ⊕ original[i + 1]`

给你一个数组 `derived` ，请判断是否存在一个能够派生得到 `derived` 的 **有效原始二进制数组** `original` 。

如果存在满足要求的原始二进制数组，返回 <em>**true**</em> ；否则，返回 <em>**false**</em> 。

- 二进制数组是仅由 **0** 和 **1** 组成的数组。

**示例 1：**

```
输入：derived = [1,1,0]
输出：true
解释：能够派生得到 [1,1,0] 的有效原始二进制数组是 [0,1,0] ：
derived[0] = original[0] ⊕ original[1] = 0 ⊕ 1 = 1
derived[1] = original[1] ⊕ original[2] = 1 ⊕ 0 = 1
derived[2] = original[2] ⊕ original[0] = 0 ⊕ 0 = 0
```

**示例 2：**

```
输入：derived = [1,1]
输出：true
解释：能够派生得到 [1,1] 的有效原始二进制数组是 [0,1] ：
derived[0] = original[0] ⊕ original[1] = 1
derived[1] = original[1] ⊕ original[0] = 1
```

**示例 3：**

```
输入：derived = [1,0]
输出：false
解释：不存在能够派生得到 [1,0] 的有效原始二进制数组。
```

**提示：**

- `n == derived.length`

- `1 <= n <= 10⁵`

- `derived` 中的值不是 **0** 就是 **1** 。

---
[↑ 返回 2600-2699](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
