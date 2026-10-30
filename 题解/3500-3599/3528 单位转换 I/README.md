# 3528. 单位转换 I

Medium · 难度分 1580 · [力扣原题](https://leetcode.cn/problems/unit-conversion-i/)

所在刷题路径：灵神题单·链表树与回溯

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 3528 单位转换 I · 灵茶山艾府.mp4](3528%20单位转换%20I%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 3528 单位转换 I · yiduobo.mp4](3528%20单位转换%20I%20·%20yiduobo.mp4) |

## 题目描述

有 `n` 种单位，编号从 `0` 到 `n - 1`。给你一个二维整数数组 `conversions`，长度为 `n - 1`，其中 `conversions[i] = [sourceUnit_i, targetUnit_i, conversionFactor_i]` ，表示一个 `sourceUnit_i` 类型的单位等于 `conversionFactor_i` 个 `targetUnit_i` 类型的单位。

请你返回一个长度为 `n` 的数组 `baseUnitConversion`，其中 `baseUnitConversion[i]` 表示 **一个** 0 类型单位等于多少个 i 类型单位。由于结果可能很大，请返回每个 `baseUnitConversion[i]` 对 `10⁹ + 7` 取模后的值。

**示例 1：**

**输入：** `conversions = [[0,1,2],[1,2,3]]`

**输出：** `[1,2,6]`

**解释：**

- 使用 `conversions[0]`：将一个 0 类型单位转换为 2 个 1 类型单位。

- 使用 `conversions[0]` 和 `conversions[1]` 将一个 0 类型单位转换为 6 个 2 类型单位。

![](../../_assets/灵茶山艾府/42567f417571e8e2.png)

**示例 2：**

**输入：** `conversions = [[0,1,2],[0,2,3],[1,3,4],[1,4,5],[2,5,2],[4,6,3],[5,7,4]]`

**输出：** `[1,2,3,8,10,6,30,24]`

**解释：**

- 使用 `conversions[0]` 将一个 0 类型单位转换为 2 个 1 类型单位。

- 使用 `conversions[1]` 将一个 0 类型单位转换为 3 个 2 类型单位。

- 使用 `conversions[0]` 和 `conversions[2]` 将一个 0 类型单位转换为 8 个 3 类型单位。

- 使用 `conversions[0]` 和 `conversions[3]` 将一个 0 类型单位转换为 10 个 4 类型单位。

- 使用 `conversions[1]` 和 `conversions[4]` 将一个 0 类型单位转换为 6 个 5 类型单位。

- 使用 `conversions[0]`、`conversions[3]` 和 `conversions[5]` 将一个 0 类型单位转换为 30 个 6 类型单位。

- 使用 `conversions[1]`、`conversions[4]` 和 `conversions[6]` 将一个 0 类型单位转换为 24 个 7 类型单位。

**提示：**

- `2 <= n <= 10⁵`

- `conversions.length == n - 1`

- `0 <= sourceUnit_i, targetUnit_i < n`

- `1 <= conversionFactor_i <= 10⁹`

- 保证单位 0 可以通过 **唯一** 的转换路径（不需要反向转换）转换为任何其他单位。

---
[↑ 返回 3500-3599](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
