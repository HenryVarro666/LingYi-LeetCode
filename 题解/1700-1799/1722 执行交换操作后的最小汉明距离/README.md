# 1722. 执行交换操作后的最小汉明距离

Medium · 难度分 1892 · [力扣原题](https://leetcode.cn/problems/minimize-hamming-distance-after-swap-operations/)

所在刷题路径：灵神题单·常用数据结构、灵神题单·贪心与思维

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 1722 执行交换操作后的最小汉明距离 · 灵茶山艾府.mp4](1722%20执行交换操作后的最小汉明距离%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 1722 执行交换操作后的最小汉明距离 · yiduobo.mp4](1722%20执行交换操作后的最小汉明距离%20·%20yiduobo.mp4) |

## 题目描述

给你两个整数数组 `source` 和 `target` ，长度都是 `n` 。还有一个数组 `allowedSwaps` ，其中每个 `allowedSwaps[i] = [a_i, b_i]` 表示你可以交换数组 `source` 中下标为 `a_i` 和 `b_i`（**下标从 0 开始**）的两个元素。注意，你可以按 **任意** 顺序 **多次** 交换一对特定下标指向的元素。

相同长度的两个数组 `source` 和 `target` 间的 **汉明距离** 是元素不同的下标数量。形式上，其值等于满足 `source[i] != target[i]` （**下标从 0 开始**）的下标 `i`（`0 <= i <= n-1`）的数量。

在对数组 `source` 执行 **任意** 数量的交换操作后，返回 `source` 和 `target` 间的 **最小汉明距离** 。

**示例 1：**

```
输入：source = [1,2,3,4], target = [2,1,4,5], allowedSwaps = [[0,1],[2,3]]
输出：1
解释：source 可以按下述方式转换：
- 交换下标 0 和 1 指向的元素：source = [2,1,3,4]
- 交换下标 2 和 3 指向的元素：source = [2,1,4,3]
source 和 target 间的汉明距离是 1 ，二者有 1 处元素不同，在下标 3 。
```

**示例 2：**

```
输入：source = [1,2,3,4], target = [1,3,2,4], allowedSwaps = []
输出：2
解释：不能对 source 执行交换操作。
source 和 target 间的汉明距离是 2 ，二者有 2 处元素不同，在下标 1 和下标 2 。
```

**示例 3：**

```
输入：source = [5,1,2,4,3], target = [1,5,4,2,3], allowedSwaps = [[0,4],[4,2],[1,3],[1,4]]
输出：0
```

**提示：**

- `n == source.length == target.length`

- `1 <= n <= 10⁵`

- `1 <= source[i], target[i] <= 10⁵`

- `0 <= allowedSwaps.length <= 10⁵`

- `allowedSwaps[i].length == 2`

- `0 <= a_i, b_i <= n - 1`

- `a_i != b_i`

---
[↑ 返回 1700-1799](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
