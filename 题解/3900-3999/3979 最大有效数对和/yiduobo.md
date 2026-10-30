---
title: "3979. 最大有效数对和"
aliases: ["yiduobo的每日leetcode 3979.最大有效数对和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2057145944785925059"
zhihu_id: "2057145944785925059"
zhihu_title: "yiduobo的每日leetcode 3979.最大有效数对和"
question_id: "3979"
question: "最大有效数对和"
problem_url: "https://leetcode.cn/problems/maximum-valid-pair-sum/"
difficulty: "Medium"
rating: 1328
created: "2026-07-05T17:22:04+08:00"
updated: "2026-07-05T17:22:05+08:00"
upvotes: 2
comments: 0
---

# 3979. 最大有效数对和

> **[yiduobo的每日leetcode 3979.最大有效数对和](https://zhuanlan.zhihu.com/p/2057145944785925059) · 知乎 · 2026-07-05 · 赞同 2**
> 力扣：[3979. 最大有效数对和](https://leetcode.cn/problems/maximum-valid-pair-sum/) · Medium · 灵茶山艾府：[枚举右，维护左（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3979.最大有效数对和

<https://leetcode.cn/problems/maximum-valid-pair-sum/description/>

题目给出一个长度为n的整数数组nums，以及一个整数k。

对于一组下标对(i, j)，若0 \<\= i \< j \< n，且j - i >\= k，那么就称这组下标对是有效的。

问所有有效下标对中，nums[i] + nums[j]最大可能是多少。

对于一个指定的j，其可以用来配对的i需要满足0 \<\= i \<\= j - k。而为了使得配对的结果最大，在这里就应该使用nums[0]到nums[j - k]这个前缀中的最大值与nums[j]配对。另一方面，随着j的向后移动，这个可用的前缀也是越来越长的，也就是说每个j对应的前缀最大值都可以通过对比前一个j的前缀最大值以及nums[j - k]得到。

基于上面的结论，就可以使用一个变量ma记录当前可用的前缀最大值，然后从下标k开始向后遍历，枚举所有的j，一边更新ma，一边计算配对的结果并更新答案。具体来说，对于当前遍历到的下标index，先使用nums[index - k]更新ma，然后使用ma + nums[index]更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxValidPairSum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        p = 0
        ma = 0
        res = 0
        for index, v in enumerate(nums[k:]):
            ma = max(ma, nums[index])
            res = max(res, v + ma)

        return res
```
