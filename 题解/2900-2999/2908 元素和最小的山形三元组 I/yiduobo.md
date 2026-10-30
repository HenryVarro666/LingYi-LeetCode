---
title: "2908. 元素和最小的山形三元组I & 2909. 元素和最小的山形三元组II"
aliases: ["yiduobo的每日leetcode 2908.元素和最小的山形三元组I && 2909.元素和最小的山形三元组II", "2908. 元素和最小的山形三元组I", "2909. 元素和最小的山形三元组II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/enumeration", "leetcode/di-tui", "leetcode/medium", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/零-常用枚举技巧", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/664215345"
zhihu_id: "664215345"
zhihu_title: "yiduobo的每日leetcode 2908.元素和最小的山形三元组I && 2909.元素和最小的山形三元组II"
question_id: ["2908", "2909"]
question: ["元素和最小的山形三元组 I", "元素和最小的山形三元组 II"]
problem_url: ["https://leetcode.cn/problems/minimum-sum-of-mountain-triplets-i/", "https://leetcode.cn/problems/minimum-sum-of-mountain-triplets-ii/"]
difficulty: ["Easy", "Medium"]
rating: 1479
created: "2023-10-31T04:17:46+08:00"
updated: "2023-10-31T04:17:46+08:00"
upvotes: 0
comments: 0
---

# 2908. 元素和最小的山形三元组I & 2909. 元素和最小的山形三元组II

> **[yiduobo的每日leetcode 2908.元素和最小的山形三元组I && 2909.元素和最小的山形三元组II](https://zhuanlan.zhihu.com/p/664215345) · 知乎 · 2023-10-31 · 赞同 0**
> 力扣：[2908. 元素和最小的山形三元组 I](https://leetcode.cn/problems/minimum-sum-of-mountain-triplets-i/) · Easy · 灵茶山艾府：[O(n) 前后缀分解，附题单（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)
> 力扣：[2909. 元素和最小的山形三元组 II](https://leetcode.cn/problems/minimum-sum-of-mountain-triplets-ii/) · Medium · 灵茶山艾府：[枚举中间 + 前后缀分解（Python/Java/C++/Go/JS/Rust）](../2909%20元素和最小的山形三元组%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2908.元素和最小的山形三元组I

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-sum-of-mountain-triplets-i/)

2909.元素和最小的山形三元组II

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-sum-of-mountain-triplets-ii/)

题目要求找出下标三元组i、j、k，满足i \< j \< k，同时nums[i]和nums[k]都小于nums[j]，问这三个元素之和的最小值是多少。

两题的题设完全相同，2909的数据规模较大，不能使用暴力法。对于这类三元组问题，依然还是枚举中间位置j，去寻找最优的i和k。

题目希望三数之和最小，又要求nums[i]和nums[k]都小于nums[j]，恰好是完全契合的目标。更具体的说，若nums[0]到nums[j - 1]之间最小值小于nums[j]，那么就应该选择这个数作为nums[i]才能使得最终答案最小；反之若最小值大于等于nums[j]，那么说明在0到j - 1找不出可用的i。可以发现，这实际上就是一个前缀最小值的问题，而对于k的选取则是后缀最小值的问题。于是可以正反两趟遍历，分别求解前缀最小值数组prefix以及后缀最小值数组suffix，然后再遍历j，通过prefix[j - 1]、nums[j]、suffix[j + 1]来更新答案。

最后附上python代码：

```python
class Solution(object):
    def minimumSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        prefix = [nums[0]]
        for index in range(1, n):
            prefix.append(min(prefix[-1], nums[index]))
        
        suffix = [nums[-1]]
        for index in range(n - 2, -1, -1):
            suffix.append(min(suffix[-1], nums[index]))
        suffix.reverse()

        res = -1
        for index in range(1, n - 1):
            if prefix[index - 1] < nums[index] and suffix[index + 1] < nums[index]:
                if res == -1 or res > prefix[index - 1] + nums[index] + suffix[index + 1]:
                    res = prefix[index - 1] + nums[index] + suffix[index + 1]
        
        return res
```
