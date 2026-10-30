---
title: "85. 最大矩形"
aliases: ["yiduobo的每日leetcode 85.最大矩形"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/monotonic-stack", "题单/单调栈", "题单/单调栈/二-矩形"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/134180401"
zhihu_id: "134180401"
zhihu_title: "yiduobo的每日leetcode 85.最大矩形"
question_id: "85"
question: "最大矩形"
problem_url: "https://leetcode.cn/problems/maximal-rectangle/"
difficulty: "Hard"
created: "2020-04-23T22:55:55+08:00"
updated: "2020-11-17T22:23:03+08:00"
upvotes: 1
comments: 2
---

# 85. 最大矩形

> **[yiduobo的每日leetcode 85.最大矩形](https://zhuanlan.zhihu.com/p/134180401) · 知乎 · 2020-04-23 · 赞同 1**
> 力扣：[85. 最大矩形](https://leetcode.cn/problems/maximal-rectangle/) · Hard · 灵茶山艾府：[直接调用 84 题代码解决（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

85.最大矩形<https://leetcode-cn.com/problems/maximal-rectangle/>

在完成了上一题之后，这一题的思路就比较简单了。

我们可以从上往下，每次关注前k行。具体来说就是以第k行为基底，将竖着的连续的1看做上一题中的柱子，将题目转化成上一题。当然，这里悬空的柱子是不能要的。

例如样例，我们可以将其看成

1 0 1 0 0

2 0 2 1 1

3 1 3 2 2

4 0 0 3 0

于是，答案就是3 1 3 2 2这一行的后三个柱子3 2 2组成的矩形面积6。

从上往下枚举每一行，然后每行都是从左往右先计算柱子的高度，再从左往右计算矩形面积，因此最终的时间复杂度为O(mn)。

最后附上python代码：

```python
class Solution(object):
    def maximalRectangle(self, matrix):
        """
        :type matrix: List[List[str]]
        :rtype: int
        """

        if not matrix:
            return 0

        m = len(matrix)
        n = len(matrix[0])

        res = 0
        height = [0] * n
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == '1':
                    height[j] += 1
                else:
                    height[j] = 0
            stack = []
            for j in range(n):
                while len(stack) > 0 and height[stack[-1]] > height[j]:
                    if len(stack) > 1:
                        res = max(res, height[stack[-1]]* (j - stack[-2] - 1))
                    else:
                        res = max(res, height[stack[-1]] * j)
                    stack.pop()

                stack.append(j)

            if len(stack) > 0:
                for j in range(len(stack)):
                    if j == 0:
                        res = max(res, height[stack[j]] * (stack[-1] + 1))
                    else:
                        res = max(res, height[stack[j]] * (stack[-1] - stack[j - 1]))

        return res
```
