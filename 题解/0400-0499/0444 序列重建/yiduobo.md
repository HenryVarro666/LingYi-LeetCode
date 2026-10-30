---
title: "444. 序列重建"
aliases: ["yiduobo的每日leetcode 444.序列重建"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/599771611"
zhihu_id: "599771611"
zhihu_title: "yiduobo的每日leetcode 444.序列重建"
question_id: "444"
question: "序列重建"
problem_url: "https://leetcode.cn/problems/sequence-reconstruction/"
created: "2023-01-17T23:35:41+08:00"
updated: "2023-01-17T23:35:41+08:00"
upvotes: 0
comments: 0
---

# 444. 序列重建

> **[yiduobo的每日leetcode 444.序列重建](https://zhuanlan.zhihu.com/p/599771611) · 知乎 · 2023-01-17 · 赞同 0**
> 力扣：[444. 序列重建](https://leetcode.cn/problems/sequence-reconstruction/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

444.序列重建

[力扣](https://leetcode.cn/problems/sequence-reconstruction/)

非常经典的拓扑排序问题。

将所有的n个整数视为有向图中的点，接下来遍历题目给出的sequences，为序列中相邻的数字间建立有向边，这样一来就得到了一个有向图。接下来对这个图做拓扑排序，若最终得到的序列是唯一的，且处理到了所有的n个点，那么就返回true，否则就返回false。

最后附上python代码：

```python
class Solution(object):
    def sequenceReconstruction(self, nums, sequences):
        """
        :type nums: List[int]
        :type sequences: List[List[int]]
        :rtype: bool
        """

        ind = {}
        g = {}
        for seq in sequences:
            if len(seq) == 1:
                if seq[0] not in ind:
                    ind[seq[0]] = 0
                continue

            for index in range(1, len(seq)):
                x, y = seq[index - 1], seq[index]
                if x not in g:
                    g[x] = set()
                if x not in ind:
                    ind[x] = 0
                if y not in ind:
                    ind[y] = 0
                
                if y not in g[x]:
                    ind[y] += 1
                    g[x].add(y)
        
        q = []
        for x in ind:
            if ind[x] == 0:
                q.append(x)
        
        if len(q) > 1:
            return False
        
        head, tail = 0, 1
        while head < tail:
            for now in q[head : tail]:
                for next in g.get(now, set()):
                    ind[next] -= 1
                    if ind[next] == 0:
                        q.append(next)
            
            head, tail = tail, len(q)
            if tail - head > 1:
                return False

        if len(q) != len(ind):
            return False
        
        return q == nums
```
