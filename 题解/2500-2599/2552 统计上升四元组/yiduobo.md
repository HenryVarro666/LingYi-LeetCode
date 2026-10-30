---
title: "2552. 统计上升四元组"
aliases: ["yiduobo的每日leetcode 2552.统计上升四元组"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "leetcode/enumeration", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/零-常用枚举技巧", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/638955470"
zhihu_id: "638955470"
zhihu_title: "yiduobo的每日leetcode 2552.统计上升四元组"
question_id: "2552"
question: "统计上升四元组"
problem_url: "https://leetcode.cn/problems/count-increasing-quadruplets/"
difficulty: "Hard"
rating: 2433
created: "2023-06-25T01:24:49+08:00"
updated: "2023-06-25T01:24:49+08:00"
upvotes: 2
comments: 0
---

# 2552. 统计上升四元组

> **[yiduobo的每日leetcode 2552.统计上升四元组](https://zhuanlan.zhihu.com/p/638955470) · 知乎 · 2023-06-25 · 赞同 2**
> 力扣：[2552. 统计上升四元组](https://leetcode.cn/problems/count-increasing-quadruplets/) · Hard · 灵茶山艾府：[两种不同的思考方式（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2552.统计上升四元组

[力扣](https://leetcode.cn/problems/count-increasing-quadruplets/)

题目给出一个1到n的排列，要求找出其中所有形如1324的四元组的数目。

对于本题，使用各式各样区间相关的数据结构应该是很好处理的，我在这里则是从极值出发来考虑。

对于1324这种形式的四元组，可以先枚举这个4的下标four，接下来在four左侧枚举3的下标three。在这里若nums[four] > nums[three]，那么这里的数值大小就符合34的大小关系，此时只需将four左侧，以nums[three]为3的所有形如132的三元组数目累加到答案中即可。

而对于这个132的三元组数目，则可以在另一种情况，也就是nums[three] > nums[four]时来更新。

在从左向右遍历three的过程中，统计之前满足nums[four] > nums[pre_three]的下标pre_three的数量。一旦当前的nums[three] > nums[four]，那么由nums[pre_three]，nums[three]，nums[four]这三个位置形成的三元组就是一个132的三元组，此时就只需将之前满足条件的pre_three的个数累加到以nums[three]为3的132三元组的数目中即可。

最后附上python代码：

```python
class Solution(object):
    def countQuadruplets(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)

        cnt = [0] * n
        res = 0
        for four in range(n):
            one = 0
            for three in range(four):
                if nums[four] > nums[three]:
                    res += cnt[three]
                    one += 1
                else:
                    cnt[three] += one

        return res
```
