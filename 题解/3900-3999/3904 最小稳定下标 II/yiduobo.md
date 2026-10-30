---
title: "3903. 最小稳定下标I & 3904. 最小稳定下标II"
aliases: ["yiduobo的每日leetcode 3903.最小稳定下标I && 3904.最小稳定下标II", "3903. 最小稳定下标I", "3904. 最小稳定下标II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/dynamic-programming", "leetcode/medium", "题单/动态规划", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2029681540305560083"
zhihu_id: "2029681540305560083"
zhihu_title: "yiduobo的每日leetcode 3903.最小稳定下标I && 3904.最小稳定下标II"
question_id: ["3903", "3904"]
question: ["最小稳定下标 I", "最小稳定下标 II"]
problem_url: ["https://leetcode.cn/problems/smallest-stable-index-i/", "https://leetcode.cn/problems/smallest-stable-index-ii/"]
difficulty: ["Easy", "Medium"]
rating: 1352
created: "2026-04-20T22:15:02+08:00"
updated: "2026-04-20T22:15:03+08:00"
upvotes: 0
comments: 0
---

# 3903. 最小稳定下标I & 3904. 最小稳定下标II

> **[yiduobo的每日leetcode 3903.最小稳定下标I && 3904.最小稳定下标II](https://zhuanlan.zhihu.com/p/2029681540305560083) · 知乎 · 2026-04-20 · 赞同 0**
> 力扣：[3903. 最小稳定下标 I](https://leetcode.cn/problems/smallest-stable-index-i/) · Easy · 灵茶山艾府：[非暴力做法（Python/Java/C++/Go）](../3903%20最小稳定下标%20I/灵茶山艾府.md)
> 力扣：[3904. 最小稳定下标 II](https://leetcode.cn/problems/smallest-stable-index-ii/) · Medium · 灵茶山艾府：[前后缀分解（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3903.最小稳定下标I

<https://leetcode.cn/problems/smallest-stable-index-i/description/>

3904.最小稳定下标II

<https://leetcode.cn/problems/smallest-stable-index-ii/description/>

题目给出一个长度为n的整数数组nums，以及一个整数k。

对于每个下标index，定义其不稳定值为nums[0]到nums[index]之间的最大值，减去nums[index]到nums[n - 1]之间的最小值。若某个下标index的不稳定值小于等于k，则称该下标为稳定下标。

要求找出最小的稳定下标。若不存在，则返回-1。

两题的题设相同，第二题的数据规模较大，n可达10^5。

题目要求找出最小的稳定下标，那么一个自然的想法就是从前往后枚举所有的下标index，检测index是否为稳定下标。

对于稳定下标的检测，实际上就是要想办法计算当前下标对应的前缀的最大值，与当前下标对应的后缀的最小值之差。对于前缀最大值，可以随着index的遍历进行计算，而对于后缀最小值，则可以进行预处理，从后往前遍历一遍，计算出每个后缀中的最小值。得到后缀最小值数组后，再正式开始从前往后遍历，一边计算前缀最大值，一边利用预处理得到的后缀最小值来计算当前下标的不稳定值，并判断其是否为稳定下标。

最后附上python代码：

```python
class Solution(object):
    def firstStableIndex(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        n = len(nums)
        suffix = [nums[-1]]
        for index in range(n - 2, -1, -1):
            suffix.append(min(suffix[-1], nums[index]))
        
        suffix.reverse()
        ma = nums[0]
        v = ma - suffix[0]
        if v <= k:
            return 0
        for index in range(1, n):
            ma = max(ma, nums[index])
            v = ma - suffix[index]
            if v <= k:
                return index
        return -1
```
