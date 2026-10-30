---
title: "801. 使序列递增的最小交换次数"
aliases: ["yiduobo的每日leetcode 801.使序列递增的最小交换次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "leetcode/dp", "leetcode/dp-2", "题单/动态规划", "题单/动态规划/六-状态机-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/342666335"
zhihu_id: "342666335"
zhihu_title: "yiduobo的每日leetcode 801.使序列递增的最小交换次数"
question_id: "801"
question: "使序列递增的最小交换次数"
problem_url: "https://leetcode.cn/problems/minimum-swaps-to-make-sequences-increasing/"
difficulty: "Hard"
rating: 2066
created: "2021-01-07T21:22:27+08:00"
updated: "2021-01-07T21:22:27+08:00"
upvotes: 0
comments: 0
---

# 801. 使序列递增的最小交换次数

> **[yiduobo的每日leetcode 801.使序列递增的最小交换次数](https://zhuanlan.zhihu.com/p/342666335) · 知乎 · 2021-01-07 · 赞同 0**
> 力扣：[801. 使序列递增的最小交换次数](https://leetcode.cn/problems/minimum-swaps-to-make-sequences-increasing/) · Hard · 灵茶山艾府：[动态规划：考虑相邻元素的大小关系（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

801.使序列递增的最小交换次数

[力扣](https://leetcode-cn.com/problems/minimum-swaps-to-make-sequences-increasing/)

对于数组中的每一位，只有换或者不换两种选择，而选择的可能性只与前一位数字有关，因此可以使用动态规划来求解。令f[i]表示第i位不进行交换且合法的最少交换次数，g[i]表示第i位交换且合法的最少交换次数，由于第0位既可以交换也可以不交换，因此初始化f[0] \= 0，g[0] \= 1。接下来从1开始往后扫描，对于f[i]和g[i]：

1、若A[i] > A[i - 1]且B[i] > B[i - 1]：

此时的f[i - 1]表示没有交换A[i - 1]与B[i - 1]，那么我们可以选择不交换A[i]与B[i]，就可以得到合法状态f[i]，那么就有f[i] \= min(f[i], f[i - 1])

此时的g[i - 1]表示已经交换了A[i - 1]与B[i - 1]，那么我们可以选择交换A[i]与B[i]，就可以得到合法状态g[i]，那么就有g[i] \= min(g[i], g[i - 1] + 1)

2、若A[i] > B[i - 1]且B[i] > A[i - 1]：

此时的f[i - 1]表示没有交换A[i - 1]与B[i - 1]，那么我们可以选择交换A[i]与B[i]，就可以得到合法状态g[i]，那么就有g[i] \= min(g[i], f[i - 1] + 1)

此时的g[i - 1]表示已经交换了A[i - 1]与B[i - 1]，那么我们可以选择不交换A[i]与B[i]，就可以得到合法状态f[i]，那么就有f[i] \= min(f[i], g[i - 1])

逐步往后处理，最终min(f[-1], g[-1])就是答案。注意到状态转移过程中只与上一位有关，因此可以使用变量迭代来替换数组节省空间。

最后附上python代码：

```python
class Solution(object):
    def minSwap(self, A, B):
        """
        :type A: List[int]
        :type B: List[int]
        :rtype: int
        """

        n = len(A)
        last_same = 0
        last_swap = 1
        for index in range(1, n):
            now_same = now_swap = n + 1
            if A[index] > A[index - 1] and B[index] > B[index - 1]:
                now_same = min(now_same, last_same)
                now_swap = min(now_swap, last_swap + 1)
            if A[index] > B[index - 1] and B[index] > A[index - 1]:
                now_same = min(last_swap, now_same)
                now_swap = min(last_same + 1, now_swap)
            last_same, last_swap = now_same, now_swap
        
        return min(last_same, last_swap)
```
