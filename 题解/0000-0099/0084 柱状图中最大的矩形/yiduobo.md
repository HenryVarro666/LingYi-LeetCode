---
title: "84. 柱状图中最大的矩形"
aliases: ["yiduobo的每日leetcode 84.柱状图中最大的矩形"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/monotonic-stack", "题单/单调栈", "题单/LeetCode-热题-100", "题单/单调栈/二-矩形", "题单/LeetCode-热题-100/栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/134175409"
zhihu_id: "134175409"
zhihu_title: "yiduobo的每日leetcode 84.柱状图中最大的矩形"
question_id: "84"
question: "柱状图中最大的矩形"
problem_url: "https://leetcode.cn/problems/largest-rectangle-in-histogram/"
difficulty: "Hard"
created: "2020-04-23T22:55:28+08:00"
updated: "2020-04-23T22:55:28+08:00"
upvotes: 0
comments: 0
---

# 84. 柱状图中最大的矩形

> **[yiduobo的每日leetcode 84.柱状图中最大的矩形](https://zhuanlan.zhihu.com/p/134175409) · 知乎 · 2020-04-23 · 赞同 0**
> 力扣：[84. 柱状图中最大的矩形](https://leetcode.cn/problems/largest-rectangle-in-histogram/) · Hard · 灵茶山艾府：[一步步优化：从三次遍历到一次遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

84.柱状图中最大的矩形<https://leetcode-cn.com/problems/largest-rectangle-in-histogram/>

很有意思的运用单调性的问题。

首先可以明确的是，答案矩形的高一定就是其中某个柱子的高，且这个柱子是构成答案的柱子中最矮的那一个。

那么对于一个柱子index，如果用它的高h[index]作为答案的高，那么其左右边界一定满足

h[left - 1] \< h[index]

h[left], h[left + 1], h[left + 2], ... , h[index - 1] >\= h[index]

h[right], h[right - 1], h[right - 2], ... ,h[index + 1] >\= h[index]

h[right + 1] \< h[index]

于是，问题就变成了对于每个柱子，找到left与right的位置，然后计算最终的答案即可。

这里直接暴力计算，时间复杂度为O(n^2)，当然使用分治可以将其优化到O(nlogn)，但依然不是最优解。

我们可以从左往右开始考虑。

首先第一个柱子，高度为height[0]，那么其左边界就是自身，只需要寻找右边界。

接下来对于height[1]：

1）如果height[1] \< height[0]，那么此时0的右边界就找到了，可以计算以height[0]为高的矩形的面积了。同时，1的左边界就是0，此时问题变成了寻找1的右边界。

2）如果height[1] >\= height[0]，那么1的左边界为其自身，而0与1的右边界都需要继续往后寻找。此时，变成了对一个单调递增的list寻找右边界的问题。实际上，情况1）也可以看作是一个单调的list寻找右边界的问题，只是list中只有一个元素。

于是，我们可以将问题看做一个单调递增的list，其满足

height\[list\[0\]\] \< height\[list\[1\]\] \< ... \< height\[-1\]

然后我们需要寻找list中这些柱子的右边界的问题。

不妨设我们现在探索到了height[k]：

1、若height\[k\]大于等于height\[list\[-1\]\]。说明list中的柱子依然没找到右边界，同时还需要再将k加入到这个list中，一起寻找右边界。

2、否则就有height\[k\] \< height\[list\[-p\]\] \< height\[list\[-p + 1\]\] \< ... \< height\[list\[-1\]\]，即list中height大于height\[k\]的这些柱子都已经找到了右边界，可以开始逐一计算这些柱子所能形成的矩形的面积。

我们从list[-1]开始计算。显然其右边界就是k - 1，然后左边界就是list[-2] + 1。当然如果此时不存在list[-2]，那么左边界就是0了。计算完list[-1]之后，可以将其从list中pop出去，然后用同样的方法计算新的list[-1]。

完成上面的计算之后，此时的list要么为空，要么满足height\[list\[-1\]\] \<\= height\[k\]。此时还是需要将k加入到list中，之后就依然还是寻找list的右边界的问题。

3、当探索到了末尾，list不为空的话，说明list中的这些柱子的右边界就是list[-1]。左边界的计算方式与上面相同，设当前柱子为list[index]，那么左边界就是list[index - 1] + 1。同样，若index为0，那么左边界就是0。此时将list中剩下的柱子所能形成的矩形面积计算出来即可。

由于每个柱子最多进出list一次，因此最终的时间复杂度为O(n)。可以发现，上面所说的list实际上就是一个栈stack。

最后附上python代码：

```python
class Solution(object):
    def largestRectangleArea(self, heights):
        """
        :type heights: List[int]
        :rtype: int
        """

        stack = []
        res = 0
        for index, height in enumerate(heights):
            if not stack or heights[stack[-1]] <= height:
                stack.append(index)
            else:
                while len(stack) > 0 and heights[stack[-1]] > height:
                    if len(stack) > 1:
                        width = index - stack[-2] - 1
                    else:
                        width = index
                    res = max(res, heights[stack[-1]] * width)
                    stack.pop()
                stack.append(index)

        if stack:
            for index in range(len(stack)):
                if index == 0:
                    res = max(res, heights[stack[index]] * (stack[-1] + 1))
                else:
                    res = max(res, heights[stack[index]] * (stack[-1] - stack[index - 1]))

        return res
```
