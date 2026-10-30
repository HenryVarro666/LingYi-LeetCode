# 3213. 最小代价构造字符串

Hard · 难度分 2171 · [力扣原题](https://leetcode.cn/problems/construct-string-with-minimum-cost/)

所在刷题路径：灵神题单·动态规划、灵神题单·字符串

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 3213 最小代价构造字符串 · 灵茶山艾府.mp4](3213%20最小代价构造字符串%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 3213 最小代价构造字符串 · yiduobo.mp4](3213%20最小代价构造字符串%20·%20yiduobo.mp4) |

## 题目描述

给你一个字符串 `target`、一个字符串数组 `words` 以及一个整数数组 `costs`，这两个数组长度相同。

设想一个空字符串 `s`。

你可以执行以下操作任意次数（包括 **零** 次）：

- 选择一个在范围  `[0, words.length - 1]` 的索引 `i`。

- 将 `words[i]` 追加到 `s`。

- 该操作的成本是 `costs[i]`。

返回使 `s` 等于 `target` 的 **最小** 成本。如果不可能，返回 `-1`。

**示例 1：**

**输入：** `target = "abcdef", words = ["abdef","abc","d","def","ef"], costs = [100,1,1,10,5]`

**输出：** `7`

**解释：**

- 选择索引 1 并以成本 1 将 `"abc"` 追加到 `s`，得到 `s = "abc"`。

- 选择索引 2 并以成本 1 将 `"d"` 追加到 `s`，得到 `s = "abcd"`。

- 选择索引 4 并以成本 5 将 `"ef"` 追加到 `s`，得到 `s = "abcdef"`。

**示例 2：**

**输入：** `target = "aaaa", words = ["z","zz","zzz"], costs = [1,10,100]`

**输出：** `-1`

**解释：**

无法使 `s` 等于 `target`，因此返回 -1。

**提示：**

- `1 <= target.length <= 5 * 10⁴`

- `1 <= words.length == costs.length <= 5 * 10⁴`

- `1 <= words[i].length <= target.length`

- 所有 `words[i].length` 的总和小于或等于 `5 * 10⁴`

- `target` 和 `words[i]` 仅由小写英文字母组成。

- `1 <= costs[i] <= 10⁴`

---
[↑ 返回 3200-3299](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
