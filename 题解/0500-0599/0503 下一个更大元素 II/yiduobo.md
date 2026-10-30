---
title: "503. 下一个更大元素II"
aliases: ["yiduobo的每日leetcode 503.下一个更大元素II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/monotonic-stack", "题单/单调栈", "题单/单调栈/一-单调栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/258948150"
zhihu_id: "258948150"
zhihu_title: "yiduobo的每日leetcode 503.下一个更大元素II"
question_id: "503"
question: "下一个更大元素 II"
problem_url: "https://leetcode.cn/problems/next-greater-element-ii/"
difficulty: "Medium"
created: "2020-09-24T20:39:55+08:00"
updated: "2020-09-24T20:39:55+08:00"
upvotes: 0
comments: 0
---

# 503. 下一个更大元素II

> **[yiduobo的每日leetcode 503.下一个更大元素II](https://zhuanlan.zhihu.com/p/258948150) · 知乎 · 2020-09-24 · 赞同 0**
> 力扣：[503. 下一个更大元素 II](https://leetcode.cn/problems/next-greater-element-ii/) · Medium · 灵茶山艾府：[【视频】单调栈的两种写法，附单调栈题单（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

503.下一个更大元素II <https://leetcode-cn.com/problems/next-greater-element-ii/>

又是求下一个更大元素的题目，同样可以使用之前用过的单调栈来进行求解，具体做法可以参考之前496题（传送门在这里[yiduobo：yiduobo的每日leetcode 496.下一个更大元素I](https://zhuanlan.zhihu.com/p/257283167)）。

这里最大的不同是nums是循环数组。对于循环数组，一种普遍的做法是将数组原样复制一遍，然后接在原始数组的后面。复制好之后，就可以对新得到的这个数组使用之前求下一个更大元素的做法了。

当然需要注意的一点是，最后只需要返回原始数组下一个更大元素即可。

最后附上python代码，我在实现的时候没有真的复制一遍nums，而是通过取模操作模拟复制nums之后的情形：

```python
class Solution(object):
    def nextGreaterElements(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        if not nums:
            return []

        stack = [nums[-1]]
        res = []
        l = len(nums)
        for index in range(l + l - 1, -1, -1):
            while stack and nums[index % l] >= nums[stack[-1] % l]:
                stack.pop()
            if index < len(nums):
                if stack:
                    res.append(nums[stack[-1] % l])
                else:
                    res.append(-1)
            stack.append(index)

        res.reverse()
        return res
```
