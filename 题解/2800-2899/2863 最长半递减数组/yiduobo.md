---
title: "2863. 最长半递减数组"
aliases: ["yiduobo的每日leetcode 2863.最长半递减数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/661688216"
zhihu_id: "661688216"
zhihu_title: "yiduobo的每日leetcode 2863.最长半递减数组"
question_id: "2863"
question: "最长半递减数组"
problem_url: "https://leetcode.cn/problems/maximum-length-of-semi-decreasing-subarrays/"
created: "2023-10-17T00:43:22+08:00"
updated: "2023-10-17T00:43:22+08:00"
upvotes: 0
comments: 0
---

# 2863. 最长半递减数组

> **[yiduobo的每日leetcode 2863.最长半递减数组](https://zhuanlan.zhihu.com/p/661688216) · 知乎 · 2023-10-17 · 赞同 0**
> 力扣：[2863. 最长半递减数组](https://leetcode.cn/problems/maximum-length-of-semi-decreasing-subarrays/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2863.最长半递减数组

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximum-length-of-semi-decreasing-subarrays/)

题目的数据规模较大，不能直接使用暴力算法，需要想办法优化处理。

对于大小比较类的问题，由于不用关心具体的数值而只需要关注数值间的相对大小，因此可以先将数组排序，然后从小到大建立数值到下标的映射，这样一来就可以将数值的范围限定在10^5之内，接下来就可以使用树状数组等数据结构，将数值大小视为下标来进行计算。

除此之外，大小比较类的问题也可以尝试利用单调性来进行优化，本题如果利用单调性来求解可以得到一个非常漂亮的处理方法。

首先，对于答案数组的左边界，若存在两个下标i、j满足i \< j且nums[i] >\= nums[j]，那么j就不可能成为答案数组的左边界。理由也很简单，因为半递减数组必须满足右边界的值小于左边界的值，而对于nums[j]而言，如果使用nums[i]来替代nums[j]作为左边界必然可以得到一个更长的半递减数组，因此j在这里就没用了。

更进一步的，答案数组的备选左边界必然是一个单调递增的数组，于是可以一趟遍历，使用栈来计算所有可能的备选左边界，不妨记为stack。

接下来则需要为stack中的左边界寻找最优的可用右边界，在这里则可以再次利用单调性，从后往前寻找栈中每个左边界对应的右边界。对于当前遍历到的右边界，若当前栈顶元素小于等于这个右边界对应的数值，由于栈中其他元素的值都小于栈顶元素的值，因此当前的右边界无法匹配任意一个备选左边界，此时就应该向左移动一步，考虑下一个右边界。反之，则应该使用当前遍历到的右边界来匹配栈顶元素，此时应该弹出栈顶元素，但是不应该移动向左移动右边界。

上述过程可能使得某个左边界匹配到在这个左边界更左侧的右边界，这显然是不合法的，但是此时计算的区间长度是负数，如果设置答案的初始值为0的话，就不会用这种情况更新答案。

最后附上python代码：

```python
class Solution(object):
    def maxSubarrayLength(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        stack = []
        n = len(nums)
        for index in range(n):
            if not stack or nums[stack[-1]] < nums[index]:
                stack.append(index)

        res = 0
        for index in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] > nums[index]:
                res = max(res, index - stack.pop() + 1)
            
            if not stack:
                break
        
        return res
```
