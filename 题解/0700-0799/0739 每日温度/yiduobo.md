---
title: "739. 每日温度"
aliases: ["yiduobo的每日leetcode 739.每日温度"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/monotonic-stack", "题单/单调栈", "题单/LeetCode-热题-100", "题单/单调栈/一-单调栈", "题单/LeetCode-热题-100/栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/336650931"
zhihu_id: "336650931"
zhihu_title: "yiduobo的每日leetcode 739.每日温度"
question_id: "739"
question: "每日温度"
problem_url: "https://leetcode.cn/problems/daily-temperatures/"
difficulty: "Medium"
created: "2020-12-13T19:48:11+08:00"
updated: "2020-12-13T19:48:11+08:00"
upvotes: 0
comments: 0
---

# 739. 每日温度

> **[yiduobo的每日leetcode 739.每日温度](https://zhuanlan.zhihu.com/p/336650931) · 知乎 · 2020-12-13 · 赞同 0**
> 力扣：[739. 每日温度](https://leetcode.cn/problems/daily-temperatures/) · Medium · 灵茶山艾府：[【视频】讲清楚为什么要用单调栈！两种写法：从右到左 / 从左到右](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

739.每日温度

[力扣](https://leetcode-cn.com/problems/daily-temperatures/)

题目给出一个数组，要求找出对每个数字而言，下一个更大的数字的位置。

对于数组中的某一位T[p]而言，其可以用来更新T[0]到T[p - 1]中还未找到答案的位置，同时其自身也需要储存起来，等待后续的数字来更新p这一位的答案。对于T[0]到T[p - 1]中还未找到答案的这些位置，其中数值小于T[p]的所有位置的下一个更大数字的位置就是p，而剩下的这些位置上的数字则必然大于等于T[p]，于是很自然想到使用单调栈来维护这些数字。

于是现在的具体做法就是从头开始往后一趟扫描，对于当前的T[index]，若其大于栈顶元素，说明栈顶元素的下一个更大数字的位置就是index，那么将其从栈中弹出，更新答案，然后重复此过程直到T[index]小于等于栈顶元素。

最后附上python代码：

```python
class Solution(object):
    def dailyTemperatures(self, T):
        """
        :type T: List[int]
        :rtype: List[int]
        """

        stack = [0]
        res = [0] * len(T)
        for index in range(1, len(T)):
            while stack and T[index] > T[stack[-1]]:
                res[stack[-1]] = index - stack[-1]
                stack.pop()
            stack.append(index)

        return res
```
