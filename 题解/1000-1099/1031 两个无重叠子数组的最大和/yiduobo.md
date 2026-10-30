---
title: "1031. 两个非重叠子数组的最大和"
aliases: ["yiduobo的每日leetcode 1031.两个非重叠子数组的最大和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/graph", "leetcode/enumeration", "leetcode/prefix-sum", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/零-常用枚举技巧", "题单/常用数据结构/一-前缀和", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/369604511"
zhihu_id: "369604511"
zhihu_title: "yiduobo的每日leetcode 1031.两个非重叠子数组的最大和"
question_id: "1031"
question: "两个无重叠子数组的最大和"
problem_url: "https://leetcode.cn/problems/maximum-sum-of-two-non-overlapping-subarrays/"
difficulty: "Medium"
rating: 1680
created: "2021-05-03T23:17:35+08:00"
updated: "2021-05-03T23:17:35+08:00"
upvotes: 0
comments: 0
---

# 1031. 两个非重叠子数组的最大和

> **[yiduobo的每日leetcode 1031.两个非重叠子数组的最大和](https://zhuanlan.zhihu.com/p/369604511) · 知乎 · 2021-05-03 · 赞同 0**
> 力扣：[1031. 两个无重叠子数组的最大和](https://leetcode.cn/problems/maximum-sum-of-two-non-overlapping-subarrays/) · Medium · 灵茶山艾府：[【图解】没有思路？一张图秒懂！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1031.两个非重叠子数组的最大和

[力扣](https://leetcode-cn.com/problems/maximum-sum-of-two-non-overlapping-subarrays/)

方便期间，我们称长度为L的数组为数组L，长度为M的数组为数组M，那么我们可以先规定L在M的前面，求解这种情况下的最优解，然后再反过来，规定M在L的前面并求解这种情况下的最有解。这两个情况的求解方式是完全一致的，因此不妨先考虑L在M前面的情况。

一个自然的想法是从头开始枚举L的位置，然后在剩下的数里面找出M。设A的长度为N，那么整个流程就是：

L的起点为0，那么此时的L为A[0]到A[L - 1]，接下来从A[L]到A[N - 1]中找到M

L的起点为1，那么此时的L为A[1]到A[L]，接下来从A[L + 1]到A[N - 1]中找到M

L的起点为2，那么此时的L为A[2]到A[L + 1]，接下来从A[L + 2]到A[N - 1]中找到M

...

L的起点为N - M - L，那么此时的L为A[N - M - L]到A[N - M - 1]，接下来从A[N - M]到A[N - 1]中找到M

关注这个求解过程，其中数组L是一开始就固定住了，可以通过前缀和很快求解。而对于M的求解则有一种违和感：随着L的移动，M的求解范围是每次减小1直到固定住的

一个自然的想法是将上面这个过程反过来：

L的起点为N - M - L，那么此时的L为A[N - M - L]到A[N - M - 1]，接下来从A[N - M]到A[N - 1]中找到M

L的起点为N - M - L - 1，那么此时的L为A[N - M - L - 1]到A[N - M - 2]，接下来从A[N - M - 1]到A[N - 1]中找到M

L的起点为N - M - L - 2，那么此时的L为A[N - M - L - 2]到A[N - M - 2]，接下来从A[N - M - 2]到A[N - 1]中找到M

...

L的起点为0，那么此时的L为A[0]到A[L - 1]，接下来从A[L]到A[N - 1]中找到M

观察前两步对M的求解：

第一步是从A[N - M]到A[N - 1]中求解M

第二步是从A[N - M - 1]到A[N - 1]中求解M

可以发现，第二步相比第一步实际上就多出以A[N - M - 1]作为M的起点这种情况

同样地，第三步相比第二步实际上就多出了A[N - M - 2]作为M的起点这种情况

更一般的，对于上面的求解过程，每一步相比于前一步实际上就多出了一种选择

那么我们可以维护一个遍历max_m，表示当前M的最大值，那么每一步我们都只需要通过对比当前max_m以及新多出来的这一种选择，就可以更新得到当前的max_m，并通过max_m以及当前固定好了的L来更新最终答案了。

上面这个过程是从后往前进行枚举的，不太直观，因此我们也可以调换一下，从前往后进行枚举。依然是假设L在M的前面，那么我们可以从头开始枚举M的结束位置end_pos，那么此时M的位置就固定为A[end_pos - M + 1]到A[end_pos]，而L则需要在A[0]到A[end_pos - M]之间求解。同样地，此时维护一个max_l，每次向后移动end_pos时，相比上一轮都会多出A[end_pos - M - L + 1]到A[end_pos - M]这个选项，于是每一轮只需要对比max_l以及这个新增的选项来更新max_l，然后使用max_l以及M更新答案即可。

对于M在L前面的情况也可以如法炮制。由于两种情况在计算时并没有冲突的地方，那么也可以只进行一趟循环，将两种情况都给处理了。

最后附上python代码：

```python
class Solution(object):
    def maxSumTwoNoOverlap(self, A, L, M):
        """
        :type A: List[int]
        :type L: int
        :type M: int
        :rtype: int
        """

        s = [A[0]]
        for num in A[1:]:
            s.append(s[-1] + num)
        
        max_l = s[L - 1]
        max_m = s[M - 1]
        res = s[L + M - 1]
        for end_pos in range(L + M, len(A)):
            max_l = max(max_l, s[end_pos - M] - s[end_pos - M - L])
            max_m = max(max_m, s[end_pos - L] - s[end_pos - M - L])
            res = max(res, max_l + s[end_pos] - s[end_pos - M], max_m + s[end_pos] - s[end_pos - L])
        
        return res
```
