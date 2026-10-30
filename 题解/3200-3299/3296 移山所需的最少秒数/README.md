# 3296. 移山所需的最少秒数

Medium · 难度分 1850 · [力扣原题](https://leetcode.cn/problems/minimum-number-of-seconds-to-make-mountain-height-zero/)

所在刷题路径：灵神核心路线、灵神题单·二分算法、灵神题单·常用数据结构

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 3296 移山所需的最少秒数 · 灵茶山艾府.mp4](3296%20移山所需的最少秒数%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 3296 移山所需的最少秒数 · yiduobo.mp4](3296%20移山所需的最少秒数%20·%20yiduobo.mp4) |

## 题目描述

给你一个整数 `mountainHeight` 表示山的高度。

同时给你一个整数数组 `workerTimes`，表示工人们的工作时间（单位：**秒**）。

工人们需要 **同时** 进行工作以 **降低** 山的高度。对于工人 `i` :

- 山的高度降低 1，需要 `workerTimes[i]` 秒。

- 山的高度降低 2，需要 `workerTimes[i] * 2` 秒。

- ...

- 山的高度降低 `x`，需要 `workerTimes[i] * x` 秒。

工人 `i` 所花费的总时间是所有 `x` 单位所需时间的总和。由于所有工人同时操作，所需的总时间是任何工人花费的 **最大** 时间。

返回一个整数，表示工人们使山的高度降低到 0 所需的 **最少** 秒数。

**示例 1：**

**输入：** `mountainHeight = 4, workerTimes = [2,1,1]`

**输出：** `3`

**解释：**

将山的高度降低到 0 的一种方式是：

- 工人 0 将高度降低 1，花费 `workerTimes[0] = 2` 秒。

- 工人 1 将高度降低 2，花费 `workerTimes[1] + workerTimes[1] * 2 = 3` 秒。

- 工人 2 将高度降低 1，花费 `workerTimes[2] = 1` 秒。

因为工人同时工作，所需的最少时间为 `max(2, 3, 1) = 3` 秒。

**示例 2：**

**输入：** `mountainHeight = 10, workerTimes = [3,2,2,4]`

**输出：** `12`

**解释：**

- 工人 0 将高度降低 2，花费 `workerTimes[0] + workerTimes[0] * 2 = 9` 秒。

- 工人 1 将高度降低 3，花费 `workerTimes[1] + workerTimes[1] * 2 + workerTimes[1] * 3 = 12` 秒。

- 工人 2 将高度降低 3，花费 `workerTimes[2] + workerTimes[2] * 2 + workerTimes[2] * 3 = 12` 秒。

- 工人 3 将高度降低 2，花费 `workerTimes[3] + workerTimes[3] * 2 = 12` 秒。

所需的最少时间为 `max(9, 12, 12, 12) = 12` 秒。

**示例 3：**

**输入：** `mountainHeight = 5, workerTimes = [1]`

**输出：** `15`

**解释：**

这个示例中只有一个工人，所以答案是 `workerTimes[0] + workerTimes[0] * 2 + workerTimes[0] * 3 + workerTimes[0] * 4 + workerTimes[0] * 5 = 15` 秒。

**提示：**

- `1 <= mountainHeight <= 10⁵`

- `1 <= workerTimes.length <= 10⁴`

- `1 <= workerTimes[i] <= 10⁶`

---
[↑ 返回 3200-3299](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
