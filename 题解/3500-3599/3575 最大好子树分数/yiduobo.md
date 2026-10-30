---
title: "3575. 最大好子树分数"
aliases: ["yiduobo的每日leetcode 3575.最大好子树分数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/tree", "leetcode/hash-table", "leetcode/dynamic-programming", "leetcode/bitmask", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/链表-二叉树与回溯/三-一般树", "题单/动态规划/九-状态压缩-DP-状压-DP", "题单/动态规划/十二-树形-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1937279273053433973"
zhihu_id: "1937279273053433973"
zhihu_title: "yiduobo的每日leetcode 3575.最大好子树分数"
question_id: "3575"
question: "最大好子树分数"
problem_url: "https://leetcode.cn/problems/maximum-good-subtree-score/"
difficulty: "Hard"
rating: 2360
created: "2025-08-08T22:48:45+08:00"
updated: "2025-08-08T22:48:45+08:00"
upvotes: 1
comments: 0
---

# 3575. 最大好子树分数

> **[yiduobo的每日leetcode 3575.最大好子树分数](https://zhuanlan.zhihu.com/p/1937279273053433973) · 知乎 · 2025-08-08 · 赞同 1**
> 力扣：[3575. 最大好子树分数](https://leetcode.cn/problems/maximum-good-subtree-score/) · Hard · 灵茶山艾府：[树形 DP + 状态压缩 + 启发式合并（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3575.最大好子树分数

[3575. 最大好子树分数 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-good-subtree-score/description/)

题目给出一颗根节点为0的无向树，其中包含n个节点，n的大小不超过500。这n个节点的编号为0到n - 1，对于节点index，其对应的节点值为vals[index]。

现在要求从一颗子树中选取部分节点，这些节点的数值组成一个子集。若子集中的所有元素的十进制表示中，从0到9每个数字都最多只出现了一次，那么就称这是一个好子集，这个子集的分数就是其节点值的总和。

定义一个长度为n的数组maxScore，其中maxScore[u]表示以节点u为根节点的子树中，好子集的最大可能值总和，问maxScore中所有值的总和是多少。

首先，从题目中关于好子集的定义来看，0到9每个数字只能出现一次，那么完全可以利用状态压缩来表示子集中已经有哪些数字。又由于本题中n的规模不大，因此可以考虑使用二维的状态表示f[now][state]表示以now为根节点的子树中，选出节点对应的子集占用数位为state时的最大可能总和，那么对于f[now][state]：

1、首先考虑vals[now]是否可用：

逐位分离vals[now]的所有数位，若某个数字出现了多次，那么说明vals[now]不可用，此时需要初始化f[now][state]为0，否则可以通过这些数字计算出vals[now]对应的状态表示state，然后就可以初始化f[now][state]为vals[now]

2、接下来枚举now的所有孩子节点，对于当前枚举到的孩子节点nxt：

首先递归求解f[nxt]。对于f[nxt]中的所有sub_state，可以先用f[nxt][sub_state]来更新f[now][sub_state]，表示直接使用子树nxt中sub_state对应的子集来充当f[now][sub_state]选取的集合。除此之外，还可以遍历f[now]中的所有state，若state & sub_state为0，说明这两个子集不相交，因此可以将二者合并，即利用f[now][state] + f[nxt][sub_state]来更新f[now][state | sub_state]。

从0号节点开始向下一趟dfs求解f，对于每个节点，将其对应的f中所有元素值累加到答案中即可。

在具体实现时，可以省去now这一维，但是需要注意由于是逐个遍历孩子节点，因此无法通过修改更新顺序来适配状态转移，而是需要通过f[now]的副本以及f[nxt]来更新最新的f[now]。

最后附上python代码：

```python
class Solution(object):
    def goodSubtreeSum(self, vals, par):
        """
        :type vals: List[int]
        :type par: List[int]
        :rtype: int
        """
        
        n = len(vals)
        g = [[] for _ in range(n)]
        for index, p in enumerate(par[1:], 1):
            g[p].append(index)
        
        global res
        res = 0
        mod = 10 ** 9 + 7
        def dfs(now):
            f = {}

            state = 0
            v = vals[now]
            while v:
                r = v % 10
                v //= 10
                if state & (1 << r) == (1 << r):
                    state = -1
                    break
                state |= (1 << r)
            
            if state != -1:
                f[state] = vals[now]
            
            for nxt in g[now]:
                sub_f = dfs(nxt)
                tmp = copy.deepcopy(f)
                for sub_state, sub_v in sub_f.items():
                    f[sub_state] = max(f.get(sub_state, 0), sub_v)
                    for state, v in tmp.items():
                        if state & sub_state == 0:
                            merge_state = state | sub_state
                            f[merge_state] = max(f.get(merge_state, 0), v + sub_v)

            if f:
                global res
                res += max(f.values())
                if res >= mod:
                    res -= mod
            
            return f
        
        dfs(0)
        return res
```
