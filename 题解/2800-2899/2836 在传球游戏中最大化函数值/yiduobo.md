---
title: "2836. 在传球游戏中最大化函数值"
aliases: ["yiduobo的每日leetcode 2836.在传球游戏中最大化函数值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/链表-二叉树与回溯", "题单/图论算法", "题单/链表-二叉树与回溯/三-一般树", "题单/图论算法/二-拓扑排序"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/659573926"
zhihu_id: "659573926"
zhihu_title: "yiduobo的每日leetcode 2836.在传球游戏中最大化函数值"
question_id: "2836"
question: "在传球游戏中最大化函数值"
problem_url: "https://leetcode.cn/problems/maximize-value-of-function-in-a-ball-passing-game/"
difficulty: "Hard"
rating: 2769
created: "2023-10-05T03:44:36+08:00"
updated: "2023-10-05T03:44:36+08:00"
upvotes: 0
comments: 0
---

# 2836. 在传球游戏中最大化函数值

> **[yiduobo的每日leetcode 2836.在传球游戏中最大化函数值](https://zhuanlan.zhihu.com/p/659573926) · 知乎 · 2023-10-05 · 赞同 0**
> 力扣：[2836. 在传球游戏中最大化函数值](https://leetcode.cn/problems/maximize-value-of-function-in-a-ball-passing-game/) · Hard · 灵茶山艾府：[【模板】树上倍增（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2836.在传球游戏中最大化函数值

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximize-value-of-function-in-a-ball-passing-game/)

题目中的函数值实际上就是传球路径中经过的所有人的编号之和，但是本题的传球次数k非常大，直接模拟肯定是行不通的，需要想办法优化。

首先可以明确的是，题目中的传球路径在经过若干步之后一定会进入到某个环路中，也就是说题目中的传球关系最终可以抽象成若干个环，而每个环上的任意节点都可能额外向外延伸出一棵树。每次传球都可以认为是先从起点在树中对应的节点开始向树根行走，走到树根后就意味着来到了环上，接下来可能要在这个环上走上几圈，最后再从这个入环点开始走完剩下的步数。

接下来问题就可以分为两个部分：

如何构造出上面描述的树->中心环结构

构造好之后如何计算每个节点行走k步之后的价值和

---

首先是如何构造。

由于每个节点最终都会属于某棵树，那么就可以使用一个哈希表g来维护树中的节点。

接下来遍历所有的节点，若当前节点之前没有访问过，那么就从当前节点开始向后行走。

在这个过程中如果出现了g中已经出现的节点，说明当前的起点以及遍历的节点是某棵已经构造出来的树的子树，此时只需把当前的子树拼上去就行了。

反之，如果整个过程中没有出现g中已经出现的节点，但是出现了本次遍历中出现过的节点，那么就说明这两次重复出现之间的部分就是一个环，而在这个环之前的部分则是入环的树。这种情况下需要先将环储存起来，然后再将树拼接上去。

---

接下来是如何计算数值：

1、第一段实际上是一个树上的区间问题。如果k足够大可以走到环上，那么在树中行走产生的节点值就是从起点到树根这一段的节点值之和，反之则可以使用从起点到树根的节点值之和减去终点到树根的节点值之和得到。

不过需要注意的是，如果单独求解的话需要从根向下遍历到指定节点，复杂度较高，因此在这里可以反过来思考，通过遍历整棵树，一次性将树上所有节点在树中将产生的节点值之和计算出来。

2、第二段相对简单，可以通过来到环上之后剩余步数除以环的长度，得到将在环上行走的圈数，然后乘以环上节点值之和就行了。由于环是固定的，因此这个节点值之和可以提前预处理出来。

3、第三段需要行走的步数则是则是一个环上的区间和问题，同样是转化成前缀和来求解。另外由于是环上的前缀和，因此需要先将原数组原封不动复制一份，然后再计算常规的前缀和。有了前缀和，2中所需的环上节点值之和就无需计算了。

构造好树->环的结构之后，从每个环上节点向外执行dfs完成1中的计算，同时得到入环后剩余的步数t，再通过t与环的长度完成2和3中的计算，然后更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def getMaxFunctionValue(self, receiver, k):
        """
        :type receiver: List[int]
        :type k: int
        :rtype: int
        """

        circle_list = []
        s_circle = []
        g = {}

        for index in range(len(receiver)):
            if index not in g:
                q = [index]
                vis = set()
                while q[-1] not in g and q[-1] not in vis:
                    vis.add(q[-1])
                    q.append(receiver[q[-1]])
                
                if q[-1] not in g:
                    p = len(q) - 2
                    while q[p] != q[-1]:
                        p -= 1
                    
                    circle_list.append([])
                    for v in q[p : len(q) - 1]:
                        circle_list[-1].append(v)
                        g[v] = set()

                    s_circle.append([0])
                    for j in range(len(circle_list[-1])):
                        s_circle[-1].append(s_circle[-1][-1] + circle_list[-1][j])
                    for j in range(len(circle_list[-1])):
                        s_circle[-1].append(s_circle[-1][-1] + circle_list[-1][j])
                
                else:
                    p = len(q) - 1

                p -= 1
                while p >= 0:
                    g[q[p]] = set()
                    g[q[p + 1]].add(q[p])
                    p -= 1

        global res
        res = 0
        def dfs(now, prefix_s):
            t = k + 1
            v = 0
            if len(prefix_s) == 0:
                prefix_s.append(now)
            else:
                prefix_s.append(prefix_s[-1] + now)
                if t < len(prefix_s):
                    v = prefix_s[-1] - prefix_s[-t - 1]
                    t = 0
                else:
                    v = prefix_s[-1] - prefix_s[0]
                    t -= len(prefix_s) - 1
            
            rnd = t / len(circle_list[circle_id])
            t %= len(circle_list[circle_id])
            v += rnd * s_circle[circle_id][len(circle_list[circle_id])]
            v += s_circle[circle_id][circle_index + t] - s_circle[circle_id][circle_index]
        
            global res
            res = max(res, v)
            
            for child in g[now]:
                dfs(child, prefix_s)
            
            prefix_s.pop()

        for circle_id in range(len(circle_list)):
            for circle_index in range(len(circle_list[circle_id])):
                dfs(circle_list[circle_id][circle_index], [])

        return res
```
