# 303. 区域和检索 - 数组不可变

Easy · [力扣原题](https://leetcode.cn/problems/range-sum-query-immutable/)

所在刷题路径：labuladong、灵神核心路线、灵神题单·常用数据结构

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ 0303 区域和检索 - 数组不可变 · 灵茶山艾府.mp4](0303%20区域和检索%20-%20数组不可变%20·%20灵茶山艾府.mp4) |
| yiduobo | [📄 题解](yiduobo.md) | [▶︎ 0303 区域和检索 - 数组不可变 · yiduobo.mp4](0303%20区域和检索%20-%20数组不可变%20·%20yiduobo.mp4) |

## 题目描述

给定一个整数数组  `nums`，处理以下类型的多个查询:

1. 计算索引 `left` 和 `right` （包含 `left` 和 `right`）之间的 `nums` 元素的 **和** ，其中 `left <= right`

实现 `NumArray` 类：

- `NumArray(int[] nums)` 使用数组 `nums` 初始化对象

- `int sumRange(int left, int right)` 返回数组 `nums` 中索引 `left` 和 `right` 之间的元素的 **总和** ，包含 `left` 和 `right` 两点（也就是 `nums[left] + nums[left + 1] + ... + nums[right]` )

**示例 1：**

```

输入：
["NumArray", "sumRange", "sumRange", "sumRange"]
[[[-2, 0, 3, -5, 2, -1]], [0, 2], [2, 5], [0, 5]]
输出：
[null, 1, -1, -3]

解释：
NumArray numArray = new NumArray([-2, 0, 3, -5, 2, -1]);
numArray.sumRange(0, 2); // return 1 ((-2) + 0 + 3)
numArray.sumRange(2, 5); // return -1 (3 + (-5) + 2 + (-1))
numArray.sumRange(0, 5); // return -3 ((-2) + 0 + 3 + (-5) + 2 + (-1))
```

**提示：**

- `1 <= nums.length <= 10⁴`

- `-10⁵ <= nums[i] <= 10⁵`

- `0 <= left <= right < nums.length`

- 最多调用 `10⁴` 次 `sumRange` 方法

---
[↑ 返回 0300-0399](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
