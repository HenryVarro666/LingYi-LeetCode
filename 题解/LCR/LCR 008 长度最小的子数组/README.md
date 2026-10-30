# LCR 008. 长度最小的子数组

Medium · [力扣原题](https://leetcode.cn/problems/2VG8Kg/)

| 作者 | 题解 | 动画讲解 |
|---|---|---|
| 灵茶山艾府 | [📄 题解](灵茶山艾府.md) | [▶︎ LCR 008 长度最小的子数组 · 灵茶山艾府.mp4](LCR%20008%20长度最小的子数组%20·%20灵茶山艾府.mp4) |
| yiduobo | — | — |

## 题目描述

给定一个含有 `n` 个正整数的数组和一个正整数 `target` **。**

找出该数组中满足其和 `≥ target` 的长度最小的 **连续子数组** `[nums_l, nums_(l+1), ..., nums_(r-1), nums_r]` ，并返回其长度**。**如果不存在符合条件的子数组，返回 `0` 。

**示例 1：**

```

输入：target = 7, nums = [2,3,1,2,4,3]
输出：2
解释：子数组 [4,3] 是该条件下的长度最小的子数组。
```

**示例 2：**

```

输入：target = 4, nums = [1,4,4]
输出：1
```

**示例 3：**

```

输入：target = 11, nums = [1,1,1,1,1,1,1,1]
输出：0
```

提示：

- `1 <= target <= 10⁹`

- `1 <= nums.length <= 10⁵`

- `1 <= nums[i] <= 10⁵`

进阶：

- 如果你已经实现 `O(n)` 时间复杂度的解法, 请尝试设计一个 `O(n log(n))` 时间复杂度的解法。

注意：本题与主站 209 题相同：[https://leetcode.cn/problems/minimum-size-subarray-sum/](https://leetcode.cn/problems/minimum-size-subarray-sum/)

---
[↑ 返回 LCR](../README.md) · [总索引](../../../索引.md) · [仓库首页](../../../README.md)
