---
title: "556. 下一个更大元素III"
aliases: ["yiduobo的每日leetcode 556.下一个更大元素III"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/265209728"
zhihu_id: "265209728"
zhihu_title: "yiduobo的每日leetcode 556.下一个更大元素III"
question_id: "556"
question: "下一个更大元素III"
problem_url: "https://leetcode.cn/problems/next-greater-element-iii/"
created: "2020-10-12T23:20:15+08:00"
updated: "2020-10-12T23:20:15+08:00"
upvotes: 0
comments: 0
---

# 556. 下一个更大元素III

> **[yiduobo的每日leetcode 556.下一个更大元素III](https://zhuanlan.zhihu.com/p/265209728) · 知乎 · 2020-10-12 · 赞同 0**
> 力扣：[556. 下一个更大元素III](https://leetcode.cn/problems/next-greater-element-iii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

556.下一个更大元素III <https://leetcode-cn.com/problems/next-greater-element-iii/>

题目要求下一个元素中的所有数字与n完全一致，那么如果将n的每一位分离出来，看成一个排列的话，题目实际上就是求下一个排列是什么，于是可以参考这一题的做法（传送门在这里[yiduobo：yiduobo的每日leetcode 31.下一个排列](https://zhuanlan.zhihu.com/p/119442273)），求出下一个排列。最后还需要判断其是否大于n，且是否在int范围之内。

最后附上python代码：

```python
class Solution(object):
    def nextGreaterElement(self, n):
        """
        :type n: int
        :rtype: int
        """

        nums = []
        tmp = n
        while tmp:
            nums.append(tmp % 10)
            tmp /= 10
        nums.reverse()

        pos = 0
        for index in range(len(nums) - 1, 0, -1):
            if nums[index] > nums[index - 1]:
                pos = index
                break
        if pos == 0:
            for index in range(len(nums) / 2):
                tmp = nums[index]
                nums[index] = nums[len(nums) - index - 1]
                nums[len(nums) - index - 1] = tmp
        else:
            pos -= 1
            sawp_pos = None
            sawp_num = None
            for index in range(len(nums) - 1, pos, -1):
                if nums[index] > nums[pos]:
                    if sawp_num is None or sawp_num > nums[index]:
                        sawp_num = nums[index]
                        sawp_pos = index

            tmp = nums[pos]
            nums[pos] = nums[sawp_pos]
            nums[sawp_pos] = tmp

            for index in range((len(nums) - pos - 1) / 2):
                tmp = nums[pos + index + 1]
                nums[pos + index + 1] = nums[len(nums) - index - 1]
                nums[len(nums) - index - 1] = tmp

        res = 0
        for index in range(len(nums)):
            res = res * 10 + nums[index]
        if res > 2147483647 or res <= n:
            return -1
        return res
```
