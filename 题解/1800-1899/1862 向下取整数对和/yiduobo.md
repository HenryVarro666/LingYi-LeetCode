---
title: "1862. 向下取整数对和"
aliases: ["yiduobo的每日leetcode 1862.向下取整数对和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/prefix-sum", "题单/常用数据结构", "题单/数学算法", "题单/常用数据结构/一-前缀和", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/473221794"
zhihu_id: "473221794"
zhihu_title: "yiduobo的每日leetcode 1862.向下取整数对和"
question_id: "1862"
question: "向下取整数对和"
problem_url: "https://leetcode.cn/problems/sum-of-floored-pairs/"
difficulty: "Hard"
rating: 2170
created: "2022-02-27T17:36:59+08:00"
updated: "2022-02-27T17:36:59+08:00"
upvotes: 0
comments: 0
---

# 1862. 向下取整数对和

> **[yiduobo的每日leetcode 1862.向下取整数对和](https://zhuanlan.zhihu.com/p/473221794) · 知乎 · 2022-02-27 · 赞同 0**
> 力扣：[1862. 向下取整数对和](https://leetcode.cn/problems/sum-of-floored-pairs/) · Hard · 灵茶山艾府：[值域前缀和+枚举分母和商](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1862.向下取整数对和

[力扣](https://leetcode-cn.com/problems/sum-of-floored-pairs/)

首先，由于nums的规模比较大，那么直接两两枚举所有数对显然是行不通的。不过注意到每个具体的数的大小最多只到10^5，那么在这里可以采用类似筛法的思路，枚举除数与向下取整后的结果。

对于当前枚举到的除数num以及倍数multi，大小处于num \* multi到num \* (multi + 1) - 1之间的数除以num向下取整后的结果才会是multi，也就是说在这里实际上就是要求nums中有多少个数位于区间[num \* multi, num \* (multi + 1) - 1]之间，那么在这里可以使用前缀和或者后缀和来进行优化。

我在这里采用的是后缀和，即令cnt_dict[num]表示数组中大于等于num的数有多少，那么计算落在区间[num \* multi, num \* (multi + 1) - 1]的数的个数就是cnt_dict[num \* multi] - cnt_dict[num \* (multi + 1)]。在这里采用后缀和的理由是对于当前枚举到的num，由于是作为除数，因此不需要关心小于num的数，所以在这里处理的顺序应该是按照num的大小从大到小处理，在处理的同时使用当前的数更新cnt数组以便比num更小的数来使用。

另一方面，nums中有重复的数，因此在处理时应该将这些数收集起来一起处理，否则时间复杂度就有问题了。

最后附上python代码：

```python
class Solution(object):
    def sumOfFlooredPairs(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        sorted_nums = sorted(nums)
        n = len(sorted_nums)
        max_num = sorted_nums[-1]
        p = n - 1
        bound = max_num
        mod = 10 ** 9 + 7
        res = 0
        cnt_dict = {}
        while p >= 0:
            prev_pos = p - 1
            while prev_pos >= 0 and sorted_nums[prev_pos] == sorted_nums[p]:
                prev_pos -= 1
            
            cnt = p - prev_pos

            for num in range(bound, sorted_nums[p], -1):
                if num != max_num:
                    cnt_dict[num] = cnt_dict[num + 1]
                else:
                    cnt_dict[num] = 0

            cnt_dict[sorted_nums[p]] = cnt
            if sorted_nums[p] < max_num:
                cnt_dict[sorted_nums[p]] += cnt_dict[sorted_nums[p] + 1]
            bound = sorted_nums[p] - 1

            last = sorted_nums[p]
            multi = 1
            step = max_num / sorted_nums[p]
            while multi < step:
                now = last + sorted_nums[p]
                res += cnt * (cnt_dict[last] - cnt_dict[now]) * multi
                res %= mod
                last = now
                multi += 1
            
            res += cnt * cnt_dict[last] * multi
            res %= mod

            p = prev_pos
        
        return res
```
