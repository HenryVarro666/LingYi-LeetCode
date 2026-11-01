# 307. 区域和检索 - 数组可修改

Medium · [力扣原题](https://leetcode.cn/problems/range-sum-query-mutable/)

所在刷题路径：灵神题单·常用数据结构

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 动画（GIF）](0307%20区域和检索%20-%20数组可修改%20·%20灵茶山艾府.gif) · [mp4 文件](0307%20区域和检索%20-%20数组可修改%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 动画（GIF）](0307%20区域和检索%20-%20数组可修改%20·%20yiduobo.gif) · [mp4 文件](0307%20区域和检索%20-%20数组可修改%20·%20yiduobo.mp4) |

## 动画讲解

> 动图会循环播放；想暂停、拖进度条请下载上面表格里的 mp4 文件。

### 灵茶山艾府

![0307 区域和检索 - 数组可修改 · 灵茶山艾府](0307%20区域和检索%20-%20数组可修改%20·%20灵茶山艾府.gif)

### yiduobo

![0307 区域和检索 - 数组可修改 · yiduobo](0307%20区域和检索%20-%20数组可修改%20·%20yiduobo.gif)


## 题目描述

给你一个数组 `nums` ，请你完成两类查询。

1. 其中一类查询要求 **更新** 数组 `nums` 下标对应的值

2. 另一类查询要求返回数组 `nums` 中索引 `left` 和索引 `right` 之间（ **包含** ）的nums元素的 **和** ，其中 `left <= right`

实现 `NumArray` 类：

- `NumArray(int[] nums)` 用整数数组 `nums` 初始化对象

- `void update(int index, int val)` 将 `nums[index]` 的值 **更新** 为 `val`

- `int sumRange(int left, int right)` 返回数组 `nums` 中索引 `left` 和索引 `right` 之间（ **包含** ）的nums元素的 **和** （即，`nums[left] + nums[left + 1], ..., nums[right]`）

**示例 1：**

```

输入：
["NumArray", "sumRange", "update", "sumRange"]
[[[1, 3, 5]], [0, 2], [1, 2], [0, 2]]
输出：
[null, 9, null, 8]

解释：
NumArray numArray = new NumArray([1, 3, 5]);
numArray.sumRange(0, 2); // 返回 1 + 3 + 5 = 9
numArray.update(1, 2);   // nums = [1,2,5]
numArray.sumRange(0, 2); // 返回 1 + 2 + 5 = 8
```

**提示：**

- `1 <= nums.length <= 3 * 10⁴`

- `-100 <= nums[i] <= 100`

- `0 <= index < nums.length`

- `-100 <= val <= 100`

- `0 <= left <= right < nums.length`

- 调用 `update` 和 `sumRange` 方法次数不大于 `3 * 10⁴`

---
[↑ 返回 0300-0399](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
