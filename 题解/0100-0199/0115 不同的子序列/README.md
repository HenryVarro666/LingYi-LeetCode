# 115. 不同的子序列

Hard · [力扣原题](https://leetcode.cn/problems/distinct-subsequences/)

所在刷题路径：灵神题单·动态规划

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 0115 不同的子序列 · 灵茶山艾府.mp4](0115%20不同的子序列%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 0115 不同的子序列 · yiduobo.mp4](0115%20不同的子序列%20·%20yiduobo.mp4) |

## 题目描述

给你两个字符串 `s` 和 `t` ，统计并返回在 `s` 的 **子序列** 中 `t` 出现的个数。

测试用例保证结果在 32 位有符号整数范围内。

**示例 1：**

```

输入：s = "rabbbit", t = "rabbit"
输出：3
解释：
如下所示, 有 3 种可以从 s 中得到 "rabbit" 的方案。
rabbbit
rabbbit
rabbbit
```

**示例 2：**

```

输入：s = "babgbag", t = "bag"
输出：5
解释：
如下所示, 有 5 种可以从 s 中得到 "bag" 的方案。
babgbag
babgbag
babgbag
babgbag
babgbag
```

**提示：**

- `1 <= s.length, t.length <= 1000`

- `s` 和 `t` 由英文字母组成

---
[↑ 返回 0100-0199](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
