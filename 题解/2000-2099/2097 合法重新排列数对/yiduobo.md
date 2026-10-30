---
title: "2097. 合法重新排列数对"
aliases: ["yiduobo的每日leetcode 2097.合法重新排列数对"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/graph", "leetcode/graph-theory", "leetcode/eulerian-path", "题单/图论算法", "题单/图论算法/五-欧拉路径/欧拉回路"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/521024604"
zhihu_id: "521024604"
zhihu_title: "yiduobo的每日leetcode 2097.合法重新排列数对"
question_id: "2097"
question: "合法重新排列数对"
problem_url: "https://leetcode.cn/problems/valid-arrangement-of-pairs/"
difficulty: "Hard"
rating: 2651
created: "2022-05-27T23:11:52+08:00"
updated: "2022-05-27T23:11:52+08:00"
upvotes: 0
comments: 0
---

# 2097. 合法重新排列数对

> **[yiduobo的每日leetcode 2097.合法重新排列数对](https://zhuanlan.zhihu.com/p/521024604) · 知乎 · 2022-05-27 · 赞同 0**
> 力扣：[2097. 合法重新排列数对](https://leetcode.cn/problems/valid-arrangement-of-pairs/) · Hard · 灵茶山艾府：[有向图欧拉路径](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2097.合法重新排列数对

[力扣](https://leetcode.cn/problems/valid-arrangement-of-pairs/)

如果将数对里面的数值视为图中的点，数对视为图中的有向边，那么最终的问题就是能否找出一个点，从这个点开始在图中走，保证图中每条边经过且仅经过一次，这就是经典的一笔画问题。

对于一笔画问题，有解的条件是图是连通的，且图中每个节点的入度都等于出度，或者仅有两个节点，入度和出度相差都是1。由于题目保证了有解，那么可以先统计每个节点的入度和出度，若存在某个节点出度比入度多1，那么该节点就是一笔画的起点，否则可以选择任意节点开始。

接下来从起点开始执行经典的Hierholzer算法即可。算法的实现非常简单，对于当前节点，若还有出边，那么就将该边从图中去掉，此时剩余的子图依然符合一笔画的规则，且此时的起点变为了当前节点，于是从当前节点开始继续执行Hierholzer算法即可。

当所有的边都遍历过后，根据dfs序还原出行走过程即可。需要注意的是，在这里需要倒序还原，因此图中可能存在桥会将剩余的子图分割开。对于这些桥，理想中的遍历顺序是先遍历完一侧的子图再走，但是在算法执行过程中无法准确控制，因此如果先走过桥，图将会被分割成不连通的两个子图，而分割出去的部分只能在回溯到当前节点时才能再去遍历。实际上，这个遍历过程应该发生在走过桥之前，因此在还原行走过程时需要倒序还原。

另一方面，如果是按理想顺序走的话，由于节点出度和入度的保证，遍历完子图后必然会回到当前节点，此时再流畅地通过桥即可，并不会出现需要回溯遍历子图并强行插入dfs序的情况。

最后附上python代码：

```python
class Solution(object):
    def validArrangement(self, pairs):
        """
        :type pairs: List[List[int]]
        :rtype: List[List[int]]
        """

        ind = {}
        oud = {}
        g = {}
        for x, y in pairs:
            if x not in g:
                g[x] = []
            g[x].append(y)
            ind[y] = ind.get(y, 0) + 1
            oud[x] = oud.get(x, 0) + 1
        
        start = pairs[0][0]
        for x in oud:
            if oud[x] - ind.get(x, 0) == 1:
                start = x
                break

        def dfs(now):
            while g.get(now, []):
                next = g[now][-1]
                g[now].pop()
                dfs(next)
                res.append([now, next])

        res = []
        dfs(start)
        res.reverse()
        return res
```
