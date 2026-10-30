---
title: "2355. 你能拿走的最大图书数量"
aliases: ["yiduobo的每日leetcode 2355.你能拿走的最大图书数量"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "leetcode/monotonic-stack", "leetcode/dp", "leetcode/dp-2", "题单/动态规划", "题单/单调栈", "题单/动态规划/十一-优化-DP", "题单/单调栈/一-单调栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/630214203"
zhihu_id: "630214203"
zhihu_title: "yiduobo的每日leetcode 2355.你能拿走的最大图书数量"
question_id: "2355"
question: "你能拿走的最大图书数量"
problem_url: "https://leetcode.cn/problems/maximum-number-of-books-you-can-take/"
difficulty: "Hard"
created: "2023-05-18T00:32:22+08:00"
updated: "2023-05-18T00:32:22+08:00"
upvotes: 0
comments: 0
---

# 2355. 你能拿走的最大图书数量

> **[yiduobo的每日leetcode 2355.你能拿走的最大图书数量](https://zhuanlan.zhihu.com/p/630214203) · 知乎 · 2023-05-18 · 赞同 0**
> 力扣：[2355. 你能拿走的最大图书数量](https://leetcode.cn/problems/maximum-number-of-books-you-can-take/) · Hard · 灵茶山艾府：[单调栈 + DP + 一次遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2355.你能拿走的最大图书数量

[力扣](https://leetcode.cn/problems/maximum-number-of-books-you-can-take/)

题目要求拿走的书是一个严格递增的子数组，那么首先可以确定的是，最终答案的最后一项必然是全拿，因为对于任何没有全拿的情况，全拿的话显然也是可行的，且拿走的书显然更多。

有了这个结论，很自然会往枚举子数组的最后一项books[i]，求解以books[i]为结尾的和最大的严格递增子数组。

当最后这一项为books[i]时，最理想的情况就是

books[i - 1] >\= books[i] - 1

books[i - 2] >\= books[i] - 2

...

books[0] >\= books[i] - i

在这种情况下，将会得到一个以books[i] - i为首项，books[i]为末项的等差数列。但是在实际操作中，可能出现两种断裂的情况：

1、books[i] \< i

这种情况下，等差数列的起点不能是books[i] - i，但是最终答案任然是等差数列。这种情况下，可以拿的书的数量就是(1 + books[i]) \* (books[i]) / 2

2、中间存在某项j不够大，也就是books[j] \< books[i] - (i - j)

这种情况下，就需要用到动态规划了。令f[i]表示以books[i]为结尾的最大严格递增子数组和，而j是i左侧最近的满足books[j] \< books[i] - (i - j)的下标，那么f[i]就由f[j]以及books[i] - (i - j) + 1到books[i]的等差数列组成，于是就有

f[i] \= f[j] + (books[i] - (i - j) + 1 + books[i]) \* (i - j) / 2

此时的问题就是如何找到最靠后的j。观察books[j] \< books[i] - (i - j)，移项后可得books[j] - j \< books[i] - i，那么如果在最开始将原始数组中的每个数减去其所在的下标，问题就转化成了左侧第一个更小的数的下标问题，可以使用单调栈将每个下标位置i对应的j都预处理出来。

另外，以上两种情况可能叠加出现，应该优先处理情况2，再处理情况1。

最后附上python代码：

```python
class Solution(object):
    def maximumBooks(self, books):
        """
        :type books: List[int]
        :rtype: int
        """

        n = len(books)
        pre = [-1] * n
        stack = []
        for index in range(n - 1, -1, -1):
            while stack and books[stack[-1]] - stack[-1] >= books[index] - index:
                pre[stack[-1]] = index
                stack.pop()
            
            stack.append(index)
        

        f = [books[0]]
        for index in range(1, n):
            if pre[index] == -1:
                start = max(1, books[index] - index)
                f.append((start + books[index]) * (books[index] - start + 1) / 2)
            else:
                start = max(1, books[index] - (index - pre[index]) + 1)
                f.append(f[pre[index]] + (start + books[index]) * (books[index] - start + 1) / 2)

        return max(f)
```
