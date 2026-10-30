# 3986. 统计起止时间经过的秒数

Easy · [力扣原题](https://leetcode.cn/problems/number-of-elapsed-seconds-between-two-times/)

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 3986 统计起止时间经过的秒数 · 灵茶山艾府.mp4](3986%20统计起止时间经过的秒数%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 3986 统计起止时间经过的秒数 · yiduobo.mp4](3986%20统计起止时间经过的秒数%20·%20yiduobo.mp4) |

## 题目描述

给你两个有效时间 `startTime` 和 `endTime`，它们均以字符串形式表示，格式为 `"HH:MM:SS"`。

返回从 `startTime` 到 `endTime` 经过的秒数（包含两个端点）。

**示例 1：**

**输入：** `startTime = "01:00:00", endTime = "01:00:25"`

**输出：** `25`

**解释：**

`endTime` 比 `startTime` 晚 25 秒。

**示例 2：**

**输入：** `startTime = "12:34:56", endTime = "13:00:00"`

**输出：** `1504`

**解释：**

`endTime` 比 `startTime` 晚 25 分 4 秒，共计 1504 秒。

**提示：**

- `startTime.length == 8`

- `endTime.length == 8`

- `startTime` 和 `endTime` 均为格式 `"HH:MM:SS"` 的有效时间

- `00 <= HH <= 23`

- `00 <= MM <= 59`

- `00 <= SS <= 59`

- `endTime` 不早于 `startTime`

---
[↑ 返回 3900-3999](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
