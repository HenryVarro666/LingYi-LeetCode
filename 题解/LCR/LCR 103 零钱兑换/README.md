# LCR 103. 零钱兑换

Medium · [力扣原题](https://leetcode.cn/problems/gaM7Ch/)

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ LCR 103 零钱兑换 · 灵茶山艾府.mp4](LCR%20103%20零钱兑换%20·%20灵茶山艾府.mp4) |
| yiduobo | — | — |

## 题目描述

给定不同面额的硬币 `coins` 和一个总金额 `amount`。编写一个函数来计算可以凑成总金额所需的最少的硬币个数。如果没有任何一种硬币组合能组成总金额，返回 `-1`。

你可以认为每种硬币的数量是无限的。

**示例 1：**

```

输入：coins = [1, 2, 5], amount = 11
输出：3
解释：11 = 5 + 5 + 1
```

**示例 2：**

```

输入：coins = [2], amount = 3
输出：-1
```

**示例 3：**

```

输入：coins = [1], amount = 0
输出：0
```

**示例 4：**

```

输入：coins = [1], amount = 1
输出：1
```

**示例 5：**

```

输入：coins = [1], amount = 2
输出：2
```

**提示：**

- `1 <= coins.length <= 12`

- `1 <= coins[i] <= 2³¹ - 1`

- `0 <= amount <= 10⁴`

注意：本题与主站 322 题相同： [https://leetcode.cn/problems/coin-change/](https://leetcode.cn/problems/coin-change/)

---
[↑ 返回 LCR](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
