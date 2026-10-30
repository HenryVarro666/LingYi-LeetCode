# 2186. 制造字母异位词的最小步骤数 II

Medium · [力扣原题](https://leetcode.cn/problems/minimum-number-of-steps-to-make-two-strings-anagram-ii/)

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | — |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 2186 制造字母异位词的最小步骤数 II · yiduobo.mp4](2186%20制造字母异位词的最小步骤数%20II%20·%20yiduobo.mp4) |

## 题目描述

给你两个字符串 `s` 和 `t` 。在一步操作中，你可以给 `s` 或者 `t` 追加 **任一字符** 。

返回使 `s` 和 `t` 互为 **字母异位词** 所需的最少步骤数<em>。</em>

**字母异位词** 指字母相同但是顺序不同（或者相同）的字符串。

**示例 1：**

```
输入：s = "leetcode", t = "coats"
输出：7
解释：
- 执行 2 步操作，将 "as" 追加到 s = "leetcode" 中，得到 s = "leetcodeas" 。
- 执行 5 步操作，将 "leede" 追加到 t = "coats" 中，得到 t = "coatsleede" 。
"leetcodeas" 和 "coatsleede" 互为字母异位词。
总共用去 2 + 5 = 7 步。
可以证明，无法用少于 7 步操作使这两个字符串互为字母异位词。
```

**示例 2：**

```
输入：s = "night", t = "thing"
输出：0
解释：给出的字符串已经互为字母异位词。因此，不需要任何进一步操作。
```

**提示：**

- `1 <= s.length, t.length <= 2 * 10⁵`

- `s` 和 `t` 由小写英文字符组成

---
[↑ 返回 2100-2199](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
