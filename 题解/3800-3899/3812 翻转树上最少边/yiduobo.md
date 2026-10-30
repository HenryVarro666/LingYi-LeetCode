---
title: "3812. 翻转树上最少边"
aliases: ["yiduobo的每日leetcode 3812.翻转树上最少边"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/sorting", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1996676458853208514"
zhihu_id: "1996676458853208514"
zhihu_title: "yiduobo的每日leetcode 3812.翻转树上最少边"
question_id: "3812"
question: "翻转树上最少边"
problem_url: "https://leetcode.cn/problems/minimum-edge-toggles-on-a-tree/"
difficulty: "Hard"
rating: 2179
created: "2026-01-20T21:58:51+08:00"
updated: "2026-01-20T21:58:51+08:00"
upvotes: 0
comments: 0
---

# 3812. 翻转树上最少边

> **[yiduobo的每日leetcode 3812.翻转树上最少边](https://zhuanlan.zhihu.com/p/1996676458853208514) · 知乎 · 2026-01-20 · 赞同 0**
> 力扣：[3812. 翻转树上最少边](https://leetcode.cn/problems/minimum-edge-toggles-on-a-tree/) · Hard · 灵茶山艾府：[树 DFS，O(n) 优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3812.翻转树上最少边

<https://leetcode.cn/problems/minimum-edge-toggles-on-a-tree/>

题目给出一颗包含n个节点的无向树，节点编号从0到n - 1。n的规模在2到10^5之间。

这棵树由长度为n - 1的二维整数数组edges表示，其中edges\[index\] \= \[a\[index\], b\[index\]\]，表示树中节点a\[index\]与b\[index\]之间存在一条边。

另外给出两个长度为n的二进制字符串start和target，对于每个节点x，start[x]是其初始颜色，target[x]是其目标颜色。

在一次操作中，可以选择下标为index的边，并翻转其两个端点。也就是说，若这条边是[u, v]，那么节点u和v的颜色各自从'0'变成'1'，或者从'1'变成'0'。

要求返回一个边下标数组，执行这些边对应的操作可以将start转换为target。在所有有序序列中找出长度最短的序列，以升序返回边下标。若无法将start转换为target，则返回[-1]。

由于题目给出的是至少有两个节点的树，那么无论树是什么形态，其中至少有两个度为1的节点。证明也很简单，如果所有的n个节点的度都大于等于2，那么度数之和至少也是n \* 2，但是n - 1条边能提供的度数为(n - 1) \* 2，因此至少有两个节点的度为1。

接下来，对于任意一个度为1的节点，其对应的start和target相同，那么与连接该节点的唯一一条边就不能被标记，反之则必须被标记。更进一步的，由于这条边能否被标记已经确定下来了，那么就可以将这条边以及这个度为1的节点删去，这样一来，树的规模从n个节点缩减到n - 1个节点，其中依然至少存在两个度为1的节点。重复此过程，直到树缩减到两个节点一条边为止。

最后，只需要判断能否通过保持原样，或者翻转这条剩下的边，使得剩下的两个节点对应的start都等于target就行了。若无法达成，则返回-1，否则将标记的边的下标排序后返回即可。

在具体实现上，每一轮都是找出一个度为1的节点，然后修正与其相邻的节点的度，这个过程与拓扑排序很相似，因此也可以采用类似拓扑排序的方式来实现上面描述的算法。在确定哪条边是依然存在的边，哪条边已经被删去了这个问题上，则可以通过连接的节点的度数来进行判断。

最后附上python代码：

```python
class Solution(object):
    def minimumFlips(self, n, edges, start, target):
        """
        :type n: int
        :type edges: List[List[int]]
        :type start: str
        :type target: str
        :rtype: List[int]
        """
        
        start = [int(x) for x in start]
        target = [int(x) for x in target]

        g = [[] for _ in range(n)]
        d = [0] * n

        for index, (x, y) in enumerate(edges):
            g[x].append((y, index))
            g[y].append((x, index))
            d[x] += 1
            d[y] += 1
        
        q = []
        for x in range(n):
            if d[x] == 1:
                q.append(x)
        
        head, tail = 0, len(q)
        res = []
        for _ in range(n - 2):
            x = q[head]
            head += 1
            d[x] -= 1
            for y, index in g[x]:
                if d[y] > 1:
                    d[y] -= 1
                    if start[x] != target[x]:
                        res.append(index)
                        start[y] ^= 1
                    if d[y] == 1:
                        q.append(y)
        
        x = q[head]
        for y, index in g[x]:
            if d[y] == 1:
                if (start[x] == target[x] and start[y] != target[y]) or (start[x] != target[x] and start[y] == target[y]):
                    return [-1]
                if start[x] != target[x]:
                    res.append(index)
                break
        
        return sorted(res)
```
