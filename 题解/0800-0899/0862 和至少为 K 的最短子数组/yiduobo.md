---
title: "862. 和至少为K的最短子数组"
aliases: ["yiduobo的每日leetcode 862.和至少为K的最短子数组"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/queue", "leetcode/prefix-sum", "leetcode/monotonic-queue", "leetcode/shuang-duan-dui-lie", "题单/常用数据结构", "题单/常用数据结构/四-队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/349820443"
zhihu_id: "349820443"
zhihu_title: "yiduobo的每日leetcode 862.和至少为K的最短子数组"
question_id: "862"
question: "和至少为 K 的最短子数组"
problem_url: "https://leetcode.cn/problems/shortest-subarray-with-sum-at-least-k/"
difficulty: "Hard"
rating: 2307
created: "2021-02-08T21:52:57+08:00"
updated: "2021-02-08T21:52:57+08:00"
upvotes: 2
comments: 0
---

# 862. 和至少为K的最短子数组

> **[yiduobo的每日leetcode 862.和至少为K的最短子数组](https://zhuanlan.zhihu.com/p/349820443) · 知乎 · 2021-02-08 · 赞同 2**
> 力扣：[862. 和至少为 K 的最短子数组](https://leetcode.cn/problems/shortest-subarray-with-sum-at-least-k/) · Hard · 灵茶山艾府：[两张图秒懂单调队列（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

862.和至少为K的最短子数组

[力扣](https://leetcode-cn.com/problems/shortest-subarray-with-sum-at-least-k/)

对于连续子数组和的问题，常见的做法是利用前缀和，那么对于当前的前缀和s[index]，需要在s[0]到s[index - 1]中找出比s[index]小K的最大的下标。

一个自然的想法就是利用某种数据结构储存s[0]到s[index - 1]中的某些值，此时可以发现两个性质：

1、若当前的s[index] - s[p] >\= K，那么s[p]就无需再储存。因为对于后续的q > index而言，即使满足s[q] - s[p] >\= K，从p到q这一段的长度显然是大于p到index这一段的，换言之就是此时以p开头的子数组就不可能成为最终答案了，因此无需再储存s[p]

2、若存在p \< index，且s[p] >\= s[index]，那么对于后续的q > index，当s[q] - s[p] >\= K时，必然有s[q] - s[index] >\= K，而p到q这一段的长度显然大于index到q的长度，因此以p开头的子数组就不可能成为最终答案，因此无需再储存s[p]

对于这上面这两个性质，性质1需要淘汰掉数据结构头部的s，而性质2则需要淘汰掉数据结构尾部的s，综合起来就应该利用双端队列来储存s。

到了这里，就有了完整的做法：

利用双端队列q维护前缀和，初始值为[0, -1]，表示前缀和为0，得出当前前缀和的下标为-1。接下来从头到尾遍历数组，计算前缀和。对于当前的前缀和s[index]：

1、若q的头部元素满足s[index] - q[0][0] >\= K，那么q[0][1]到index这一段就是合法的子数组，此时应该利用index - q[0][1]来更新答案，同时将q[0]弹出队列。重复该操作直到q为空或者s[index] - q[0][0] \< K。

2、若q的尾部元素满足s[index] \<\= q[-1][0]，那么将q[-1]弹出队列。重复该操作直到q为空或者s[index] > q[-1][0]。

3、将[s[index], index]加入到q的尾部

最后附上python代码：

```python
class Solution(object):
    def shortestSubarray(self, A, K):
        """
        :type A: List[int]
        :type K: int
        :rtype: int
        """

        q = deque([[0, -1]])
        s = 0
        res = len(A) + 1
        for index, num in enumerate(A):
            s += num
            while q and s - q[0][0] >= K:
                res = min(res, index - q[0][1])
                q.popleft()
            while q and s <= q[-1][0]:
                q.pop()
            q.append([s, index])

        if res == len(A) + 1:
            res = -1
        return res
```
