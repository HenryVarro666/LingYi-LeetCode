---
title: "2035. 将数组分成两个数组并最小化数组和的差"
aliases: ["yiduobo的每日leetcode 2035.将数组分成两个数组并最小化数组和的差"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/binary-search", "leetcode/sorting", "leetcode/meet-in-the-middle", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/四-回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/508778210"
zhihu_id: "508778210"
zhihu_title: "yiduobo的每日leetcode 2035.将数组分成两个数组并最小化数组和的差"
question_id: "2035"
question: "将数组分成两个数组并最小化数组和的差"
problem_url: "https://leetcode.cn/problems/partition-array-into-two-arrays-to-minimize-sum-difference/"
difficulty: "Hard"
rating: 2490
created: "2022-05-03T16:05:11+08:00"
updated: "2022-05-03T16:05:11+08:00"
upvotes: 1
comments: 0
---

# 2035. 将数组分成两个数组并最小化数组和的差

> **[yiduobo的每日leetcode 2035.将数组分成两个数组并最小化数组和的差](https://zhuanlan.zhihu.com/p/508778210) · 知乎 · 2022-05-03 · 赞同 1**
> 力扣：[2035. 将数组分成两个数组并最小化数组和的差](https://leetcode.cn/problems/partition-array-into-two-arrays-to-minimize-sum-difference/) · Hard · 灵茶山艾府：[折半枚举+排序+二分](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2035.将数组分成两个数组并最小化数组和的差

[力扣](https://leetcode-cn.com/problems/partition-array-into-two-arrays-to-minimize-sum-difference/)

由于单个数值的上限可以到10^7，那么使用背包问题的解法也是不行的，另一方面，由于n最大可以取到15，也就是说原数组最多可能有30个数，直接使用状态压缩动态规划或者dfs都是行不通的。

不过对于这个30，还是有处理办法的。

之前碰到过一个类似的问题，是从最多40个数中选一些数出来使得最接近goal。具体做法是40个数分两组，然后计算两组中各种可能选择。这一步预处理的复杂度为O(2^n)，由于n最多为20，所以还是可以接受的。

得到两个序列后，问题就变成了两个序列中各选出一个数使得选择的两个数最接近goal，此时利用单调性，使用双指针就可以在线性的时间内找出最终答案。具体的细节可以参考

[yiduobo：yiduobo的每日leetcode 1755.最接近目标值的子序列和](https://zhuanlan.zhihu.com/p/459169163)

对于本题，同样是将这个30分成两组，然后计算两组中各种可能的选择。接下来也同样是两个序列中各选一个数，使得选择的两个数最接近goal。本题的goal就是所有数的总和除以2。不过相对前面这题还是有些区别，因为本题要求两个序列中选择的数恰好是n个。

对于这个问题，一个自然的想法就是在预处理时按照选择的数的个数分别储存，接下来从0开始枚举到n。对于当前枚举到的cnt，可以认为从前半部分中选择了cnt个数，从后半部分中选择了n - cnt个数，分别从预处理的结果中选出对应的序列，然后再尝试选择两个数即可。

最后附上python代码：

```python
class Solution(object):
    def minimumDifference(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        s = sum(nums)
        target = s / 2

        n = len(nums) / 2
        first_part = [set([0])]
        for index in range(n):
            first_part.append(set())
            for cnt in range(index, -1, -1):
                for num in first_part[cnt]:
                    first_part[cnt + 1].add(num + nums[index])
        
        second_part = [set([0])]
        for index in range(n):
            second_part.append(set())
            for cnt in range(index, -1, -1):
                for num in second_part[cnt]:
                    second_part[cnt + 1].add(num + nums[index + n])

        res = None
        for first_cnt in range(n + 1):
            second_cnt = n - first_cnt
            first_nums = sorted(first_part[first_cnt])
            second_nums = sorted(second_part[second_cnt], reverse = True)

            first_p = second_p = 0

            while first_p < len(first_nums) and second_p < len(second_nums):
                now = first_nums[first_p] + second_nums[second_p]
                if now == target:
                    return s - target - target
                if now < target:
                    if res is None or res > s - now - now:
                        res = s - now - now
                    first_p += 1
                else:
                    if res is None or res > now - (s - now):
                        res = now - (s - now)
                    second_p += 1

        return res
```
