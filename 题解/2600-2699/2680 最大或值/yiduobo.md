---
title: "2680. 最大或值"
aliases: ["yiduobo的每日leetcode 2680.最大或值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/bit-manipulation", "题单/动态规划", "题单/位运算", "题单/贪心算法", "题单/动态规划/专题-前后缀分解", "题单/位运算/三-与或-AND/OR-的性质", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/649537138"
zhihu_id: "649537138"
zhihu_title: "yiduobo的每日leetcode 2680.最大或值"
question_id: "2680"
question: "最大或值"
problem_url: "https://leetcode.cn/problems/maximum-or/"
difficulty: "Medium"
rating: 1912
created: "2023-08-12T00:23:20+08:00"
updated: "2023-08-12T00:23:20+08:00"
upvotes: 0
comments: 0
---

# 2680. 最大或值

> **[yiduobo的每日leetcode 2680.最大或值](https://zhuanlan.zhihu.com/p/649537138) · 知乎 · 2023-08-12 · 赞同 0**
> 力扣：[2680. 最大或值](https://leetcode.cn/problems/maximum-or/) · Medium · 灵茶山艾府：[两种方法：前后缀分解 / O(1) 空间（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2680.最大或值

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximum-or/description/)

题目给出一个数组，可以对其中的数进行若干次左移操作，要求使得数组元素取或的结果最大。

首先可以明确的是，这些左移操作都应该集中在同一个数字上，因为这样才能使得某个1被推到更高的数位上，从而使得最终结果最大。但是需要注意的是，在这里并不一定是选择最大的数进行左移操作，例如6和4，二者的二进制表示分别为110和100，将110左移一位之后得到的是1100，与100取或的话相当于浪费掉了这个1，反过来将100左移一位之后得到的是1000，与110取或的话就得到了1110，是更优的选择。

由于无法直接确定应该对哪个数执行左移，那么就需要一趟遍历，枚举这个执行左移操作的数，此时的结果就相当于数组的一个前缀或值，当前数的左移，以及数组的一个后缀或值，这三者再取或。为了高效求解，在这里就可以先正反两趟遍历，预处理出数组所有前缀或值以及后缀或值，这样一来就可以在O(n)的时间内解决问题了。

最后附上python代码：

```python
class Solution(object):
    def maximumOr(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        prefix = []
        suffix = []

        n = len(nums)
        for index in range(n):
            prefix.append(nums[index])
            if index > 0:
                prefix[-1] |= prefix[-2]
        
        for index in range(n - 1, -1, -1):
            suffix.append(nums[index])
            if index < n - 1:
                suffix[-1] |= suffix[-2]
        
        suffix.reverse()

        res = 0
        for index in range(n):
            v = nums[index] << k
            if index > 0:
                v |= prefix[index - 1]
            if index < n - 1:
                v |= suffix[index + 1]
        
            res = max(res, v)
        
        return res
```
