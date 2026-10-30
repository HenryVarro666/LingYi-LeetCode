---
title: "1791. 找出星型图的中心节点"
aliases: ["yiduobo的每日leetcode 1791.找出星型图的中心节点"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/463369041"
zhihu_id: "463369041"
zhihu_title: "yiduobo的每日leetcode 1791.找出星型图的中心节点"
question_id: "1791"
question: "找出星型图的中心节点"
problem_url: "https://leetcode.cn/problems/find-center-of-star-graph/"
difficulty: "Easy"
created: "2022-01-31T17:59:26+08:00"
updated: "2022-01-31T17:59:26+08:00"
upvotes: 0
comments: 0
---

# 1791. 找出星型图的中心节点

> **[yiduobo的每日leetcode 1791.找出星型图的中心节点](https://zhuanlan.zhihu.com/p/463369041) · 知乎 · 2022-01-31 · 赞同 0**
> 力扣：[1791. 找出星型图的中心节点](https://leetcode.cn/problems/find-center-of-star-graph/) · Easy · 灵茶山艾府：[O(1) 一行解法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1791.找出星型图的中心节点

[力扣](https://leetcode-cn.com/problems/find-center-of-star-graph/)

题目中定义的中心节点度数为n - 1，那么只需要统计每个节点的度数，然后一趟遍历找出其中度数为n - 1的节点即可。

最后附上python代码：

```python
class Solution(object):
    def findCenter(self, edges):
        """
        :type edges: List[List[int]]
        :rtype: int
        """

        d = {}
        for x, y in edges:
            d[x] = d.get(x, 0) + 1
            d[y] = d.get(y, 0) + 1
        
        for x in d:
            if d[x] == len(d) - 1:
                return x
```
