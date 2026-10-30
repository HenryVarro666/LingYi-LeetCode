---
title: "2092. 找出知晓秘密的所有专家"
aliases: ["yiduobo的每日leetcode 2092.找出知晓秘密的所有专家"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/union-find", "leetcode/graph", "leetcode/sorting", "leetcode/simulation", "题单/常用数据结构", "题单/图论算法", "题单/常用数据结构/七-并查集", "题单/图论算法/一-图的遍历"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/519997767"
zhihu_id: "519997767"
zhihu_title: "yiduobo的每日leetcode 2092.找出知晓秘密的所有专家"
question_id: "2092"
question: "找出知晓秘密的所有专家"
problem_url: "https://leetcode.cn/problems/find-all-people-with-secret/"
difficulty: "Hard"
rating: 2004
created: "2022-05-26T00:07:47+08:00"
updated: "2022-05-26T00:07:47+08:00"
upvotes: 0
comments: 0
---

# 2092. 找出知晓秘密的所有专家

> **[yiduobo的每日leetcode 2092.找出知晓秘密的所有专家](https://zhuanlan.zhihu.com/p/519997767) · 知乎 · 2022-05-26 · 赞同 0**
> 力扣：[2092. 找出知晓秘密的所有专家](https://leetcode.cn/problems/find-all-people-with-secret/) · Hard · 灵茶山艾府：[两种方法：DFS / 并查集（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2092.找出知晓秘密的所有专业

[力扣](https://leetcode.cn/problems/find-all-people-with-secret/)

本题是很典型的染色问题，但是与常规染色问题有所不同的是，本题的图是每时每刻都在变化的，因此可以先将所有边以时间作为key用哈希表收集起来，然后从小到大遍历每个时间点，并使用对应的边来建图，然后执行bfs进行染色。

在这里有一个问题是bfs的起点应该如何选择。一个直观的想法是将当前知晓秘密的所有节点都加入bfs的初始队列中，这个做法的正确性是可以保证的，但是在极限情况下时间复杂度可能达到O(mn)，其中n为点数，m为边数。

可以发现，在当前时刻，并不是每个知晓秘密的点都出现在当前的图中，而对于这些点是没必要将其加入到bfs队列中的，因此在建图的时候可以进行一些筛选。在建图过程中，对于当前枚举的边(x, y)：

1、若x和y都是知晓秘密的，那么这条边没必要加入到图中

2、若x和y中有一方是知晓秘密的，那么将其加入到bfs的初始队列中，并在图中添加这条边

3、若x和y都不知道秘密，那么也需要在图中添加这条边

这样一来，最终的时间复杂度就优化到了O(m)。

最后附上python代码：

```python
class Solution(object):
    def findAllPeople(self, n, meetings, firstPerson):
        """
        :type n: int
        :type meetings: List[List[int]]
        :type firstPerson: int
        :rtype: List[int]
        """

        res_set = set([0, firstPerson])
        time_dict = {}
        for x, y, t in meetings:
            if t not in time_dict:
                time_dict[t] = []
            time_dict[t].append([x, y])
        
        for t in range(1, 100001):
            if t in time_dict:
                g = {}
                q_set = set()
                for x, y in time_dict[t]:
                    if x in res_set:
                        if y in res_set:
                            continue
                        else:
                            q_set.add(x)
                    elif y in res_set:
                        q_set.add(y)
                    
                    if x not in g:
                        g[x] = set()
                    if y not in g:
                        g[y] = set()

                    g[x].add(y)
                    g[y].add(x)

                q = list(q_set)
                l, r = 0, len(q)
                while l < r:
                    now = q[l]
                    l += 1
                    for next in g.get(now, set()):
                        if next not in res_set:
                            q.append(next)
                            res_set.add(next)
                            r += 1
        
        return list(res_set)
```
