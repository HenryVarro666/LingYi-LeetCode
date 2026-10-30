---
title: "3939. 统计有根树中不相邻子集的数目"
aliases: ["yiduobo的每日leetcode 3939.统计有根树中不相邻子集的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/动态规划", "题单/动态规划/三-背包"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2043451374776620336"
zhihu_id: "2043451374776620336"
zhihu_title: "yiduobo的每日leetcode 3939.统计有根树中不相邻子集的数目"
question_id: "3939"
question: "统计有根树中不相邻子集的数目"
problem_url: "https://leetcode.cn/problems/count-non-adjacent-subsets-in-a-rooted-tree/"
difficulty: "Hard"
rating: 2354
created: "2026-05-28T22:17:29+08:00"
updated: "2026-05-28T22:17:29+08:00"
upvotes: 1
comments: 0
---

# 3939. 统计有根树中不相邻子集的数目

> **[yiduobo的每日leetcode 3939.统计有根树中不相邻子集的数目](https://zhuanlan.zhihu.com/p/2043451374776620336) · 知乎 · 2026-05-28 · 赞同 1**
> 力扣：[3939. 统计有根树中不相邻子集的数目](https://leetcode.cn/problems/count-non-adjacent-subsets-in-a-rooted-tree/) · Hard · 灵茶山艾府：[树上独立集 + 树上背包（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3939.统计有根树中不相邻子集的数目

<https://leetcode.cn/problems/count-non-adjacent-subsets-in-a-rooted-tree/description/>

题目给出一棵具有n个节点的有根树，节点编号从0到n - 1，由一个长度为n的整数数组parent表示。其中：

- parent[0] \= -1，表示0号节点为根节点
- 对于所有的1 \<\= index \< n，对应的parent[index]取值在0到index之间，表示parent[index]是index的父亲节点

另外给出一个长度为n的整数数组nums，其中nums[index]是节点index的值，以及一个整数k。

对于树中节点的一个非空子集，若其中所有节点之和为k的倍数，同时任意一对节点都不相邻，那么就称其为一个有效子集。问树中有效子集的数目。

经典的动态规划问题。令f[now][v]表示以now为根节点的子树中，包含节点now，且节点值之和模k等于v的子集数目，g[now][v]则表示不包含now，且节点值之和模k等于v的子集数目。由于部分数值可能取不到，在这里可以将f[now]和g[now]设计为哈希表，避免遍历不存在的状态。

那么对于f[now]和g[now]：

1、首先可以初始化f[now][nums[now] % k]以及g[now][0]为1，也就是f对应的子集中必须选择now，而g对应的子集一开始为空。

2、接下来遍历now的所有孩子nxt，对于当前遍历到的nxt，先递归计算nxt，得到所有的f[nxt][v]以及g[nxt][v]，然后将g[nxt]中的可能子集合并到f[now]中，同时将f[nxt]以及g[nxt]中的可能子集合并到g[now]中。需要注意，因为不能存在相邻的节点，因此f[now]只能通过g[nxt]更新，而g[now]则不受限制。

具体的合并方式如下，以将g[nxt]合并到f[now]中为例：

由于这里需要对k取模，因此无法原地修改，在这里需要先将f[now]中所有可能的值now_v以及对应的子集数目now_cnt提取出来，储存在数组f_now中，然后将f[now]清空。

接下来遍历f_now中的now_v与now_cnt，然后再遍历g[nxt]中所有的nxt_v与nxt_cnt，根据乘法原理，此时就应该将now_cnt \* nxt_cnt累加到f[now][(now_v + nxt_v) % k]当中，也就是将原来和为now_v的子集，与nxt中值为nxt_v的子集合并，得到模k的结果为(now_v + nxt_v) % k的子集。

从根节点0向下递归计算，全部计算完成后，最终答案就是f[0][0] + g[0][0] - 1。这里的减一是因为g[0][0]中必然包含了空集，而题目需要计算的是非空集合的数量，因此需要减去1。

最后附上python代码：

```python
class Solution(object):
    def countValidSubsets(self, parent, nums, k):
        """
        :type parent: List[int]
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        n = len(parent)
        f = [{} for _ in range(n)]
        g = [{} for _ in range(n)]
        mod = 10 ** 9 + 7

        t = [[] for _ in range(n)]
        for index, p in enumerate(parent):
            if p != -1:
                t[p].append(index)

        def calc(now):
            f[now][nums[now] % k] = 1
            g[now][0] = 1

            for nxt in t[now]:
                calc(nxt)
                f_now = f[now].items()
                f[now] = {}
                g_now = g[now].items()
                g[now] = {}

                for now_v, now_cnt in f_now:
                    for nxt_v, nxt_cnt in g[nxt].items():
                        v = (now_v + nxt_v) % k
                        f[now][v] = (f[now].get(v, 0) + now_cnt * nxt_cnt) % mod
                
                for now_v, now_cnt in g_now:
                    for nxt_v, nxt_cnt in f[nxt].items():
                        v = (now_v + nxt_v) % k
                        g[now][v] = (g[now].get(v, 0) + now_cnt * nxt_cnt) % mod
                    for nxt_v, nxt_cnt in g[nxt].items():
                        v = (now_v + nxt_v) % k
                        g[now][v] = (g[now].get(v, 0) + now_cnt * nxt_cnt) % mod
            
        calc(0)
        return (f[0].get(0, 0) + g[0][0] - 1) % mod
```
