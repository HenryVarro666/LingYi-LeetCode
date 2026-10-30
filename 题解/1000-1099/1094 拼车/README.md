# 1094. 拼车

Medium · 难度分 1441 · [力扣原题](https://leetcode.cn/problems/car-pooling/)

所在刷题路径：labuladong、灵神题单·常用数据结构

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 1094 拼车 · 灵茶山艾府.mp4](1094%20拼车%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 1094 拼车 · yiduobo.mp4](1094%20拼车%20·%20yiduobo.mp4) |

## 题目描述

车上最初有 `capacity` 个空座位。车 **只能** 向一个方向行驶（也就是说，**不允许掉头或改变方向**）

给定整数 `capacity` 和一个数组 `trips` ,  `trips[i] = [numPassengers_i, from_i, to_i]` 表示第 `i` 次旅行有 `numPassengers_i` 乘客，接他们和放他们的位置分别是 `from_i` 和 `to_i` 。这些位置是从汽车的初始位置向东的公里数。

乘客在接上新乘客之前会被放下。在路线的每个点，车内乘客总数不得超过 `capacity`。

当且仅当你可以在所有给定的行程中接送所有乘客时，返回 `true`，否则请返回 `false`。

**示例 1：**

```

输入：trips = [[2,1,5],[3,3,7]], capacity = 4
输出：false
```

**示例 2：**

```

输入：trips = [[2,1,5],[3,3,7]], capacity = 5
输出：true
```

**提示：**

- `1 <= trips.length <= 1000`

- `trips[i].length == 3`

- `1 <= numPassengers_i <= 100`

- `0 <= from_i < to_i <= 1000`

- `1 <= capacity <= 10⁵`

---
[↑ 返回 1000-1099](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
