---
title: "3425. 最长特殊路径"
aliases: ["yiduobo的每日leetcode 3425.最长特殊路径"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/tree", "leetcode/depth-first-search", "leetcode/hash-table", "leetcode/two-pointers", "leetcode/sliding-window", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1889443746753528088"
zhihu_id: "1889443746753528088"
zhihu_title: "yiduobo的每日leetcode 3425.最长特殊路径"
question_id: "3425"
question: "最长特殊路径"
problem_url: "https://leetcode.cn/problems/longest-special-path/"
difficulty: "Hard"
rating: 2435
created: "2025-03-29T23:29:53+08:00"
updated: "2025-03-29T23:29:53+08:00"
upvotes: 1
comments: 0
---

# 3425. 最长特殊路径

> **[yiduobo的每日leetcode 3425.最长特殊路径](https://zhuanlan.zhihu.com/p/1889443746753528088) · 知乎 · 2025-03-29 · 赞同 1**
> 力扣：[3425. 最长特殊路径](https://leetcode.cn/problems/longest-special-path/) · Hard · 灵茶山艾府：[树上滑窗（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

昨天看错题号跳过了10题，今天补上

3425.最长特殊路径

[3425. 最长特殊路径 - 力扣（LeetCode）](https://leetcode.cn/problems/longest-special-path/description/)

题目给出一颗根节点为节点0的无向树，树中有n个节点，标号为0到n - 1。这里n的规模可达50000。这棵树通过一个长度为n - 1的二维数组edges表示，其中edges\[i\] \= \[u\[i\], v\[i\], length\[i\]\]，表示节点u\[i\]和v\[i\]之间有一条长度为length\[i\]的边，所有的length\[i\]都在1到1000之间。另外还给出一个整数数组nums，其中nums\[i\]表示节点i的值。

定义特殊路径为树中一条从祖先节点往下到后代节点，且经过节点的值互不相同的路径。

问树中最长，且经过节点数最少的特殊路径的长度以及经过的节点数是多少。

由于题目中length的长度都为整数，那么对于某个节点p，以p为终点的最长的特殊路径，就必然是以p为终点的所有特殊路径中起点最靠上的那一条。而对于这个最靠上的起点，则可以通过动态规划的方法来解决。不妨设p的父亲节点为fa\[p\]，且nums\[p\]在根节点到fa\[p\]这条路径上最后一次出现的位置为last\[nums\[p\]\]，那么以p为终点的最靠上的起点start\[p\]就是：

1、以fa\[p\]为终点的最靠上的起点start\[fa\[p\]\]

2、last\[nums\[p\]\]向下走一步的节点

这两个节点中靠下的那一个。理解起来也很直观。start\[fa\[p\]\]保证了start\[fa\[p\]\]到fa\[p\]这条路径上没有重复出现的nums，但是再往上就会出现重复了。另一方面，在节点p加入后，也需要保证nums\[p\]没有重复出现，因此需要保证start\[p\]在last\[nums\[p\]\]的下面。

在得到start[p]之后，接下来需要想办法计算start[p]到p之间路径的长度。这是一个区间和问题，同样可以通过转化为前缀和来处理，这里的前缀和指的是从根节点到当前节点的路径的距离之和。

为了配合前缀和的计算，上面start和last的定义可以从具体节点修改为对应节点的深度，这样就可以直接利用这个深度作为前缀和数组中的下标，从而计算区间和。

在具体实现上，可以从根节点开始向下做一次dfs，使用哈希表last记录每种nums在当前dfs路径上最后一次出现的深度，那么对于当前节点now，其在树中的深度为level，其父亲节点为fa，同时fa的最佳起点的深度为pre_start，从根节点到fa的路径长度前缀和数组为s，那么：

1、首先可以通过max(last\[nums\[now\]\] + 1, pre_start)计算now对应的最佳起点的深度start

2、通过s计算路径长度，通过level与start计算路径上节点的数量，然后更新答案

3、使用临时变量pre_last记录last\[nums\[now\]\]，然后将last\[nums\[now\]\]更新为level，为接下来的递归计算做准备

4、遍历now的所有孩子节点nxt，使用now到nxt的距离更新前缀和数组s并递归计算以nxt为终点的最佳路径长度，计算完成后将s中最后这一项删去

5、将last\[nums\[now\]\]还原为pre_last然后回溯

最后附上python代码：

```python
class Solution(object):
    def longestSpecialPath(self, edges, nums):
        """
        :type edges: List[List[int]]
        :type nums: List[int]
        :rtype: List[int]
        """
        
        n = len(edges) + 1
        g = {x : {} for x in range(n)}

        for x, y, w in edges:
            g[x][y] = w
            g[y][x] = w

        last = {}
        for v in nums:
            last[v] = -1

        def dfs(now, fa, pre_start, last, s, level, res):
            start = max(last[nums[now]] + 1, pre_start)
            if start < level:
                length = s[-1] - s[start]
                cnt = level - start + 1
                if res[0] < length or (res[0] == length and res[1] > cnt):
                    res[0] = length
                    res[1] = cnt

            pre_last = last[nums[now]]
            last[nums[now]] = level
            for nxt in g[now]:
                if nxt == fa:
                    continue
                s.append(s[-1] + g[now][nxt])
                dfs(nxt, now, start, last, s, level + 1, res)
                s.pop()
            last[nums[now]] = pre_last

        res = [0, 1]
        dfs(0, -1, 0, last, [0], 0, res)
        return res
```
