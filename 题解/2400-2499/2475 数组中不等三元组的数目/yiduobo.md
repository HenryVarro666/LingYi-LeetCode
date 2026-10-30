---
title: "2475. 数组中不等三元组的数目"
aliases: ["yiduobo的每日leetcode 2475.数组中不等三元组的数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/588496620"
zhihu_id: "588496620"
zhihu_title: "yiduobo的每日leetcode 2475.数组中不等三元组的数目"
question_id: "2475"
question: "数组中不等三元组的数目"
problem_url: "https://leetcode.cn/problems/number-of-unequal-triplets-in-array/"
difficulty: "Easy"
created: "2022-12-02T02:37:48+08:00"
updated: "2022-12-02T02:37:48+08:00"
upvotes: 0
comments: 0
---

# 2475. 数组中不等三元组的数目

> **[yiduobo的每日leetcode 2475.数组中不等三元组的数目](https://zhuanlan.zhihu.com/p/588496620) · 知乎 · 2022-12-02 · 赞同 0**
> 力扣：[2475. 数组中不等三元组的数目](https://leetcode.cn/problems/number-of-unequal-triplets-in-array/) · Easy · 灵茶山艾府：[两种非暴力做法：排序 / 哈希表](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2475.数组中不等三元组的数目

[力扣](https://leetcode.cn/problems/number-of-unequal-triplets-in-array/)

题目的数据规模非常小，使用暴力法是完全可行的。我在这里使用的逆向思维的做法，考虑有多少不符合条件的三元组。

一共有C(n, 3)个三元组，其中不符合条件的三元组可以分成其中只有两个数相等以及三个数都相等这两种情况。为了避免重复计算，在这里需要先使用一个哈希表cnt统计每种数出现的次数，接下来枚举每种数字num，对于cnt[num]：

1、如果cnt[num] >\= 2，那么就有C(cnt[num], 2) \* (n - cnt[num])种不符合条件的三元组，包含了两个cnt[num]以及一个其他整数

2、如果cnt[num] >\= 3，那么就有C(cnt[num], 3)种完全由cnt[num]组成的不符合条件的三元组

对于每种num，都使用总三元组数目减去上面这两种情况中不符合条件的三元组数目，最后剩下的就是题目要求的答案了。

最后附上python代码：

```python
class Solution(object):
    def unequalTriplets(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        cnt = {}
        for num in nums:
            cnt[num] = cnt.get(num, 0) + 1
        
        res = n * (n - 1) * (n - 2) / 6
        for num in cnt:
            if cnt[num] >= 2:
                res -= (cnt[num] * (cnt[num] - 1) / 2) * (n - cnt[num])
                if cnt[num] >= 3:
                    res -= (cnt[num] * (cnt[num] - 1) * (cnt[num] - 2) / 6)
        
        return res
```
