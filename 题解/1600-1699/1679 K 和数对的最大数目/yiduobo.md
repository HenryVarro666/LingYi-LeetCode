---
title: "1679. K和数对的最大数目"
aliases: ["yiduobo的每日leetcode 1679.K和数对的最大数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/bian-li", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/444957829"
zhihu_id: "444957829"
zhihu_title: "yiduobo的每日leetcode 1679.K和数对的最大数目"
question_id: "1679"
question: "K 和数对的最大数目"
problem_url: "https://leetcode.cn/problems/max-number-of-k-sum-pairs/"
difficulty: "Medium"
rating: 1346
created: "2021-12-13T23:36:29+08:00"
updated: "2021-12-13T23:36:29+08:00"
upvotes: 0
comments: 0
---

# 1679. K和数对的最大数目

> **[yiduobo的每日leetcode 1679.K和数对的最大数目](https://zhuanlan.zhihu.com/p/444957829) · 知乎 · 2021-12-13 · 赞同 0**
> 力扣：[1679. K 和数对的最大数目](https://leetcode.cn/problems/max-number-of-k-sum-pairs/) · Medium · 灵茶山艾府：[O(n) 一次遍历（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

1679.K和数对的最大数目

[力扣](https://leetcode-cn.com/problems/max-number-of-k-sum-pairs/)

不说跟第一题一模一样，那也是大差不差的。直接照搬第一题的做法，排序后双指针向中间扫描就好了。

最后附上python代码：

```python
class Solution(object):
    def maxOperations(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        nums = sorted(nums)
        l = 0
        r = len(nums) - 1
        res = 0
        while l < r:
            s = nums[l] + nums[r]
            if s == k:
                l += 1
                r -= 1
                res += 1
            elif s > k:
                r -= 1
            else:
                l += 1
        
        return res
```
