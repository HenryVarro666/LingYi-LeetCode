# 2185. 统计包含给定前缀的字符串

Easy · [力扣原题](https://leetcode.cn/problems/counting-words-with-a-given-prefix/)

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | — |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 2185 统计包含给定前缀的字符串 · yiduobo.mp4](2185%20统计包含给定前缀的字符串%20·%20yiduobo.mp4) |

## 题目描述

给你一个字符串数组 `words` 和一个字符串 `pref` 。

返回 `words` 中以 `pref` 作为 **前缀** 的字符串的数目。

字符串 `s` 的 **前缀** 就是  `s` 的任一前导连续字符串。

**示例 1：**

```
输入：words = ["pay","attention","practice","attend"], pref = "at"
输出：2
解释：以 "at" 作为前缀的字符串有两个，分别是："attention" 和 "attend" 。
```

**示例 2：**

```
输入：words = ["leetcode","win","loops","success"], pref = "code"
输出：0
解释：不存在以 "code" 作为前缀的字符串。
```

**提示：**

- `1 <= words.length <= 100`

- `1 <= words[i].length, pref.length <= 100`

- `words[i]` 和 `pref` 由小写英文字母组成

---
[↑ 返回 2100-2199](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
