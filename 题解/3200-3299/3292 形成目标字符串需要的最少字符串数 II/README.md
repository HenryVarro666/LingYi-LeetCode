# 3292. 形成目标字符串需要的最少字符串数 II

Hard · 难度分 2662 · [力扣原题](https://leetcode.cn/problems/minimum-number-of-valid-strings-to-form-target-ii/)

所在刷题路径：灵神题单·动态规划、灵神题单·字符串

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 3292 形成目标字符串需要的最少字符串数 II · 灵茶山艾府.mp4](3292%20形成目标字符串需要的最少字符串数%20II%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 3292 形成目标字符串需要的最少字符串数 II · yiduobo.mp4](3292%20形成目标字符串需要的最少字符串数%20II%20·%20yiduobo.mp4) |

## 题目描述

给你一个字符串数组 `words` 和一个字符串 `target`。

如果字符串 `x` 是 `words` 中 **任意** 字符串的 前缀，则认为 `x` 是一个 **有效** 字符串。

现计划通过 **连接** 有效字符串形成 `target` ，请你计算并返回需要连接的 **最少** 字符串数量。如果无法通过这种方式形成 `target`，则返回 `-1`。

**示例 1：**

**输入：** `words = ["abc","aaaaa","bcdef"], target = "aabcdabc"`

**输出：** `3`

**解释：**

target 字符串可以通过连接以下有效字符串形成：

- `words[1]` 的长度为 2 的前缀，即 `"aa"`。

- `words[2]` 的长度为 3 的前缀，即 `"bcd"`。

- `words[0]` 的长度为 3 的前缀，即 `"abc"`。

**示例 2：**

**输入：** `words = ["abababab","ab"], target = "ababaababa"`

**输出：** `2`

**解释：**

target 字符串可以通过连接以下有效字符串形成：

- `words[0]` 的长度为 5 的前缀，即 `"ababa"`。

- `words[0]` 的长度为 5 的前缀，即 `"ababa"`。

**示例 3：**

**输入：** `words = ["abcdef"], target = "xyz"`

**输出：** `-1`

**提示：**

- `1 <= words.length <= 100`

- `1 <= words[i].length <= 5 * 10⁴`

- 输入确保 `sum(words[i].length) <= 10⁵`.

- `words[i]`  只包含小写英文字母。

- `1 <= target.length <= 5 * 10⁴`

- `target`  只包含小写英文字母。

---
[↑ 返回 3200-3299](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
