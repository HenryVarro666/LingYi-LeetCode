---
title: "3967. 任务完成时间II"
aliases: ["yiduobo的每日leetcode 3967.任务完成时间II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2052900657636578160"
zhihu_id: "2052900657636578160"
zhihu_title: "yiduobo的每日leetcode 3967.任务完成时间II"
question_id: "3967"
question: "任务完成时间II"
problem_url: "https://leetcode.cn/problems/finish-time-of-tasks-ii/"
created: "2026-06-24T22:29:38+08:00"
updated: "2026-06-24T22:29:42+08:00"
upvotes: 0
comments: 0
---

# 3967. 任务完成时间II

> **[yiduobo的每日leetcode 3967.任务完成时间II](https://zhuanlan.zhihu.com/p/2052900657636578160) · 知乎 · 2026-06-24 · 赞同 0**
> 力扣：[3967. 任务完成时间II](https://leetcode.cn/problems/finish-time-of-tasks-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3967.任务完成时间II

<https://leetcode.cn/problems/finish-time-of-tasks-ii/>

题目给出一个整数n，表示项目中的任务数量，这些任务的标号从0到n - 1，以无向树的形式连接。另外给出一个长度为n - 1的二维整数数组edges，其中edges\[index\] \= \[u\[index\], v\[index\]\]，表示任务u\[index\]与任务v\[index\]相连。

同时给出一个长度为n的数组bastTime，其中baseTime[index]表示完成任务index所需的时间。

现在可以任选任意任务作为树的根节点，确定根节点之后，树的形态也随之确定。接下来，对于树中的任务index，其完成时间计算如下：

- 叶子任务：完成时间为baseTime[index]
- 非叶子任务：
   - 令earliest和latest分别为其子节点中最小和最大的完成时间
   - 令ownDuration为(latest - earliest) + baseTime[index]
   - 完成时间为latest + ownDuration

问每个节点作为根节点时，其中完成时间最小的是多少。

之前3965题的加强版

[yiduobo的每日leetcode 3965.任务完成时间I](https://zhuanlan.zhihu.com/p/2052124487328573279)

本题需要考虑以每个节点作为根节点时的任务完成时间，基于树的形态以及完成时间的计算方法，很容易联想到使用换根dp来进行处理。

具体来说，还是先以0作为根节点进行一次dfs，计算这种形态下每个任务的完成时间，记为数组f。

接下来，还是从0开始向下dfs，对于当前节点now，先计算其作为根节点时对应的完成时间，再遍历now的每个孩子nxt，先将now的完成时间修正为将now作为nxt的某个孩子所需的时间，然后递归计算nxt。

鉴于题目中计算完成时间涉及到孩子节点完成时间的最小值以及最大值，而换根的过程中，下一个目标根节点可能恰好就是当前节点孩子完成时间中的最小值或者最大值，不能继续使用，因此在这里需要为每个节点维护所有孩子完成时间的最大、次大以及最小、次小值。

需要注意的是，这四个值同样需要考虑当前节点父亲节点修正后的完成时间，因为当前节点作为根节点后，其原来的父亲节点也是当前节点的孩子。

基于上面的讨论，对于当前作为根节点的节点now，具体处理方法如下：

1、首先遍历now的所有孩子节点nxt，记录其中最大、次大以及最小、次小值

2、若now原来有父亲节点fa，那么还需要使用h[fa]更新上面的四个值。这里的h[v]表示的是v从根节点变为其某个特定孩子的子节点时，修正后的完成时间

3、使用最大、最小值确定当前节点now的完成时间res[now]

4、在此遍历now的所有孩子节点nxt，对于当前的nxt，需要先计算now变为nxt的孩子后对应的最大值和最小值。具体来说，这两个值初始化为步骤1中记录的最大值和最小值，若f[nxt]恰好等于最大值或者最小值，则需要使用次大值或者次小值来代替。接下来，根据这两个值计算修正后now的花费时间h[now]，然后递归计算nxt。需要特别注意，对于每个nxt都需要计算对应的h[now]，在这里h[now]并不是固定不变的

全部计算完成后，取res的最小值即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def finishTime(self, n, edges, baseTime):
        """
        :type n: int
        :type edges: List[List[int]]
        :type baseTime: List[int]
        :rtype: int
        """
        
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        f = [None] * n
        h = [None] * n
        res = [None] * n

        def dfs(now, fa):
            earliest = None
            latest = None
            for nxt in g[now]:
                if nxt == fa:
                    continue
                dfs(nxt, now)
                if earliest is None or earliest > f[nxt]:
                    earliest = f[nxt]
                if latest is None or latest < f[nxt]:
                    latest = f[nxt]
            
            if earliest is None:
                f[now] = baseTime[now]
            else:
                f[now] = latest + (latest - earliest) + baseTime[now]
        
        def calc(now, fa):
            first_e, second_e = None, None
            first_l, second_l = None, None
            for nxt in g[now]:
                if nxt == fa:
                    continue

                if first_e is None or first_e > f[nxt]:
                    first_e, second_e = f[nxt], first_e
                elif second_e is None or second_e > f[nxt]:
                    second_e = f[nxt]
                
                if first_l is None or first_l < f[nxt]:
                    first_l, second_l = f[nxt], first_l
                elif second_l is None or second_l < f[nxt]:
                    second_l = f[nxt]

            if fa != -1:
                if first_e is None or first_e > h[fa]:
                    first_e, second_e = h[fa], first_e
                elif second_e is None or second_e > h[fa]:
                    second_e = h[fa]

                if first_l is None or first_l < h[fa]:
                    first_l, second_l = h[fa], first_l
                elif second_l is None or second_l < h[fa]:
                    second_l = h[fa]
            
            if first_e is None:
                res[now] = f[now]
            else:
                res[now] = first_l - first_e + baseTime[now] + first_l

            for nxt in g[now]:
                if nxt == fa:
                    continue
                
                e, l = first_e, first_l
                if f[nxt] == e:
                    e = second_e
                if f[nxt] == l:
                    l = second_l
                
                if e is None:
                    h[now] = baseTime[now]
                else:
                    h[now] = l - e + baseTime[now] + l
                
                calc(nxt, now)

        dfs(0, -1)
        calc(0, -1)
        return min(res)
```
