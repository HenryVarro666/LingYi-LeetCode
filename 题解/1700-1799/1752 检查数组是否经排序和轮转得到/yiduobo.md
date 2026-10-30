---
title: "1752. 检查数组是否经排序和轮转得到"
aliases: ["yiduobo的每日leetcode 1752.检查数组是否经排序和轮转得到"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/455256691"
zhihu_id: "455256691"
zhihu_title: "yiduobo的每日leetcode 1752.检查数组是否经排序和轮转得到"
question_id: "1752"
question: "检查数组是否经排序和轮转得到"
problem_url: "https://leetcode.cn/problems/check-if-array-is-sorted-and-rotated/"
difficulty: "Easy"
created: "2022-01-10T00:36:46+08:00"
updated: "2022-01-10T00:36:46+08:00"
upvotes: 0
comments: 0
---

# 1752. 检查数组是否经排序和轮转得到

> **[yiduobo的每日leetcode 1752.检查数组是否经排序和轮转得到](https://zhuanlan.zhihu.com/p/455256691) · 知乎 · 2022-01-10 · 赞同 0**
> 力扣：[1752. 检查数组是否经排序和轮转得到](https://leetcode.cn/problems/check-if-array-is-sorted-and-rotated/) · Easy · 灵茶山艾府：[至多一次严格递减，附思考题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1752.检查数组是否经排序和轮转得到

[力扣](https://leetcode-cn.com/problems/check-if-array-is-sorted-and-rotated/)

首先，如果数组没有被轮转过，那么数组必然是单调不减的。如果被轮转过，那么其需要满足三个条件：

1、数组中存在且仅存在一个位置p，满足nums[p] > nums[p + 1]

1、数组中从nums[0]到nums[p]是单调不减的，从nums[p + 1]到nums[n - 1]也是单调不减的

2、数组中nums[p + 1]到nums[n - 1]中的每个数都必须小于等于nums[0]

于是可以一趟循环，先找到第一次满足nums[p] > nums[p + 1]的位置p。若不存在，说明数组是单调不减的，此时直接返回true。若存在p，那么需要从p + 1开始向后检测是否单调不减，且每个数都小于等于nums[0]，若满足则返回true否则返回false。

最后附上python代码：

```python
class Solution(object):
    def check(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        n = len(nums)
        p = 0
        while p < n - 1 and nums[p] <= nums[p + 1]:
            p += 1
        
        if p == n - 1:
            return True
        
        p += 1
        while p < n - 1 and nums[p] <= nums[p + 1] and nums[p] <= nums[0]:
            p += 1
        
        if p == n - 1 and nums[p] <= nums[0]:
            return True

        return False
```
