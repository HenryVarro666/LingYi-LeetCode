---
title: "2270. 分割数组的方案数"
aliases: ["yiduobo的每日leetcode 2270.分割数组的方案数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/array", "题单/动态规划", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/549637608"
zhihu_id: "549637608"
zhihu_title: "yiduobo的每日leetcode 2270.分割数组的方案数"
question_id: "2270"
question: "分割数组的方案数"
problem_url: "https://leetcode.cn/problems/number-of-ways-to-split-array/"
difficulty: "Medium"
rating: 1334
created: "2022-08-04T01:09:29+08:00"
updated: "2022-08-04T01:09:29+08:00"
upvotes: 0
comments: 0
---

# 2270. 分割数组的方案数

> **[yiduobo的每日leetcode 2270.分割数组的方案数](https://zhuanlan.zhihu.com/p/549637608) · 知乎 · 2022-08-04 · 赞同 0**
> 力扣：[2270. 分割数组的方案数](https://leetcode.cn/problems/number-of-ways-to-split-array/) · Medium · 灵茶山艾府：[两次遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2270.分割数组的方案数

[力扣](https://leetcode.cn/problems/number-of-ways-to-split-array/)

题目要求找出所有的分割点，使得分割点左侧数字之和大于等于右侧之和。分割点左侧数字之和是一个典型的前缀和问题，而右侧数字之和则可以通过数组总和减去左侧数字之和得到，于是可以先预先计算好数组总和s，然后从左向右一趟遍历，使用一个遍历now记录到当前位置的前缀和。每一轮都使用当前数字更新now，然后对比now和s - now的大小来判断当前位置是否为合法的分割点并更新答案。

最后附上python代码：

```python
class Solution(object):
    def waysToSplitArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        s = sum(nums)
        res = 0
        now = 0
        for index in range(len(nums) - 1):
            now += nums[index]
            if now >= s - now:
                res += 1
        
        return res
```
