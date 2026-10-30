---
title: "2334. 元素值大于变化阈值的子数组"
aliases: ["yiduobo的每日leetcode 2334.元素值大于变化阈值的子数组"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/union-find", "leetcode/monotonic-stack", "题单/常用数据结构", "题单/单调栈", "题单/常用数据结构/七-并查集", "题单/单调栈/三-贡献法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/558839165"
zhihu_id: "558839165"
zhihu_title: "yiduobo的每日leetcode 2334.元素值大于变化阈值的子数组"
question_id: "2334"
question: "元素值大于变化阈值的子数组"
problem_url: "https://leetcode.cn/problems/subarray-with-elements-greater-than-varying-threshold/"
difficulty: "Hard"
rating: 2381
created: "2022-08-28T23:44:58+08:00"
updated: "2022-08-28T23:44:58+08:00"
upvotes: 0
comments: 0
---

# 2334. 元素值大于变化阈值的子数组

> **[yiduobo的每日leetcode 2334.元素值大于变化阈值的子数组](https://zhuanlan.zhihu.com/p/558839165) · 知乎 · 2022-08-28 · 赞同 0**
> 力扣：[2334. 元素值大于变化阈值的子数组](https://leetcode.cn/problems/subarray-with-elements-greater-than-varying-threshold/) · Hard · 灵茶山艾府：[两种做法：并查集 / 单调栈（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2334.元素值大于变化阈值的子数组

[力扣](https://leetcode.cn/problems/subarray-with-elements-greater-than-varying-threshold/)

由于nums和threshold都是不变的，因此可以先计算出min_k[i] \= threshold / nums[i] + 1，其含义是包含第i个数的合法子数组的最短长度，那么问题就变成了能否在min_k中找出一个子数组，其中的最小值大于等于这个子数组的长度。

一个自然的想法就是遍历min_k，想办法计算当min_k[index]作为其所在子数组的最小值时，这个子数组的最大长度。若这个长度大于等于min_k[index]，说明这个子数组就是合法的子数组。

为了高效求解这个子数组的长度，在这里就需要两个辅助数组left和right，其中left\[index\]表示在index左侧，且满足min_k\[left\[index\]\] \< min_k\[index\]的最大值，而right\[index\]则表示在index右侧，且满足min_k\[right\[index\]\] > min_k\[index\]的最大值。

left和right的求解是非常经典的问题，可以利用单调栈，正反两趟遍历分别求解，在这里就不展开了。

得到left和right后，以min_k[index]作为子数组的最小值时的最长子数组就是min_k[left[index] + 1]到min_k[right[index] - 1]之间这一段，其长度为right[index] - left[index] - 1。若这个长度大于等于min_k[index]，那么说明这个子数组是合法子数组，此时返回这个长度即可。

若遍历完整个min_k都没有找到合法子数组，那么说明无解，返回-1。

最后附上python代码：

```python
class Solution(object):
    def validSubarraySize(self, nums, threshold):
        """
        :type nums: List[int]
        :type threshold: int
        :rtype: int
        """

        min_k = [threshold / num + 1 for num in nums]
        n = len(nums)

        left = [-1] * n
        stack = []
        for index in range(n):
            while stack and min_k[stack[-1]] <= min_k[index]:
                stack.pop()
            
            if stack:
                left[index] = stack[-1]
            
            stack.append(index)
        
        right = [n] * n
        stack = []
        for index in range(n - 1, -1, -1):
            while stack and min_k[stack[-1]] <= min_k[index]:
                stack.pop()
            
            if stack:
                right[index] = stack[-1]
            
            stack.append(index)
        
        for index in range(n):
            if right[index] - left[index] - 1 >= min_k[index]:
                return min_k[index]
        
        return -1
```
