# 1147. 段式回文

Hard · 难度分 1912 · [力扣原题](https://leetcode.cn/problems/longest-chunked-palindrome-decomposition/)

所在刷题路径：灵神题单·贪心与思维

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 1147 段式回文 · 灵茶山艾府.mp4](1147%20段式回文%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 1147 段式回文 · yiduobo.mp4](1147%20段式回文%20·%20yiduobo.mp4) |

## 题目描述

你会得到一个字符串 `text` 。你应该把它分成 `k` 个子字符串 `(subtext1, subtext2，…， subtextk)` ，要求满足:

- `subtext_i`<sub> </sub>是 **非空** 字符串

- 所有子字符串的连接等于 `text` ( 即`subtext₁ + subtext₂ + ... + subtext_k == text` )

- 对于所有 i 的有效值( 即 `1 <= i <= k` ) ，`subtext_i == subtext_(k - i + 1)` 均成立

返回`k`可能最大值。

**示例 1：**

```

输入：text = "ghiabcdefhelloadamhelloabcdefghi"
输出：7
解释：我们可以把字符串拆分成 "(ghi)(abcdef)(hello)(adam)(hello)(abcdef)(ghi)"。
```

**示例 2：**

```

输入：text = "merchant"
输出：1
解释：我们可以把字符串拆分成 "(merchant)"。
```

**示例 3：**

```

输入：text = "antaprezatepzapreanta"
输出：11
解释：我们可以把字符串拆分成 "(a)(nt)(a)(pre)(za)(tep)(za)(pre)(a)(nt)(a)"。
```

**提示：**

- `1 <= text.length <= 1000`

- `text` 仅由小写英文字符组成

---
[↑ 返回 1100-1199](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
