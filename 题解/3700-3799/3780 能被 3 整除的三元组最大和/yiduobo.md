---
title: "3780. 能被3整除的三元组最大和"
aliases: ["yiduobo的每日leetcode 3780.能被3整除的三元组最大和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1986215023660516735"
zhihu_id: "1986215023660516735"
zhihu_title: "yiduobo的每日leetcode 3780.能被3整除的三元组最大和"
question_id: "3780"
question: "能被 3 整除的三元组最大和"
problem_url: "https://leetcode.cn/problems/maximum-sum-of-three-numbers-divisible-by-three/"
difficulty: "Medium"
created: "2025-12-22T21:52:16+08:00"
updated: "2025-12-22T21:52:17+08:00"
upvotes: 2
comments: 0
---

# 3780. 能被3整除的三元组最大和

> **[yiduobo的每日leetcode 3780.能被3整除的三元组最大和](https://zhuanlan.zhihu.com/p/1986215023660516735) · 知乎 · 2025-12-22 · 赞同 2**
> 力扣：[3780. 能被 3 整除的三元组最大和](https://leetcode.cn/problems/maximum-sum-of-three-numbers-divisible-by-three/) · Medium · 灵茶山艾府：[通用做法：二维 0-1 背包（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3780.能被3整除的三元组最大和

[3780. 能被 3 整除的三元组最大和 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-sum-of-three-numbers-divisible-by-three/description/)

题目给出一个正整数数组nums。

现在要求从中选出恰好三个数，使得它们的和能被3整除。问选出的三个数可能得到的最大和是多少。若不存在可行的选择方案，则返回0。

首先考察哪些三元组之和是3的倍数。对于这类问题，通常可以基于余数进行考虑，一共有四种情况：

- 3个数都是3的倍数
- 3个数都模3余1
- 3个数都模3余2
- 3个数模3的余数分别为0、1、2

于是只需一趟遍历，记录模3余0、1、2的元素中的最大值、次大值以及第三大值，然后取以上四种情况中和最大的那一种作为最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def maximumSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        first = [None] * 3
        second = [None] * 3
        third = [None] * 3
        for v in nums:
            r = v % 3
            if first[r] is None or first[r] < v:
                first[r], second[r], third[r] = v, first[r], second[r]
            elif second[r] is None or second[r] < v:
                second[r], third[r] = v, second[r]
            elif third[r] is None or third[r] < v:
                third[r] = v
        
        res = 0
        for r in range(3):
            if third[r] is not None:
                res = max(res, first[r] + second[r] + third[r])
        
        if first[0] is not None and first[1] is not None and first[2] is not None:
            res = max(res, first[0] + first[1] + first[2])
        
        return res
```
