---
title: "2508. 添加边使所有节点度数都为偶数"
aliases: ["yiduobo的每日leetcode 2508.添加边使所有节点度数都为偶数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/图论算法", "题单/贪心算法", "题单/图论算法/九-其他", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/634312050"
zhihu_id: "634312050"
zhihu_title: "yiduobo的每日leetcode 2508.添加边使所有节点度数都为偶数"
question_id: "2508"
question: "添加边使所有节点度数都为偶数"
problem_url: "https://leetcode.cn/problems/add-edges-to-make-degrees-of-all-nodes-even/"
difficulty: "Hard"
rating: 2060
created: "2023-06-04T01:00:41+08:00"
updated: "2023-06-04T01:00:41+08:00"
upvotes: 0
comments: 0
---

# 2508. 添加边使所有节点度数都为偶数

> **[yiduobo的每日leetcode 2508.添加边使所有节点度数都为偶数](https://zhuanlan.zhihu.com/p/634312050) · 知乎 · 2023-06-04 · 赞同 0**
> 力扣：[2508. 添加边使所有节点度数都为偶数](https://leetcode.cn/problems/add-edges-to-make-degrees-of-all-nodes-even/) · Hard · 灵茶山艾府：[分类讨论（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2508.添加边使所有节点度数都为偶数

[力扣](https://leetcode.cn/problems/add-edges-to-make-degrees-of-all-nodes-even/)

题目要求将图中所有节点的度都变为偶数，那么自然是先要进行一趟遍历，计算每个节点的度数。由于题目最多只能添加两条边，而一条边可以修改两个节点度的奇偶性，那么若度为奇数的节点大于4，答案必然是False。

接下来只需要来度为奇数的节点数为0、2、4这三种情况：

1、没有度为奇数的节点：

此时无需进行任何操作，答案必然为True。

2、度为奇数的节点有两个：

此时最直观的处理方法就是在这两个点之间添加一条边，但是如果这两个点之间已经有边了，那么就只能另找一个度为偶数的节点，从这两个度为奇数的节点分别发射一条边到该节点，此时则要求这个度为偶数的节点与这两个度为奇数的节点之间都不存在边。若找不到这样的节点，则只能返回False。

3、度为奇数的节点有四个：

此时就只能内部消化了。一共三种连边的方案，分别为(0-1、2-3)，(0-2、1-3)，(0-3，1-2)。此时只需分别检测这三种方案的可行性，也就是连边方案中的两个节点之间原来都没有边才可行。

最后附上python代码：

```python
class Solution(object):
    def isPossible(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: bool
        """

        g = [set() for _ in range(n + 1)]
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)
        
        nodes = []
        for x in range(1, n + 1):
            if len(g[x]) % 2 == 1:
                nodes.append(x)
        
        if len(nodes) == 0:
            return True

        elif len(nodes) == 2:
            if nodes[0] not in g[nodes[1]]:
                return True
            else:
                for x in range(1, n + 1):
                    if len(g[x]) % 2 == 0 and nodes[0] not in g[x] and nodes[1] not in g[x]:
                        return True
                return False

        elif len(nodes) == 4:
            if nodes[0] not in g[nodes[1]] and nodes[2] not in g[nodes[3]]:
                return True
            if nodes[0] not in g[nodes[2]] and nodes[1] not in g[nodes[3]]:
                return True
            if nodes[0] not in g[nodes[3]] and nodes[1] not in g[nodes[2]]:
                return True
            return False
        
        return False
```
