---
title: "2453. 摧毁一系列目标"
aliases: ["yiduobo的每日leetcode 2453.摧毁一系列目标"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/math", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/585538321"
zhihu_id: "585538321"
zhihu_title: "yiduobo的每日leetcode 2453.摧毁一系列目标"
question_id: "2453"
question: "摧毁一系列目标"
problem_url: "https://leetcode.cn/problems/destroy-sequential-targets/"
difficulty: "Medium"
rating: 1762
created: "2022-11-22T01:59:32+08:00"
updated: "2022-11-22T01:59:32+08:00"
upvotes: 0
comments: 0
---

# 2453. 摧毁一系列目标

> **[yiduobo的每日leetcode 2453.摧毁一系列目标](https://zhuanlan.zhihu.com/p/585538321) · 知乎 · 2022-11-22 · 赞同 0**
> 力扣：[2453. 摧毁一系列目标](https://leetcode.cn/problems/destroy-sequential-targets/) · Medium · 灵茶山艾府：[按模 space 的结果分组](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2453.摧毁一系列目标

[力扣](https://leetcode.cn/problems/destroy-sequential-targets/)

在输入nums[i]后，所有nums[i] + c \* space的目标都将被摧毁，这也就意味着说有满足nums[j] >\= nums[i]，且nums[j] % space \= nums[i] % space的目标j都将被摧毁。于是在这里可以根据nums中的数先根据其对space的余数聚合起来，然后对于一组余数相同的nums，输入其中最下的nums，就可以将这一组余数相同的nums全部摧毁。

题目要找的是摧毁尽量多目标前提下，可输入的最小值，此时就只需要遍历每一组余数相同的nums，取其中数字最多的那一组中nums的最小值作为答案即可。当两组nums的数字个数相同时，则应该取两组数字各自最小值中较小的那一个。

最后附上python代码：

```python
class Solution(object):
    def destroyTargets(self, nums, space):
        """
        :type nums: List[int]
        :type space: int
        :rtype: int
        """

        rest = {}
        for index, num in enumerate(nums):
            r = num % space
            if r not in rest:
                rest[r] = [index, 0]
            elif nums[rest[r][0]] > num:
                rest[r][0] = index

            rest[r][1] += 1
        
        res = None
        max_cnt = 0
        for index, cnt in rest.values():
            if cnt > max_cnt or (cnt == max_cnt and nums[index] < res):
                max_cnt = cnt
                res = nums[index]
        
        return res
```
