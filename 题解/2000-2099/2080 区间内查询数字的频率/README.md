# 2080. 区间内查询数字的频率

Medium · 难度分 1702 · [力扣原题](https://leetcode.cn/problems/range-frequency-queries/)

所在刷题路径：灵神题单·二分算法

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 动画（GIF）](2080%20区间内查询数字的频率%20·%20灵茶山艾府.gif) · [mp4 文件](2080%20区间内查询数字的频率%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 动画（GIF）](2080%20区间内查询数字的频率%20·%20yiduobo.gif) · [mp4 文件](2080%20区间内查询数字的频率%20·%20yiduobo.mp4) |

## 动画讲解

> 动图会循环播放；想暂停、拖进度条请下载上面表格里的 mp4 文件。

### 灵茶山艾府

![2080 区间内查询数字的频率 · 灵茶山艾府](2080%20区间内查询数字的频率%20·%20灵茶山艾府.gif)

### yiduobo

![2080 区间内查询数字的频率 · yiduobo](2080%20区间内查询数字的频率%20·%20yiduobo.gif)


## 题目描述

请你设计一个数据结构，它能求出给定子数组内一个给定值的 **频率** 。

子数组中一个值的 **频率** 指的是这个子数组中这个值的出现次数。

请你实现 `RangeFreqQuery` 类：

- `RangeFreqQuery(int[] arr)` 用下标从 **0** 开始的整数数组 `arr` 构造一个类的实例。

- `int query(int left, int right, int value)` 返回子数组 `arr[left...right]` 中 `value` 的 **频率** 。

一个 **子数组** 指的是数组中一段连续的元素。`arr[left...right]` 指的是 `nums` 中包含下标 `left` 和 `right` **在内** 的中间一段连续元素。

**示例 1：**

```
输入：
["RangeFreqQuery", "query", "query"]
[[[12, 33, 4, 56, 22, 2, 34, 33, 22, 12, 34, 56]], [1, 2, 4], [0, 11, 33]]
输出：
[null, 1, 2]

解释：
RangeFreqQuery rangeFreqQuery = new RangeFreqQuery([12, 33, 4, 56, 22, 2, 34, 33, 22, 12, 34, 56]);
rangeFreqQuery.query(1, 2, 4); // 返回 1 。4 在子数组 [33, 4] 中出现 1 次。
rangeFreqQuery.query(0, 11, 33); // 返回 2 。33 在整个子数组中出现 2 次。
```

**提示：**

- `1 <= arr.length <= 10⁵`

- `1 <= arr[i], value <= 10⁴`

- `0 <= left <= right < arr.length`

- 调用 `query` 不超过 `10⁵` 次。

---
[↑ 返回 2000-2099](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
