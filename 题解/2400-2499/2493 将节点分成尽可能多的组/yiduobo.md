---
title: "2493. 将节点分成尽可能多的组"
aliases: ["yiduobo的每日leetcode 2493.将节点分成尽可能多的组"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/图论算法", "题单/图论算法/九-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/633213268"
zhihu_id: "633213268"
zhihu_title: "yiduobo的每日leetcode 2493.将节点分成尽可能多的组"
question_id: "2493"
question: "将节点分成尽可能多的组"
problem_url: "https://leetcode.cn/problems/divide-nodes-into-the-maximum-number-of-groups/"
difficulty: "Hard"
rating: 2415
created: "2023-05-30T03:23:04+08:00"
updated: "2023-05-30T03:23:04+08:00"
upvotes: 0
comments: 0
---

# 2493. 将节点分成尽可能多的组

> **[yiduobo的每日leetcode 2493.将节点分成尽可能多的组](https://zhuanlan.zhihu.com/p/633213268) · 知乎 · 2023-05-30 · 赞同 0**
> 力扣：[2493. 将节点分成尽可能多的组](https://leetcode.cn/problems/divide-nodes-into-the-maximum-number-of-groups/) · Hard · 灵茶山艾府：[枚举起点跑 BFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2493.将节点分成尽可能多的组

[力扣](https://leetcode.cn/problems/divide-nodes-into-the-maximum-number-of-groups/)

首先，题目要求相邻节点需要分到相邻的组中，换言之，题目中的图必须是一个二分图，其中不能存在长度为奇数的简单环。比较直观的理解是假设图中存在一个长度为k的环，这里的k为奇数，那么就可以从环上任意点出发，向与其相邻的两个点各往外走k / 2步，最终将会走到两个相邻的点，同时这两个点由于都是从相同点走k / 2步到达的，那么这两个点分组的奇偶性必然是相同的，但是这两个点中又存在一条边，要求这两个点属于相邻的组，这就与二者所在的组奇偶性相同产生了矛盾。

有了这个结论，就可以通过黑白染色的方法来检测当前图是否为二分图，若不是，则直接返回-1。

而对于当前图是二分图的情况而言，不同连通分量之间的节点所属的组必然是串联的形式而不是并联的形式，这样才能使得最终分出的组最多，于是问题就转化成了对于图中的每个连通分量，将这个连通分量拉得尽可能长，然后将每个连通分量拉伸的长度相加作为最终答案。

对于拉伸这个操作，由于要求相邻节点所属的组也相邻，那么在这里就可以从每个连通分量的任意节点开始进行bfs，每一轮都将与当前节点相邻的未访问节点放入下一组当中，最终bfs的轮次恰好就是当前连通分量可以拉伸到最大时分组的数目。

具体实现上，由于最后拉伸也是采用的bfs，那么可以与之前染色的过程结合起来，只需一趟遍历对于未访问过的节点开始bfs拉伸以及染色就行了。

最后附上python代码：

```python
class Solution(object):
    def magnificentSets(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: int
        """

        g = {}
        for x, y in edges:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)

        part = 0
        len_dict = {}
        belong_part = {}
        for start in range(1, n + 1):
            part_len = 0
            if start not in belong_part:
                belong_part[start] = part
                part += 1
            color = {start : 0}
            q = [start]
            head, tail = 0, 1
            while head < tail:
                part_len += 1
                for now in q[head : tail]:
                    for next in g.get(now, set()):
                        if next not in color:
                            color[next] = 1 - color[now]
                            q.append(next)
                        elif color[next] == color[now]:
                            return -1
                        if next not in belong_part:
                            belong_part[next] = belong_part[start]
                
                head, tail = tail, len(q)

            len_dict[belong_part[start]] = max(len_dict.get(belong_part[start], 0), part_len)
        
        return sum(len_dict.values())
```
