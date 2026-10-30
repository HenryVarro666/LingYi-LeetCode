---
title: "2099. 找到和最大的长度为K的子序列"
aliases: ["yiduobo的每日leetcode 2099.找到和最大的长度为K的子序列"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/quickselect", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/521424172"
zhihu_id: "521424172"
zhihu_title: "yiduobo的每日leetcode 2099.找到和最大的长度为K的子序列"
question_id: "2099"
question: "找到和最大的长度为 K 的子序列"
problem_url: "https://leetcode.cn/problems/find-subsequence-of-length-k-with-the-largest-sum/"
difficulty: "Easy"
rating: 1447
created: "2022-05-28T23:21:19+08:00"
updated: "2022-05-28T23:21:19+08:00"
upvotes: 0
comments: 0
---

# 2099. 找到和最大的长度为K的子序列

> **[yiduobo的每日leetcode 2099.找到和最大的长度为K的子序列](https://zhuanlan.zhihu.com/p/521424172) · 知乎 · 2022-05-28 · 赞同 0**
> 力扣：[2099. 找到和最大的长度为 K 的子序列](https://leetcode.cn/problems/find-subsequence-of-length-k-with-the-largest-sum/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2099.找到和最大的长度为K的子序列

<https://leetcode.cn/problems/find-subsequence-of-length-k-with-the-largest-sum/>

题目要求找出和最大的长度为K的子序列，那么显然应该选择数组中最大的K个数，于是只需将数组从大到小排序后选择top K的数即可。

最后附上python代码：

```python
class Solution(object):
    def maxSubsequence(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """

        n = len(nums)
        order = sorted(range(n), key=lambda d:-nums[d])
        chosen = set(order[:k])
        res = []
        for index in range(n):
            if index in chosen:
                res.append(nums[index])
        
        return res
```
