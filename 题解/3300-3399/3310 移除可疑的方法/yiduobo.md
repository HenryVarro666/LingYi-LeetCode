---
title: "3310. 移除可疑的方法"
aliases: ["yiduobo的每日leetcode 3310.移除可疑的方法"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/graph", "题单/图论算法", "题单/图论算法/一-图的遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1489902891"
zhihu_id: "1489902891"
zhihu_title: "yiduobo的每日leetcode 3310.移除可疑的方法"
question_id: "3310"
question: "移除可疑的方法"
problem_url: "https://leetcode.cn/problems/remove-methods-from-project/"
difficulty: "Medium"
rating: 1711
created: "2024-10-17T00:30:59+08:00"
updated: "2024-10-17T00:30:59+08:00"
upvotes: 0
comments: 0
---

# 3310. 移除可疑的方法

> **[yiduobo的每日leetcode 3310.移除可疑的方法](https://zhuanlan.zhihu.com/p/1489902891) · 知乎 · 2024-10-17 · 赞同 0**
> 力扣：[3310. 移除可疑的方法](https://leetcode.cn/problems/remove-methods-from-project/) · Medium · 灵茶山艾府：[DFS 标记可疑方法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3310.移除可疑的方法

[. - 力扣（LeetCode）](https://leetcode.cn/problems/remove-methods-from-project/description/)

题目给出两个整数n和k，表示有编号从0到n - 1的n个方法，其中方法k存在bug。另外给出一个二维整数数组invocations，其中invocations\[i\] \= \[a\[i\], b\[i\]\]表示方法a\[i\]调用了方法b\[i\]。对于方法k，以及所有被它直接或者间接调用的方法，都被称为可疑方法。

如果所有的可疑方法都没有被其他正常的方法调用过，那么就需要将所有的可疑方法移除，否则不移除任何方法。问最终剩下的方法有哪些。

根据题意，所有被方法k直接或者间接调用的方法都是可疑方法，那么就可以通过invocations建立有向图，然后从k开始做bfs，所有遍历到的方法都是可疑方法。

另外，题目还要求所有可疑方法都没有被正常方法调用过，在这里可以通过有向图中的入度来进行判断。

在建图时更新所有方法的入度，每个方法的入度就代表这个方法被多少其他方法调用过。接下来先遍历所有可疑方法，将被当前可疑方法调用过的方法的入度减去1，然后再次遍历所有可疑方法，若当前可疑方法的入度不为0，说明依然存在正常方法在调用当前可疑方法，无法进行删除，应该直接返回所有方法。若不存在这样的方法，则将所有可疑方法删除后返回。

最后附上python代码：

```python
class Solution(object):
    def remainingMethods(self, n, k, invocations):
        """
        :type n: int
        :type k: int
        :type invocations: List[List[int]]
        :rtype: List[int]
        """

        bugs = set()
        bugs.add(k)

        g = [set() for _ in range(n)]
        ind = [0] * n
        for x, y in invocations:
            if y not in g[x]:
                g[x].add(y)
                ind[y] += 1
            
        q = [k]
        head, tail = 0, 1
        while head < tail:
            for x in q[head : tail]:
                for y in g[x]:
                    if y not in bugs:
                        bugs.add(y)
                        q.append(y)
            
            head, tail = tail, len(q)

        for x in bugs:
            for y in g[x]:
                ind[y] -= 1
        
        flag = True
        for x in bugs:
            if ind[x] > 0:
                flag = False
        
        res = []
        for x in range(n):
            if x not in bugs or not flag:
                res.append(x)
        
        return res
```
