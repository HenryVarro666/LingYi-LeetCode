---
title: "3493. 属性图"
aliases: ["yiduobo的每日leetcode 3493.属性图"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/union-find", "leetcode/graph", "leetcode/hash-table", "题单/常用数据结构", "题单/常用数据结构/七-并查集"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1899508763536364551"
zhihu_id: "1899508763536364551"
zhihu_title: "yiduobo的每日leetcode 3493.属性图"
question_id: "3493"
question: "属性图"
problem_url: "https://leetcode.cn/problems/properties-graph/"
difficulty: "Medium"
rating: 1565
created: "2025-04-27T23:15:17+08:00"
updated: "2025-04-27T23:15:17+08:00"
upvotes: 1
comments: 0
---

# 3493. 属性图

> **[yiduobo的每日leetcode 3493.属性图](https://zhuanlan.zhihu.com/p/1899508763536364551) · 知乎 · 2025-04-27 · 赞同 1**
> 力扣：[3493. 属性图](https://leetcode.cn/problems/properties-graph/) · Medium · 灵茶山艾府：[【模板】并查集（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3493.属性图

[3493. 属性图 - 力扣（LeetCode）](https://leetcode.cn/problems/properties-graph/description/)

题目给出一个大小为n \* m的二维整数数组properties以及一个整数k，n和m的大小都不超过100。另外定义一个函数intersect(a, b)，返回数组a和b中共有的不同整数的数量。

接下来要求构造一个无向图，其中每个节点i对应properties[i]。若intersect(properties[i], properties[j]) >\= k，那么在节点i和节点j之间连上一条边。

问这个图中连通分量的数量。

由于题目中n和m的规模都不大，因此可以直接暴力枚举节点对(i, j)，然后枚举properties[i]中的所有元素，检测其是否也出现在properties[j]当中，这个检测的过程可以通过集合来实现。若出现的相同元素数量same大于等于k，那么就说明i和j在同一个连通分量中，在这里则可以通过并查集来维护连通性。初始情况下可以设置最终答案为n，接下来若某一组节点对(i, j)属于不同连通分量，且出现的相同元素数量same大于等于k，就通过并查集合并i和j的祖先，并将答案减去1。

最后附上python代码：

```python
class Solution(object):
    def numberOfComponents(self, properties, k):
        """
        :type properties: List[List[int]]
        :type k: int
        :rtype: int
        """
        
        n = len(properties)
        num_set = []
        fa = []
        for index in range(n):
            num_set.append(set(properties[index]))
            fa.append(index)

        def find(x, fa):
            if fa[x] != x:
                fa[x] = find(fa[x], fa)
            return fa[x]

        res = n
        for i in range(n):
            for j in range(i + 1, n):
                same = 0
                for v in num_set[i]:
                    if v in num_set[j]:
                        same += 1
                
                if same >= k:
                    fa_i = find(i, fa)
                    fa_j = find(j, fa)
                    if fa_i != fa_j:
                        fa[fa_i] = fa_j
                        res -= 1
        
        return res
```
