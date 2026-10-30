---
title: "3862. 找出最小平衡下标"
aliases: ["yiduobo的每日leetcode 3862.找出最小平衡下标"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/prefix-sum", "题单/滑动窗口与双指针", "题单/动态规划", "题单/滑动窗口与双指针/三-单序列双指针", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2014135609103503820"
zhihu_id: "2014135609103503820"
zhihu_title: "yiduobo的每日leetcode 3862.找出最小平衡下标"
question_id: "3862"
question: "找出最小平衡下标"
problem_url: "https://leetcode.cn/problems/find-the-smallest-balanced-index/"
difficulty: "Medium"
rating: 1697
created: "2026-03-11T02:01:40+08:00"
updated: "2026-03-11T02:01:45+08:00"
upvotes: 0
comments: 1
---

# 3862. 找出最小平衡下标

> **[yiduobo的每日leetcode 3862.找出最小平衡下标](https://zhuanlan.zhihu.com/p/2014135609103503820) · 知乎 · 2026-03-11 · 赞同 0**
> 力扣：[3862. 找出最小平衡下标](https://leetcode.cn/problems/find-the-smallest-balanced-index/) · Medium · 灵茶山艾府：[两种方法：前后缀分解 / 相向双指针（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3862.找出最小平衡下标

<https://leetcode.cn/problems/find-the-smallest-balanced-index/description/>

题目给出一个整数数组nums，对于其中的某个下标index，若nums[0]到nums[index - 1]这些元素之和，恰好等于nums[index + 1]到nums[-1]这些元素之积，就称index为平衡下标。

需要注意，若index左侧没有元素，那么左侧之和视为0；若右侧没有元素，则右侧之积视为1。

问最小的平衡下标是什么，若不存在，则返回-1。

题目中的左侧之和以及右侧之积实际上可以视为前缀和以及后缀积，于是可以先正反两趟遍历，计算出前缀和数组s以及后缀积数组m，接下来再一趟遍历，通过s和m确认当前的index是否为平衡下标即可。

需要注意的是，在计算m的过程中，可能会出现乘积非常巨大的情况，一种可行的处理方式是若目前的后缀积已经大于整个数组之和，那么就将当前后缀积以及接下来的其他后缀积都视为数组之和加1。

最后附上python代码：

```python
class Solution(object):
    def smallestBalancedIndex(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        s = [0]
        for v in nums:
            s.append(s[-1] + v)
        
        m = [1]
        for v in nums[::-1]:
            if m[-1] == s[-1] + 1:
                m.append(m[-1])
            else:
                m.append(m[-1] * v)
                if m[-1] > s[-1]:
                    m[-1] = s[-1] + 1
        m.reverse()
        
        for index in range(len(nums)):
            left = s[index]
            right = m[index + 1]
            if left == right:
                return index
        
        return -1
```
