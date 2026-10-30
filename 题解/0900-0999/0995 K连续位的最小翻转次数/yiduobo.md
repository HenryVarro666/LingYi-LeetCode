---
title: "995. K连续位的最小翻转次数"
aliases: ["yiduobo的每日leetcode 995.K连续位的最小翻转次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/365206605"
zhihu_id: "365206605"
zhihu_title: "yiduobo的每日leetcode 995.K连续位的最小翻转次数"
question_id: "995"
question: "K连续位的最小翻转次数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-k-consecutive-bit-flips/"
created: "2021-04-15T22:18:22+08:00"
updated: "2021-04-15T22:18:22+08:00"
upvotes: 0
comments: 0
---

# 995. K连续位的最小翻转次数

> **[yiduobo的每日leetcode 995.K连续位的最小翻转次数](https://zhuanlan.zhihu.com/p/365206605) · 知乎 · 2021-04-15 · 赞同 0**
> 力扣：[995. K连续位的最小翻转次数](https://leetcode.cn/problems/minimum-number-of-k-consecutive-bit-flips/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

995.K连续位的最小翻转次数

[力扣](https://leetcode-cn.com/problems/minimum-number-of-k-consecutive-bit-flips/)

由于题目的操作是翻转，那么对于每一个长度为K的连续子数组而言，其要么不翻转，要么就翻转一次。如果从两端开始进行翻转，很容易发现实际上如果有解，那么翻转的操作是已经固定下来的。例如我们从数组的头部开始，设当前处理到第i位，那么若A[i]等于0，我们就翻转A[i]到A[i + k - 1]，否则就继续向后考察A[i + 1]。

直接模拟这个翻转过程的时间复杂度为O(nk)，其中n为A的长度，这个复杂度是比较高的。

此时的问题是对于A[i]，我们如何高效地知道在处理完A[0]到A[i - 1]之后，A[i]当前的值是0还是1。一个自然的想法就是将其变为动态区间问题，即每次翻转视为对某段区间加1或者减1，那么使用各种logn的数据结构是可以解决的。不过注意到这里对区间的操作只有两种状态，那么我们可以使用类似差分系统的思想，维护一个变量cnt表示当前的A[i]之前经历过多少次翻转。若我们在之前的某处A[j]进行了翻转，我们就应该将cnt加上1，同时在A[j + k - 1]设置标记，当处理到A[j + k - 1]时，由A[j]带来的这次翻转就结束了，此时应该将cnt减去1。

于是现在就有了一种做法，从头开始向后遍历数组A，同时维护一个变量cnt表示当前位置经历过的翻转次数，对于当前的A[i]，若当前的A[i]加上cnt为奇数，那么说明在经历过A[0]到A[i - 1]的操作后，此时的A[i]变成了1，无需进行翻转，直接向后继续考察A[i +1]；否则说明此时需要执行翻转。

若此时的i >\= n - k + 1，说明无法再翻转，返回-1；否则就应该翻转A[i]到A[i + k - 1]，于是将答案加上1，同时将cnt加上1，然后还需要在A[i + k - 1]这里做上标记，表示此处是某次翻转的终结。

最后若A[i]处有标记，说明在A[i - k + 1]处进行过翻转，到A[i]结束，因此还需要将cnt减1。

最后附上python代码：

```python
class Solution(object):
    def minKBitFlips(self, A, K):
        """
        :type A: List[int]
        :type K: int
        :rtype: int
        """

        n = len(A)
        end_pos = [0] * n
        reverse_cnt = 0
        res = 0
        for index, num in enumerate(A):
            if (num + reverse_cnt) % 2 == 0:
                if index >= n - K + 1:
                    return -1
                reverse_cnt += 1
                res += 1
                end_pos[index + K - 1] = 1
            
            reverse_cnt -= end_pos[index]
        
        return res
```
