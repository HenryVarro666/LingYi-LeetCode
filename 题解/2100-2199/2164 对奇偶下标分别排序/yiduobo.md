---
title: "2164. 对奇偶下标分别排序"
aliases: ["yiduobo的每日leetcode 2164.对奇偶下标分别排序"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/532994281"
zhihu_id: "532994281"
zhihu_title: "yiduobo的每日leetcode 2164.对奇偶下标分别排序"
question_id: "2164"
question: "对奇偶下标分别排序"
problem_url: "https://leetcode.cn/problems/sort-even-and-odd-indices-independently/"
difficulty: "Easy"
created: "2022-06-23T23:35:34+08:00"
updated: "2022-06-23T23:35:34+08:00"
upvotes: 0
comments: 0
---

# 2164. 对奇偶下标分别排序

> **[yiduobo的每日leetcode 2164.对奇偶下标分别排序](https://zhuanlan.zhihu.com/p/532994281) · 知乎 · 2022-06-23 · 赞同 0**
> 力扣：[2164. 对奇偶下标分别排序](https://leetcode.cn/problems/sort-even-and-odd-indices-independently/) · Easy · 灵茶山艾府：[模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2164.对奇偶下标分别排序

[力扣](https://leetcode.cn/problems/sort-even-and-odd-indices-independently/)

比较基础的题目，依照题目要求分别按下标奇偶收集数组中的数据，排序后再按奇偶交替填充到答案数组中即可。

最后附上python代码：

```python
class Solution(object):
    def sortEvenOdd(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        odd = []
        even = []
        n = len(nums)
        for index in range(n):
            if index % 2 == 1:
                odd.append(nums[index])
            else:
                even.append(nums[index])
        
        sorted_odd = sorted(odd, reverse=True)
        sorted_even = sorted(even)
        res = []
        for index in range(n):
            if index % 2 == 1:
                res.append(sorted_odd[index / 2])
            else:
                res.append(sorted_even[index / 2])
        
        return res
```
