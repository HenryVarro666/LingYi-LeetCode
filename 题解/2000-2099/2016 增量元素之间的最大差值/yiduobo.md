---
title: "2016. 增量元素之间的最大差值"
aliases: ["yiduobo的每日leetcode 2016.增量元素之间的最大差值"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/505638705"
zhihu_id: "505638705"
zhihu_title: "yiduobo的每日leetcode 2016.增量元素之间的最大差值"
question_id: "2016"
question: "增量元素之间的最大差值"
problem_url: "https://leetcode.cn/problems/maximum-difference-between-increasing-elements/"
difficulty: "Easy"
rating: 1246
created: "2022-04-26T23:43:02+08:00"
updated: "2022-04-26T23:43:02+08:00"
upvotes: 0
comments: 0
---

# 2016. 增量元素之间的最大差值

> **[yiduobo的每日leetcode 2016.增量元素之间的最大差值](https://zhuanlan.zhihu.com/p/505638705) · 知乎 · 2022-04-26 · 赞同 0**
> 力扣：[2016. 增量元素之间的最大差值](https://leetcode.cn/problems/maximum-difference-between-increasing-elements/) · Easy · 灵茶山艾府：[O(n) 做法：枚举右，维护左（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2016.增量元素之间的最大差值

[力扣](https://leetcode-cn.com/problems/maximum-difference-between-increasing-elements/)

由于题目数据规模比较小，直接暴力枚举每一组i和j然后求解是可行的做法。当然，在这里也可以采用一个常见的小优化。

一趟遍历，枚举j的位置。对于当前的nums[j]，为了使得nums[j] - nums[i]尽可能大，那么就需要让选择的nums[i]尽可能小，也就是说应该找出nums[0]到nums[j - 1]之间的最小值。

对于这个最小值，则可以通过对比nums[0]到nums[j - 2]之间的最小值以及nums[j - 1]来得到。

最后附上python代码：

```python
class Solution(object):
    def maximumDifference(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        mi = nums[0]
        p = 0
        res = -1
        for index in range(1, len(nums)):
            if nums[index] > mi:
                res = max(res, nums[index] - mi)
            elif nums[index] < mi:
                mi = nums[index]
                p = index
        
        return res
```
