# 72. 编辑距离

Medium · [力扣原题](https://leetcode.cn/problems/edit-distance/)

所在刷题路径：labuladong、灵神核心路线、灵神突击、灵神题单·动态规划

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 0072 编辑距离 · 灵茶山艾府.mp4](0072%20编辑距离%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 0072 编辑距离 · yiduobo.mp4](0072%20编辑距离%20·%20yiduobo.mp4) |

## 题目描述

给你两个单词 `word1` 和 `word2`， <em>请返回将 `word1` 转换成 `word2` 所使用的最少操作数</em>  。

你可以对一个单词进行如下三种操作：

- 插入一个字符

- 删除一个字符

- 替换一个字符

**示例 1：**

```

输入：word1 = "horse", word2 = "ros"
输出：3
解释：
horse -> rorse (将 'h' 替换为 'r')
rorse -> rose (删除 'r')
rose -> ros (删除 'e')
```

**示例 2：**

```

输入：word1 = "intention", word2 = "execution"
输出：5
解释：
intention -> inention (删除 't')
inention -> enention (将 'i' 替换为 'e')
enention -> exention (将 'n' 替换为 'x')
exention -> exection (将 'n' 替换为 'c')
exection -> execution (插入 'u')
```

**提示：**

- `0 <= word1.length, word2.length <= 500`

- `word1` 和 `word2` 由小写英文字母组成

---
[↑ 返回 0000-0099](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
