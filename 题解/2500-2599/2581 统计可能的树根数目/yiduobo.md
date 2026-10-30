---
title: "2581. 统计可能的树根数目"
aliases: ["yiduobo的每日leetcode 2581.统计可能的树根数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/hash-table", "leetcode/dynamic-programming", "leetcode/dfs", "leetcode/dp-2", "题单/动态规划", "题单/动态规划/十二-树形-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/642510411"
zhihu_id: "642510411"
zhihu_title: "yiduobo的每日leetcode 2581.统计可能的树根数目"
question_id: "2581"
question: "统计可能的树根数目"
problem_url: "https://leetcode.cn/problems/count-number-of-possible-root-nodes/"
difficulty: "Hard"
rating: 2228
created: "2023-07-10T03:03:27+08:00"
updated: "2023-07-10T03:03:27+08:00"
upvotes: 0
comments: 0
---

# 2581. 统计可能的树根数目

> **[yiduobo的每日leetcode 2581.统计可能的树根数目](https://zhuanlan.zhihu.com/p/642510411) · 知乎 · 2023-07-10 · 赞同 0**
> 力扣：[2581. 统计可能的树根数目](https://leetcode.cn/problems/count-number-of-possible-root-nodes/) · Hard · 灵茶山艾府：[换根 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2581.统计可能的树根数目

[力扣](https://leetcode.cn/problems/count-number-of-possible-root-nodes/)

题目的数据规模比较大，通过bfs求出以指定节点为根节点时猜测正确的数目至少需要O(n)的时间，不能直接枚举每个节点作为根节点然后bfs求解。

一种常见的思路是对于树中两个节点p和q，如果将根节点从p换成q后，能否利用p对应的结果高效计算出q对应的结果。在这里如果任意选取p和q，树的结构可能发生巨大变化，因此对p和q的选择也有一定的讲究。对于节点p，不妨先尝试选择其某个孩子节点q，那么当q成为根节点时，可以发现：

1、p的所有孩子节点中，除q之外的其他孩子节点与p的父子关系没有变化

2、q的所有孩子节点与q的父子关系没有变化，同时新增了p这个孩子

3、其他与p和q无关的节点不受任何影响

综合起来可以发现，将根节点从p移动到q实际上只会影响(p, q)这一组父子对，若之前以p为根节点时命中的猜测数量为p_hit，那么以q为根节点时命中的猜测数量q_hit只需在p_hit的基础上，增加关于边(p, q)的判断就可以计算得到了。更具体的，若之前p是q的父亲在猜测中，那么需要将q_hit减去1，另一方面，若q是p的父亲在猜测中，那么就需要将q_hit加上1。

有了上面的结论，就可以先通过一次bfs找出以某个节点为根节点时命中的猜测数量hit，例如先以0号节点为根节点。接下来，从0号节点开始再次进行bfs，对于遍历过程中遇到的所有父子对，利用上面的计算方法让根节点在父子之间传递并计算命中的猜测数量，并统计命中数量大于等于k的节点个数作为最终答案。

最后附上python代码：

```python
class Solution(object):
    def rootCount(self, edges, guesses, k):
        """
        :type edges: List[List[int]]
        :type guesses: List[List[int]]
        :type k: int
        :rtype: int
        """

        n = len(edges) + 1
        g = {index : set() for index in range(n)}
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)
        
        guess_dict = {index : set() for index in range(n)}
        for x, y in guesses:
            guess_dict[x].add(y)
        
        hit = 0

        q = [0]
        head, tail = 0, 1
        vis = set([0])
        while head < tail:
            now = q[head]
            head += 1
            for nxt in g[now]:
                if nxt not in vis:
                    if nxt in guess_dict[now]:
                        hit += 1
                    q.append(nxt)
                    vis.add(nxt)
                    tail += 1
        
        res = 0
        if hit >= k:
            res += 1

        q = [[0, hit]]
        vis = set([0])
        head, tail = 0, 1
        while head < tail:
            now, now_hit = q[head]
            head += 1
            for nxt in g[now]:
                if nxt not in vis:
                    vis.add(nxt)
                    nxt_hit = now_hit
                    if nxt in guess_dict[now]:
                        nxt_hit -= 1
                    if now in guess_dict[nxt]:
                        nxt_hit += 1
                    if nxt_hit >= k:
                        res += 1

                    q.append([nxt, nxt_hit])
                    tail += 1
        
        return res
```
