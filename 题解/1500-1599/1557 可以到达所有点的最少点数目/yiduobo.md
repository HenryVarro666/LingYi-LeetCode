---
title: "1557. 可以到达所有点的最少点数目"
aliases: ["yiduobo的每日leetcode 1557.可以到达所有点的最少点数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/426965592"
zhihu_id: "426965592"
zhihu_title: "yiduobo的每日leetcode 1557.可以到达所有点的最少点数目"
question_id: "1557"
question: "可以到达所有点的最少点数目"
problem_url: "https://leetcode.cn/problems/minimum-number-of-vertices-to-reach-all-nodes/"
created: "2021-10-28T23:30:18+08:00"
updated: "2021-10-28T23:30:18+08:00"
upvotes: 0
comments: 0
---

# 1557. 可以到达所有点的最少点数目

> **[yiduobo的每日leetcode 1557.可以到达所有点的最少点数目](https://zhuanlan.zhihu.com/p/426965592) · 知乎 · 2021-10-28 · 赞同 0**
> 力扣：[1557. 可以到达所有点的最少点数目](https://leetcode.cn/problems/minimum-number-of-vertices-to-reach-all-nodes/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1557.可以到达所有点的最少点数目

[力扣](https://leetcode-cn.com/problems/minimum-number-of-vertices-to-reach-all-nodes/)

对于图中的点而言，若一个点的入度为0，那么就无法通过其他点到达该点，反之若入度不为0，那么必然存在另一个点可以到达这个点，因此只需要选出所有入度为0的点，就能保证可以从这些点出发到达所有点了。

最后附上python代码：

```python
class Solution(object):
    def findSmallestSetOfVertices(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: List[int]
        """

        ind = [0] * n
        for x, y in edges:
            ind[y] += 1
        
        res = []
        for index in range(n):
            if ind[index] == 0:
                res.append(index)
        
        return res
```
