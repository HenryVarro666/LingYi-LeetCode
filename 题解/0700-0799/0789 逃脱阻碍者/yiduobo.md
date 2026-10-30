---
title: "789. 逃脱阻碍者"
aliases: ["yiduobo的每日leetcode 789.逃脱阻碍者"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/341376434"
zhihu_id: "341376434"
zhihu_title: "yiduobo的每日leetcode 789.逃脱阻碍者"
question_id: "789"
question: "逃脱阻碍者"
problem_url: "https://leetcode.cn/problems/escape-the-ghosts/"
created: "2021-01-02T15:37:03+08:00"
updated: "2021-01-02T15:37:03+08:00"
upvotes: 0
comments: 0
---

# 789. 逃脱阻碍者

> **[yiduobo的每日leetcode 789.逃脱阻碍者](https://zhuanlan.zhihu.com/p/341376434) · 知乎 · 2021-01-02 · 赞同 0**
> 力扣：[789. 逃脱阻碍者](https://leetcode.cn/problems/escape-the-ghosts/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

789.逃脱阻碍者

[力扣](https://leetcode-cn.com/problems/escape-the-ghosts/)

乍一看感觉不知道如何下手，不过仔细看题目描述可以发现，在终点处相遇同样不能算是逃脱成功，那么对于所有阻碍者来说，只需要尽可能早的到达终点，然后守株待兔即可。

当然，也可能出现中途就已经拦截下来的情况，不过对于这种情况，阻碍者从拦截地点到达终点所需的步数与逃脱者相同，因此如果可能出现中途的拦截，那么必然可以出现终点的拦截。

有了上面的结论，我们就只需要分别考虑逃脱者与阻碍者到终点的最短时间。由于题目中没有障碍物之类的东西，因此这个最短时间就是横纵坐标的绝对值之和。

计算出到达终点所需时间之后，若逃脱者所需时间是最小的，那么逃脱成功，否则逃脱失败。

题目本身难度不大，但是思路的转化比较重要。对于阻碍者而言，其最优选择是尽早到达终点。若其在最优选择的情况下依然拦截不到逃脱者，那么其无论如何都不可能拦截到逃脱者。

最后附上python代码：

```python
class Solution(object):
    def escapeGhosts(self, ghosts, target):
        """
        :type ghosts: List[List[int]]
        :type target: List[int]
        :rtype: bool
        """

        dis = abs(target[0]) + abs(target[1])
        for x, y in ghosts:
            if abs(x - target[0]) + abs(y - target[1]) <= dis:
                return False

        return True
```
