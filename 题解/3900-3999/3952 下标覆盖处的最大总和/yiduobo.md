---
title: "3952. 下标覆盖处的最大总和"
aliases: ["yiduobo的每日leetcode 3952.下标覆盖处的最大总和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/dynamic-programming", "题单/滑动窗口与双指针", "题单/动态规划", "题单/滑动窗口与双指针/六-分组循环", "题单/动态规划/六-状态机-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2047464748816529302"
zhihu_id: "2047464748816529302"
zhihu_title: "yiduobo的每日leetcode 3952.下标覆盖处的最大总和"
question_id: "3952"
question: "下标覆盖处的最大总和"
problem_url: "https://leetcode.cn/problems/maximum-total-value-of-covered-indices/"
difficulty: "Medium"
rating: 1763
created: "2026-06-09T00:14:48+08:00"
updated: "2026-06-09T00:14:51+08:00"
upvotes: 0
comments: 0
---

# 3952. 下标覆盖处的最大总和

> **[yiduobo的每日leetcode 3952.下标覆盖处的最大总和](https://zhuanlan.zhihu.com/p/2047464748816529302) · 知乎 · 2026-06-09 · 赞同 0**
> 力扣：[3952. 下标覆盖处的最大总和](https://leetcode.cn/problems/maximum-total-value-of-covered-indices/) · Medium · 灵茶山艾府：[两种方法：贪心 / 状态机 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3952.下标覆盖处的最大总和

<https://leetcode.cn/problems/maximum-total-value-of-covered-indices/description/>

题目给出一个长度为n的正整数数组nums以及一个长度为n的二进制字符串s。对于s[index]，若s[index]为'1'，表示index处有标记，反之则表示没有标记。

现在可以执行以下操作任意次：

- 选择一个之前处于非0的下标index处的标记，这个标记之前必须没有被移动过
- 将这个标记从index移动到index - 1

在执行完所有操作后，计算nums中有标记的下标位置的元素之和。问在最优地执行上面的操作后，这个和最大可能是多少。

首先可以明确的是，由于nums是正整数数组，因此不应该通过移动操作让两个标记重叠在同一个位置上，这样相当于浪费了那个被移动的标记。

另一方面，由于每个标记只能被移动至多一次，因此对于s中一段形如'011...11'的子串，执行上述的移动过程，相当于让这个0保持不变，或者与后续这一中的任意1进行交换。为了使得最终答案最大，在这里就相当于在这一段连续下标中找到nums最小的位置，然后将这个'0'移动到该位置。

基于这一点，就得到了一种贪心的算法：

遍历字符串，将其划分为若干个'011...11'组成的子串，在此过程中可能遇到相邻的'0'，这些'0'可以直接跳过。接下来对于每个'011...11'形的字符串，计算其在nums中对应子数组的元素之和，并找出其中的最小值，那么将'0'移动到最小值对应的下标后，这个子数组对最终答案的贡献，就相当于子数组之和减去这个最小值。将每个子数组的贡献累加起来即为最终答案。

另外，为了应对s以1开头的情况，可以假设在nums头部添加一个值为0的元素，在s的头部添加一个'0'，这样一来就可以顺利处理这种情况。

最后附上python代码：

```python
class Solution(object):
    def maxTotal(self, nums, s):
        """
        :type nums: List[int]
        :type s: str
        :rtype: int
        """
        
        mi = 0
        res = 0

        p = 0
        while p < len(nums):
            while p < len(nums) and s[p] == '0':
                mi = nums[p]
                p += 1

            if p == len(nums):
                break
            
            res += mi
            while p < len(nums) and s[p] == '1':
                mi = min(mi, nums[p])
                res += nums[p]
                p += 1
            
            res -= mi
        
        return res
```
