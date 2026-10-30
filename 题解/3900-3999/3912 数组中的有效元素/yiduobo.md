---
title: "3912. 数组中的有效元素"
aliases: ["yiduobo的每日leetcode 3912.数组中的有效元素"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "题单/动态规划", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2032600184916534303"
zhihu_id: "2032600184916534303"
zhihu_title: "yiduobo的每日leetcode 3912.数组中的有效元素"
question_id: "3912"
question: "数组中的有效元素"
problem_url: "https://leetcode.cn/problems/valid-elements-in-an-array/"
difficulty: "Easy"
rating: 1273
created: "2026-04-28T23:24:44+08:00"
updated: "2026-04-28T23:24:45+08:00"
upvotes: 1
comments: 0
---

# 3912. 数组中的有效元素

> **[yiduobo的每日leetcode 3912.数组中的有效元素](https://zhuanlan.zhihu.com/p/2032600184916534303) · 知乎 · 2026-04-28 · 赞同 1**
> 力扣：[3912. 数组中的有效元素](https://leetcode.cn/problems/valid-elements-in-an-array/) · Easy · 灵茶山艾府：[O(n) 做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3912.数组中的有效元素

<https://leetcode.cn/problems/valid-elements-in-an-array/description/>

题目给出一个整数数组nums。

若其中的nums[index]至少满足一下一个条件，就认为它是有效元素。

- 它严格大于左侧的所有元素
- 它严格大于右侧的所有元素

要求返回所有有效元素组成的数组，顺序与它们在nums中出现的顺序相同。

题目中有效元素的条件，实际上就是要求这个元素要么是以该元素结尾的前缀的最大值，要么是以该元素开头的后缀的最大值。于是可以正反两趟遍历，在遍历过程中维护前缀/后缀的最大值ma。对于当前遍历到的nums[index]，若其大于ma，那么就说nums[index]是有效的，此时需要将index标记为有效的，然后将ma更新为nums[index]。反之，则不需要进行任何操作，继续向后遍历即可。

遍历完成后，再正序遍历所有下标，将所有被标记为有效的下标对应的元素加入到答案数组中即可。

最后附上python代码：

```python
class Solution(object):
    def findValidElements(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        
        n = len(nums)
        flag = [False] * n
        ma = 0
        for index in range(n):
            if nums[index] > ma:
                flag[index] = True
                ma = nums[index]
        
        ma = 0
        for index in range(n - 1, -1, -1):
            if nums[index] > ma:
                flag[index] = True
                ma = nums[index]
        
        res = []
        for index in range(n):
            if flag[index]:
                res.append(nums[index])
        
        return res
```
