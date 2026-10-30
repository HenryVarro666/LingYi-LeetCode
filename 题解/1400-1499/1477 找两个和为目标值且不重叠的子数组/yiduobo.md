---
title: "1477. 找两个和为目标值且不重叠的子数组"
aliases: ["yiduobo的每日leetcode 1477.找两个和为目标值且不重叠的子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sliding-window", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/零-常用枚举技巧", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/415169556"
zhihu_id: "415169556"
zhihu_title: "yiduobo的每日leetcode 1477.找两个和为目标值且不重叠的子数组"
question_id: "1477"
question: "找两个和为目标值且不重叠的子数组"
problem_url: "https://leetcode.cn/problems/find-two-non-overlapping-sub-arrays-each-with-target-sum/"
difficulty: "Medium"
rating: 1851
created: "2021-09-28T23:25:24+08:00"
updated: "2021-09-28T23:25:24+08:00"
upvotes: 0
comments: 0
---

# 1477. 找两个和为目标值且不重叠的子数组

> **[yiduobo的每日leetcode 1477.找两个和为目标值且不重叠的子数组](https://zhuanlan.zhihu.com/p/415169556) · 知乎 · 2021-09-28 · 赞同 0**
> 力扣：[1477. 找两个和为目标值且不重叠的子数组](https://leetcode.cn/problems/find-two-non-overlapping-sub-arrays-each-with-target-sum/) · Medium · 灵茶山艾府：[两种方法：前后缀分解 / 枚举右维护左（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1477.找两个和为目标值且不重叠的子数组

[力扣](https://leetcode-cn.com/problems/find-two-non-overlapping-sub-arrays-each-with-target-sum/)

对于子数组问题，经典做法就是将其转化为前缀和问题。具体来说，就是一趟扫描，计算前缀和。对于当前位置index的前缀和为s，若之前出现过一个值为s - target的前缀和，设对应的下标为prev，那么prev + 1到index这一段的和就是target。

为了使得答案最小，此时显然应该选择位置最靠后的prev。另外，由于题目需要找出两个不重叠的子数组，那么此时还需要找出0到prev这一段中最短且和为target的子数组，于是在这里还需要额外使用一个数组f[i]表示0到i之间和为target的最短子数组的长度，此时就应该用target - (prev + 1) + 1 + f[prev]来更新答案。而对于f的求解，则可以在先前求解的过程中顺便更新好。

除此之外，注意到题目这里的arr中都是正数，那么在这里没有必要使用前缀和，而只需要使用双指针来求解和等于target的子数组。

最后附上python代码：

```python
class Solution(object):
    def minSumOfLengths(self, arr, target):
        """
        :type arr: List[int]
        :type target: int
        :rtype: int
        """

        left = 0
        now = arr[0]
        if now == target:
            prev_min = [1]
        else:
            prev_min = [None]
        
        res = None
        for right in range(1, len(arr)):
            now += arr[right]
            while left <= right and now > target:
                now -= arr[left]
                left += 1
            
            prev_min.append(prev_min[-1])
            if now == target:
                if left > 0 and prev_min[left - 1] is not None and (res is None or res > prev_min[left - 1] + right - left + 1):
                    res = prev_min[left - 1] + right - left + 1
                
                if prev_min[-1] is None or prev_min[-1] > right - left + 1:
                    prev_min[-1] = right - left + 1
        
        if res is None:
            res = -1

        return res
```
