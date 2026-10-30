# 2306. 公司命名

Hard · 难度分 2305 · [力扣原题](https://leetcode.cn/problems/naming-a-company/)

所在刷题路径：灵神题单·数学算法

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 2306 公司命名 · 灵茶山艾府.mp4](2306%20公司命名%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 2306 公司命名 · yiduobo.mp4](2306%20公司命名%20·%20yiduobo.mp4) |

## 题目描述

给你一个字符串数组 `ideas` 表示在公司命名过程中使用的名字列表。公司命名流程如下：

1. 从 `ideas` 中选择 2 个 **不同** 名字，称为 `idea_A` 和 `idea_B` 。

2. 交换 `idea_A` 和 `idea_B` 的首字母。

3. 如果得到的两个新名字 **都** 不在 `ideas` 中，那么 `idea_A idea_B`（**串联** `idea_A` 和 `idea_B` ，中间用一个空格分隔）是一个有效的公司名字。

4. 否则，不是一个有效的名字。

返回 **不同** 且有效的公司名字的数目。

**示例 1：**

```
输入：ideas = ["coffee","donuts","time","toffee"]
输出：6
解释：下面列出一些有效的选择方案：
- ("coffee", "donuts")：对应的公司名字是 "doffee conuts" 。
- ("donuts", "coffee")：对应的公司名字是 "conuts doffee" 。
- ("donuts", "time")：对应的公司名字是 "tonuts dime" 。
- ("donuts", "toffee")：对应的公司名字是 "tonuts doffee" 。
- ("time", "donuts")：对应的公司名字是 "dime tonuts" 。
- ("toffee", "donuts")：对应的公司名字是 "doffee tonuts" 。
因此，总共有 6 个不同的公司名字。

下面列出一些无效的选择方案：
- ("coffee", "time")：在原数组中存在交换后形成的名字 "toffee" 。
- ("time", "toffee")：在原数组中存在交换后形成的两个名字。
- ("coffee", "toffee")：在原数组中存在交换后形成的两个名字。
```

**示例 2：**

```
输入：ideas = ["lack","back"]
输出：0
解释：不存在有效的选择方案。因此，返回 0 。
```

**提示：**

- `2 <= ideas.length <= 5 * 10⁴`

- `1 <= ideas[i].length <= 10`

- `ideas[i]` 由小写英文字母组成

- `ideas` 中的所有字符串 **互不相同**

---
[↑ 返回 2300-2399](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
