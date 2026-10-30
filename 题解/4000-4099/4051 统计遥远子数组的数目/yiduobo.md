---
title: "4051. 统计遥远子数组的数目"
aliases: ["yiduobo的每日leetcode 4051.统计遥远子数组的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-indexed-tree", "leetcode/binary-search", "leetcode/ordered-set", "leetcode/prefix-sum", "leetcode/sorting", "题单/常用数据结构", "题单/常用数据结构/一-前缀和", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2083340211304534555"
zhihu_id: "2083340211304534555"
zhihu_title: "yiduobo的每日leetcode 4051.统计遥远子数组的数目"
question_id: "4051"
question: "统计遥远子数组的数目"
problem_url: "https://leetcode.cn/problems/count-subarrays-with-distant-sums/"
difficulty: "Hard"
rating: 2140
created: "2026-09-15T23:53:54+08:00"
updated: "2026-09-15T23:53:57+08:00"
upvotes: 2
comments: 0
---

# 4051. 统计遥远子数组的数目

> **[yiduobo的每日leetcode 4051.统计遥远子数组的数目](https://zhuanlan.zhihu.com/p/2083340211304534555) · 知乎 · 2026-09-15 · 赞同 2**
> 力扣：[4051. 统计遥远子数组的数目](https://leetcode.cn/problems/count-subarrays-with-distant-sums/) · Hard · 灵茶山艾府：[前缀和 + 值域树状数组 / 有序集合（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4051.统计遥远子数组的数目

<https://leetcode.cn/problems/count-subarrays-with-distant-sums/description/>

题目给出一个整数数组nums，以及两个整数goal和k。

对于一个子数组，若其中所有元素之和与goal的绝对差至少为k，则称其为遥远子数组。

问遥远子数组的数量。

题目要求判断区间和不在特定范围内的子数组的数目，那么在这里可以先做两个转化。

首先区间和自然是转化为前缀和之差来进行处理，也就是说，对于每个前缀s，需要找出其左侧有多少个前缀和p满足s - p的结果，与goal的绝对差至少为k。

另一方面，判断不在特定范围内需要查两头，那么就不如改为判断在特定范围内子数组的数目，然后用总的子数组的数目减去这个值。

综合起来，问题就变成了对于前缀和s，计算其左侧有多少个前缀和p满足goal - k \<\= s - p \<\= goal + k。

将这个式子变形，就变成了计算前缀和s的左右有多少个前缀和p满足s - goal - k \<\= p \<\= s - goal + k。

对于这个问题，由于只需要关心大小关系，而不需要关心具体的差值，因此在这里就可以先将所有出现过的前缀和s以及对应的s - goal + k与s - goal - k收集起来进行离散化，按照大小顺序映射到1到m，接下来建立一个大小为m的树状数组，就可以在logm的时间内完成每个s对应的查询了。

最后附上python代码：

```python
class Solution(object):
    def distantSubarrays(self, nums, goal, k):
        """
        :type nums: List[int]
        :type goal: int
        :type k: int
        :rtype: int
        """
        
        nums_set = set([0])
        s = 0
        for v in nums:
            s += v
            nums_set.add(s)
            nums_set.add(s - goal + k)
            nums_set.add(s - goal - k)

        nums_list = sorted(list(nums_set))
        mapping = {}
        for index, v in enumerate(nums_list):
            mapping[v] = index + 1

        m = len(mapping)
        f = [0] * (m + 1)
        
        def add(x):
            while x <= m:
                f[x] += 1
                x += x & -x
        
        def get(x):
            v = 0
            while x > 0:
                v += f[x]
                x -= x & -x
            return v
        
        s = 0
        res = 0
        add(mapping[0])
        for v in nums:
            s += v
            if s - goal + k > s - goal - k:
                res += get(mapping[s - goal + k] - 1) - get(mapping[s - goal - k])
            add(mapping[s])
        
        return len(nums) * (len(nums) + 1) // 2 - res
```
