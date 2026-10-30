---
title: "2460. 对数组执行操作"
aliases: ["yiduobo的每日leetcode 2460.对数组执行操作"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/586493916"
zhihu_id: "586493916"
zhihu_title: "yiduobo的每日leetcode 2460.对数组执行操作"
question_id: "2460"
question: "对数组执行操作"
problem_url: "https://leetcode.cn/problems/apply-operations-to-an-array/"
difficulty: "Easy"
created: "2022-11-25T03:37:04+08:00"
updated: "2022-11-25T03:37:04+08:00"
upvotes: 0
comments: 0
---

# 2460. 对数组执行操作

> **[yiduobo的每日leetcode 2460.对数组执行操作](https://zhuanlan.zhihu.com/p/586493916) · 知乎 · 2022-11-25 · 赞同 0**
> 力扣：[2460. 对数组执行操作](https://leetcode.cn/problems/apply-operations-to-an-array/) · Easy · 灵茶山艾府：[O(1) 空间写法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2460.对数组执行操作

<https://leetcode.cn/problems/apply-operations-to-an-array/>

首先一趟遍历，按照题目的要求完成翻倍和清零操作，接下来再一趟遍历，将所有非零的值移动到数组靠前的位置即可。

最后附上python代码：

```python
class Solution(object):
    def applyOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        n = len(nums)
        for index in range(n - 1):
            if nums[index] == nums[index + 1]:
                nums[index] += nums[index]
                nums[index + 1] = 0
        
        p = 0
        for index in range(n):
            if nums[index] == 0 and p < n:
                if p <= index:
                    p = index + 1
                while p < n and nums[p] == 0:
                    p += 1
                
                if p < n:
                    nums[index], nums[p] = nums[p], nums[index]
                    p += 1
        
        return nums
```
