---
title: "3965. 任务完成时间I"
aliases: ["yiduobo的每日leetcode 3965.任务完成时间I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2052124487328573279"
zhihu_id: "2052124487328573279"
zhihu_title: "yiduobo的每日leetcode 3965.任务完成时间I"
question_id: "3965"
question: "任务完成时间 I"
problem_url: "https://leetcode.cn/problems/finish-time-of-tasks-i/"
difficulty: "Medium"
rating: 1699
created: "2026-06-23T22:46:35+08:00"
updated: "2026-06-23T22:46:36+08:00"
upvotes: 2
comments: 0
---

# 3965. 任务完成时间I

> **[yiduobo的每日leetcode 3965.任务完成时间I](https://zhuanlan.zhihu.com/p/2052124487328573279) · 知乎 · 2026-06-23 · 赞同 2**
> 力扣：[3965. 任务完成时间 I](https://leetcode.cn/problems/finish-time-of-tasks-i/) · Medium · 灵茶山艾府：[自底向上 DFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3965.任务完成时间I

<https://leetcode.cn/problems/finish-time-of-tasks-i/description/>

题目给出一个整数n，表示项目中的任务数量，这些任务的标号从0到n - 1，以任务0为根节点的树的形式连接。另外给出一个长度为n - 1的二维整数数组edges，其中edges\[index\] \= \[u\[index\], v\[index\]\]，表示任务u\[index\]是任务v\[index\]的父节点。

同时给出一个长度为n的数组bastTime，其中baseTime[index]表示完成任务index所需的时间。

对于任务index，其完成时间计算如下：

- 叶子任务：完成时间为baseTime[index]
- 非叶子任务：
   - 令earliest和latest分别为其子节点中最小和最大的完成时间
   - 令ownDuration为(latest - earliest) + baseTime[index]
   - 完成时间为latest + ownDuration

问根任务0的完成时间。

题目中的任务呈树形构造，且每个非叶子任务的完成时间与孩子节点的完成时间，那么在这里就可以从根节点向下进行dfs，对于当前节点index，若其为叶子节点，那么完成时间就是baseTime[index]，反之，则先遍历其所有孩子节点并递归计算这些节点的完成时间，记录其中最小和最大作为earliest和latest，然后按照题目描述中的latest + (latest - earliest) + baseTime[index]计算完成时间。

从0号开始向下dfs计算，最后回到0号节点，得到最终答案。

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
        
        def dfs(now, fa):
            earliest = None
            latest = None
            for nxt in g[now]:
                if nxt == fa:
                    continue
                t = dfs(nxt, now)
                if earliest is None or earliest > t:
                    earliest = t
                if latest is None or latest < t:
                    latest = t
            
            if earliest is None:
                return baseTime[now]
            else:
                return latest + (latest - earliest) + baseTime[now]
        
        return dfs(0, -1)
```
