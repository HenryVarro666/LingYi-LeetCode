---
title: "3486. 最长特殊路径II"
aliases: ["yiduobo的每日leetcode 3486.最长特殊路径II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "leetcode/depth-first-search", "leetcode/hash-table", "leetcode/sliding-window", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1897416000024052873"
zhihu_id: "1897416000024052873"
zhihu_title: "yiduobo的每日leetcode 3486.最长特殊路径II"
question_id: "3486"
question: "最长特殊路径 II"
problem_url: "https://leetcode.cn/problems/longest-special-path-ii/"
difficulty: "Hard"
rating: 2925
created: "2025-04-23T22:08:58+08:00"
updated: "2025-04-23T22:08:58+08:00"
upvotes: 0
comments: 0
---

# 3486. 最长特殊路径II

> **[yiduobo的每日leetcode 3486.最长特殊路径II](https://zhuanlan.zhihu.com/p/1897416000024052873) · 知乎 · 2025-04-23 · 赞同 0**
> 力扣：[3486. 最长特殊路径 II](https://leetcode.cn/problems/longest-special-path-ii/) · Hard · 灵茶山艾府：[树上滑窗，只需在 3425 的基础上改几行（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3486.最长特殊路径II

[3486. 最长特殊路径 II - 力扣（LeetCode）](https://leetcode.cn/problems/longest-special-path-ii/description/)

题目给出一颗根节点为节点0的无向树，树中有n个节点，标号为0到n - 1。这里n的规模可达50000。这棵树通过一个长度为n - 1的二维数组edges表示，其中edges\[i\] \= \[u\[i\], v\[i\], length\[i\]\]，表示节点u\[i\]和v\[i\]之间有一条长度为length\[i\]的边，所有的length\[i\]都在1到1000之间。另外还给出一个整数数组nums，其中nums\[i\]表示节点i的值。

定义特殊路径为树中一条从祖先节点往下到后代节点，要求路径上的节点值除了一个值之外都仅出现一次，而这个值也最多只能出现两次。

问树中最长，且经过节点数最少的特殊路径的长度以及经过的节点数是多少。

本题与之前的3425题类似，不过本题中的路径相比3425题的路径稍微宽松点，允许某个值出现两次。

[yiduobo：yiduobo的每日leetcode 3425.最长特殊路径](https://zhuanlan.zhihu.com/p/1889443746753528088)

处理方法也与之前类似，不同之处在于由于本题允许某个值出现两次，那么在计算节点now对应的没有重复值的路径起点start时，还需要额外计算start_with_dup，表示带重复值的最靠上的起点。那么对于start_with_dup，如果这次重复的机会在之前就用过了，start_with_dup就受限于pre_start_with_dup以及nums[now]上次出现的位置加上1，其中pre_start_with_dup表示now的父亲节点fa的start_with_dup；除此之外，若这次重复的机会在之前还没有被用过，那么start_with_dup则受限于pre_start以及nums[now]倒数第二次出现的位置加上1。为此还需要记录nums[now]最近两次出现的位置，也就是说之前3425题中的last[v]从最近v最近出现的位置替换成了长度为2的list，记录v最近两次出现的位置。这样一来，就有

start_with_dup \= min(max(pre_start_with_dup, last\[nums\[now\]\]\[1\] + 1), max(pre_start, last\[nums\[now\]\]\[0\] + 1))

接下来，只需通过s[start_with_dup]而不是3425题中的s[start]来计算路径上元素之和就行了。

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
            last[v] = [-1, -1]

        def dfs(now, fa, pre_start, pre_start_with_dup, last, s, level, res):
            start = max(last[nums[now]][1] + 1, pre_start)
            start_with_dup = min(max(pre_start_with_dup, last[nums[now]][1] + 1), max(pre_start, last[nums[now]][0] + 1))
            if start_with_dup < level:
                length = s[-1] - s[start_with_dup]
                cnt = level - start_with_dup + 1
                if res[0] < length or (res[0] == length and res[1] > cnt):
                    res[0] = length
                    res[1] = cnt

            pre_last = last[nums[now]][0]
            last[nums[now]][0] = last[nums[now]][1]
            last[nums[now]][1] = level
            for nxt in g[now]:
                if nxt == fa:
                    continue
                s.append(s[-1] + g[now][nxt])
                dfs(nxt, now, start, start_with_dup, last, s, level + 1, res)
                s.pop()
            last[nums[now]][1] = last[nums[now]][0]
            last[nums[now]][0] = pre_last

        res = [0, 1]
        dfs(0, -1, 0, 0, last, [0], 0, res)
        return res
```
