---
title: "3532. 针对图的路径存在性查询I"
aliases: ["yiduobo的每日leetcode 3532.针对图的路径存在性查询I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "题单/常用数据结构", "题单/常用数据结构/七-并查集"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1904717848787530022"
zhihu_id: "1904717848787530022"
zhihu_title: "yiduobo的每日leetcode 3532.针对图的路径存在性查询I"
question_id: "3532"
question: "针对图的路径存在性查询 I"
problem_url: "https://leetcode.cn/problems/path-existence-queries-in-a-graph-i/"
difficulty: "Medium"
created: "2025-05-14T22:06:46+08:00"
updated: "2025-05-14T22:06:46+08:00"
upvotes: 0
comments: 0
---

# 3532. 针对图的路径存在性查询I

> **[yiduobo的每日leetcode 3532.针对图的路径存在性查询I](https://zhuanlan.zhihu.com/p/1904717848787530022) · 知乎 · 2025-05-14 · 赞同 0**
> 力扣：[3532. 针对图的路径存在性查询 I](https://leetcode.cn/problems/path-existence-queries-in-a-graph-i/) · Medium · 灵茶山艾府：[两种方法：二分 / 连通块编号（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3532.针对图的路径存在性查询I

[3532. 针对图的路径存在性查询 I - 力扣（LeetCode）](https://leetcode.cn/problems/path-existence-queries-in-a-graph-i/description/)

题目给出一个整数n，表示图中的节点数量，这些节点从0到n - 1编号。同时给出一个长度为n的整数数组nums，该数组按非递减的顺序排列，以及一个整数maxDiff。

对于一组节点对(i, j)，若|nums[i] - nums[j]| \<\= maxDiff，那么这两个节点间存在一条无向边。

另外给出一个二维数组queries，对于其中的每个查询queries\[index\] \= \[u\[index\], v\[index\]\]，需要判断u\[index\]与v\[index\]之间是否存在路径。

由于题目保证了nums按照非递减的顺序排列，那么对于一组i \< j，若nums[j] - nums[i] > maxDiff，说明i和j之间不存在边，同时i与所有大于j的节点之间，以及j与所有小于i的节点之间也不可能存在边，因为nums是单调的。因此只需一趟遍历，根据相邻元素之差是否小于等于maxDiff将nums划分为若干段，每一段中的节点可以互相抵达，不同段间则不能互相抵达。在划分的过程中，可以使用一个哈希表belong记录每个节点属于的段，接下来就可以利用belong判断queries中每组查询的节点间是否存在路径了。

最后附上python代码：

```python
class Solution(object):
    def pathExistenceQueries(self, n, nums, maxDiff, queries):
        """
        :type n: int
        :type nums: List[int]
        :type maxDiff: int
        :type queries: List[List[int]]
        :rtype: List[bool]
        """
        
        tot = 0
        belong = [None] * n
        p = 0
        while p < len(nums):
            q = p + 1
            belong[p] = tot
            while q < len(nums) and nums[q] - nums[q - 1] <= maxDiff:
                belong[q] = tot
                q += 1
            
            p = q
            tot += 1
        
        res = []
        for x, y in queries:
            res.append(belong[x] == belong[y])
        return res
```
