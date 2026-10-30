---
title: "1911. 最大子序列交替和"
aliases: ["yiduobo的每日leetcode 1911.最大子序列交替和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/dp", "leetcode/dp-2", "题单/动态规划", "题单/动态规划/六-状态机-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/482849082"
zhihu_id: "482849082"
zhihu_title: "yiduobo的每日leetcode 1911.最大子序列交替和"
question_id: "1911"
question: "最大交替子序列和"
problem_url: "https://leetcode.cn/problems/maximum-alternating-subsequence-sum/"
difficulty: "Medium"
rating: 1786
created: "2022-03-17T23:49:14+08:00"
updated: "2022-03-17T23:51:54+08:00"
upvotes: 1
comments: 0
---

# 1911. 最大子序列交替和

> **[yiduobo的每日leetcode 1911.最大子序列交替和](https://zhuanlan.zhihu.com/p/482849082) · 知乎 · 2022-03-17 · 赞同 1**
> 力扣：[1911. 最大交替子序列和](https://leetcode.cn/problems/maximum-alternating-subsequence-sum/) · Medium · 灵茶山艾府：[动态规划](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1911.最大子序列交替和

[力扣](https://leetcode-cn.com/problems/maximum-alternating-subsequence-sum/)

看上去应该是动态规划的题目，不过我在这里用的是贪心法。

在这里先说明贪心的依据。

首先，答案中的第一个数必然是nums中第一个山峰的值，证明可以分成两个部分。不妨设第一个山峰在nums中下标为p，那么：

1、若答案中的第一个数是nums[q]，且q \< p：

首先可以证明nums[p]肯定不是起负向作用的。若nums[p]起的是负向作用，那么截止到nums[p]最终答案必然是nums[q] - x1 + x2 - x3 + ... - nums[p]的形式。两两分组来看，就可以得到(nums[q] - x1) + (x2 - x3) + ... + (xk - nums[p])。由于nums[q]到nums[p]是山峰的单调不减区间，那么上面这个式子里面每一个括号都是非正的，那还不如全都不要。

接下来以nums[p]必然起正向作用为前提进行讨论。

同样地，若选择了nums[q]，那么到nums[p]为止地最终但必然是nums[q] - x1 + x2 - x3 + ... + nums[p]，同样是两两分组，可以发现，nums[p]之前的部分是没有存在的必要的。

2、若答案中的第一个数是nums[r]，且r > p：

如果最终答案里面的第一个数为nums[r]，那么必然有nums[r] > nums[p]，才有替换掉nums[p]的必要。而如果nums[r] > nums[p]，又由于nums[p]是山峰所在的位置，也就是说nums[p + 1]到nums[r - 1]之间必然存在一个数小于nums[p]，不妨记为nums[t]。那么此时相比于选择nums[r]作为第一个数，选择nums[p] , nums[t]，nums[r]这个子序列作为前三个数显然是更优的。

至此，就证明了答案中的第一个数是nums的第一个山峰。

对于答案中的第二个数而言，与第一个数恰好是完全相反的，那么可以简单推广得到答案中的第二个数必然是nums中的第一个山谷。

而对于答案中第三个数的选择，则可以认为是转化成了从nums中剔除了到第一个山谷为止的前缀之后的后缀子数组nums[p + 1:]来构造出最大子序列交替和的问题，那么此时可以认为又回到了问题一。

根据上面的结论，就可以一趟扫描，根据山峰山谷的状况依序填充答案，同时在每一个山峰加入后更新答案。在这里需要注意的是最后一段单调递增的数组可能会导致丢失掉最后一个山峰，因此可以在nums后加入一个0，从而保证最后一段单调递增数组也能被计算进来。

最后附上python代码：

```
class Solution(object):
    def maxAlternatingSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        now = 0
        l = 0
        nums.append(0)
        res = 0
        for index in range(1, len(nums)):
            if l & 1:
                if nums[index] > nums[index - 1]:
                    now -= nums[index - 1]
                    l += 1
            else:
                if nums[index] < nums[index - 1]:
                    now += nums[index - 1]
                    res = max(res, now)
                    l += 1

        return res
```
