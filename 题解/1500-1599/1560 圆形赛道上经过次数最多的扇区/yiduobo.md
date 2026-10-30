---
title: "1560. 圆形赛道上经过次数最多的扇区"
aliases: ["yiduobo的每日leetcode 1560.圆形赛道上经过次数最多的扇区"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/426983615"
zhihu_id: "426983615"
zhihu_title: "yiduobo的每日leetcode 1560.圆形赛道上经过次数最多的扇区"
question_id: "1560"
question: "圆形赛道上经过次数最多的扇区"
problem_url: "https://leetcode.cn/problems/most-visited-sector-in-a-circular-track/"
created: "2021-10-29T20:11:24+08:00"
updated: "2021-10-29T20:11:25+08:00"
upvotes: 0
comments: 0
---

# 1560. 圆形赛道上经过次数最多的扇区

> **[yiduobo的每日leetcode 1560.圆形赛道上经过次数最多的扇区](https://zhuanlan.zhihu.com/p/426983615) · 知乎 · 2021-10-29 · 赞同 0**
> 力扣：[1560. 圆形赛道上经过次数最多的扇区](https://leetcode.cn/problems/most-visited-sector-in-a-circular-track/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1560.圆形赛道上经过次数最多的扇区

[力扣](https://leetcode-cn.com/problems/most-visited-sector-in-a-circular-track/)

看上去很复杂的样子，但是仔细思考可以发现，从起点开始跑任意的整圈，最终都会回到起点。一个整圈将经过每个扇区一次，因此跑任意整圈经过各个扇区的次数都是一样的。如果将这些整圈省去，那么剩下的就是从起点跑到终点的这一段路程，因此只需要找出这一段路程经过了哪些扇区即可。

值得注意的是，这里也可能出现跨圈的情况，即起点大于终点时，多出来的这一段路程是由起点到赛道末尾，以及赛道末尾到终点这两部分组成的。

最后附上python代码：

```python
class Solution(object):
    def mostVisited(self, n, rounds):
        """
        :type n: int
        :type rounds: List[int]
        :rtype: List[int]
        """

        l = rounds[0]
        r = rounds[-1]
        
        if l <= r:
            return range(l, r + 1)
        else:
            return range(1, r + 1) + range(l, n + 1)
```
