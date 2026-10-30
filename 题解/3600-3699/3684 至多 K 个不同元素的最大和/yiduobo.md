---
title: "3684. 至多K个不同元素的最大和"
aliases: ["yiduobo的每日leetcode 3684.至多K个不同元素的最大和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/sorting", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1953242312529392516"
zhihu_id: "1953242312529392516"
zhihu_title: "yiduobo的每日leetcode 3684.至多K个不同元素的最大和"
question_id: "3684"
question: "至多 K 个不同元素的最大和"
problem_url: "https://leetcode.cn/problems/maximize-sum-of-at-most-k-distinct-elements/"
difficulty: "Easy"
created: "2025-09-27T01:28:36+08:00"
updated: "2025-09-27T01:28:37+08:00"
upvotes: 0
comments: 0
---

# 3684. 至多K个不同元素的最大和

> **[yiduobo的每日leetcode 3684.至多K个不同元素的最大和](https://zhuanlan.zhihu.com/p/1953242312529392516) · 知乎 · 2025-09-27 · 赞同 0**
> 力扣：[3684. 至多 K 个不同元素的最大和](https://leetcode.cn/problems/maximize-sum-of-at-most-k-distinct-elements/) · Easy · 灵茶山艾府：[排序+去重（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3684.至多K个不同元素的最大和

[3684. 至多 K 个不同元素的最大和 - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-sum-of-at-most-k-distinct-elements/description/)

题目给出一个正整数数组nums以及一个整数k，要求从中选取至多k个互不相同的元素，使得这些元素之和最大。要求按递减顺序返回选取的元素。

将nums按从大到小的顺序进行排序，接下来一趟遍历，若当前答案数组为空，或者答案数组的最后一个元素与当前元素不同，则将其加入到答案数组中，直到遍历完整个数组，或者答案数组的长度达到k为止。

最后附上python代码：

```python
class Solution(object):
    def maxKDistinct(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        
        res = []
        for v in sorted(nums, reverse=True):
            if not res or res[-1] != v:
                res.append(v)
            if len(res) == k:
                break
        
        return res
```
