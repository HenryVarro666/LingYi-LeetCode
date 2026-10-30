# 2030. 含特定字母的最小子序列

Hard · 难度分 2562 · [力扣原题](https://leetcode.cn/problems/smallest-k-length-subsequence-with-occurrences-of-a-letter/)

所在刷题路径：灵神题单·单调栈

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | — |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 2030 含特定字母的最小子序列 · yiduobo.mp4](2030%20含特定字母的最小子序列%20·%20yiduobo.mp4) |

## 题目描述

给你一个字符串 `s` ，一个整数 `k` ，一个字母 `letter` 以及另一个整数 `repetition` 。

返回 `s` 中长度为 `k` 且 **字典序最小** 的子序列，该子序列同时应满足字母 `letter` 出现 **至少** `repetition` 次。生成的测试用例满足 `letter` 在 `s` 中出现 **至少** `repetition` 次。

**子序列** 是由原字符串删除一些（或不删除）字符且不改变剩余字符顺序得到的剩余字符串。

字符串 `a` 字典序比字符串 `b` 小的定义为：在 `a` 和 `b` 出现不同字符的第一个位置上，字符串 `a` 的字符在字母表中的顺序早于字符串 `b` 的字符。

**示例 1：**

```

输入：s = "leet", k = 3, letter = "e", repetition = 1
输出："eet"
解释：存在 4 个长度为 3 ，且满足字母 'e' 出现至少 1 次的子序列：
- "lee"（"leet"）
- "let"（"leet"）
- "let"（"leet"）
- "eet"（"leet"）
其中字典序最小的子序列是 "eet" 。
```

**示例 2：**

![example-2](../../_assets/灵茶山艾府/4e4882918bfe3d2e.png)

```

输入：s = "leetcode", k = 4, letter = "e", repetition = 2
输出："ecde"
解释："ecde" 是长度为 4 且满足字母 "e" 出现至少 2 次的字典序最小的子序列。
```

**示例 3：**

```

输入：s = "bb", k = 2, letter = "b", repetition = 2
输出："bb"
解释："bb" 是唯一一个长度为 2 且满足字母 "b" 出现至少 2 次的子序列。
```

**提示：**

- `1 <= repetition <= k <= s.length <= 5 * 10⁴`

- `s` 由小写英文字母组成

- `letter` 是一个小写英文字母，在 `s` 中至少出现 `repetition` 次

---
[↑ 返回 2000-2099](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
