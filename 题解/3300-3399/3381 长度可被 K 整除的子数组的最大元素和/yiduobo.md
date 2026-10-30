---
title: "3381. 长度可被K整除的子数组的最大元素和"
aliases: ["yiduobo的每日leetcode 3381.长度可被K整除的子数组的最大元素和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/dynamic-programming", "leetcode/prefix-sum", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/一-前缀和", "题单/动态规划/一-入门-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/29319625011"
zhihu_id: "29319625011"
zhihu_title: "yiduobo的每日leetcode 3381.长度可被K整除的子数组的最大元素和"
question_id: "3381"
question: "长度可被 K 整除的子数组的最大元素和"
problem_url: "https://leetcode.cn/problems/maximum-subarray-sum-with-length-divisible-by-k/"
difficulty: "Medium"
rating: 1943
created: "2025-03-11T01:51:22+08:00"
updated: "2025-03-11T01:51:34+08:00"
upvotes: 0
comments: 0
---

# 3381. 长度可被K整除的子数组的最大元素和

> **[yiduobo的每日leetcode 3381.长度可被K整除的子数组的最大元素和](https://zhuanlan.zhihu.com/p/29319625011) · 知乎 · 2025-03-11 · 赞同 0**
> 力扣：[3381. 长度可被 K 整除的子数组的最大元素和](https://leetcode.cn/problems/maximum-subarray-sum-with-length-divisible-by-k/) · Medium · 灵茶山艾府：[两种方法：前缀和 / 动态规划（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3381.长度可被K整除的子数组的最大元素和

[3381. 长度可被 K 整除的子数组的最大元素和 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-subarray-sum-with-length-divisible-by-k/description/)

题目给出一个整数数组nums以及一个整数k，要求从nums中找出一个非空子数组的最大和，这个子数组的长度必须为k的倍数。

当k \= 1时，题目就是经典的最大子段和问题。对于这个问题，除了常见的贪心法之外，还可以使用前缀和求解。具体来说，还是利用子数组和等于前缀和之差，若想要以当前index结尾的子数组和最大，那么就应该从0到index - 1之间选出一个最小的前缀和，使用当前的前缀和减去最小的前缀和即为以index结尾的最大子数组和，于是可以一趟遍历，一边计算前缀和，一边使用哈希表更新答案，然后使用当前的前缀和更新哈希表。

对于本题，实际上也可以采用类似的方法。对于当前的index，可以减的前缀只需满足结尾下标与index关于k同余，就可以使得前缀相减得到的子数组的长度为k的倍数。于是在这里可以使用一个哈希表s_dict记录每种下标余数对应的最小前缀和，接下来一趟遍历，一边计算前缀和s，一边利用下标计算对应的余数p，使用s - s_dict[p]更新答案，然后使用s更新s_dict[p]即可。

最后附上python代码：

```python
class Solution(object):
    def maxSubarraySum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        s_dict = {0: 0}
        res = None
        s = 0
        for index, v in enumerate(nums, 1):
            s += v
            p = index % k
            if p not in s_dict:
                s_dict[p] = s
            else:
                if res is None or res < s - s_dict[p]:
                    res = s - s_dict[p]
                s_dict[p] = min(s_dict[p], s)
        
        return res
```
