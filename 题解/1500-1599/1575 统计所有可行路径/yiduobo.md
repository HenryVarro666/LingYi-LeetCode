---
title: "1575. 统计所有可行路径"
aliases: ["yiduobo的每日leetcode 1575.统计所有可行路径"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/429572086"
zhihu_id: "429572086"
zhihu_title: "yiduobo的每日leetcode 1575.统计所有可行路径"
question_id: "1575"
question: "统计所有可行路径"
problem_url: "https://leetcode.cn/problems/count-all-possible-routes/"
created: "2021-11-04T23:25:43+08:00"
updated: "2021-11-04T23:25:43+08:00"
upvotes: 0
comments: 0
---

# 1575. 统计所有可行路径

> **[yiduobo的每日leetcode 1575.统计所有可行路径](https://zhuanlan.zhihu.com/p/429572086) · 知乎 · 2021-11-04 · 赞同 0**
> 力扣：[1575. 统计所有可行路径](https://leetcode.cn/problems/count-all-possible-routes/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1575.统计所有可行路径

[力扣](https://leetcode-cn.com/problems/count-all-possible-routes/)

动态规划的题目，令f[i][j]表示邮箱里还剩i升油，最后走到位置j的方案总数，那么首先就有f[fuel][start] \= 1，其他的f则初始化为0。

接下来考虑一般情况。对于f[i][j]而言，需要枚举其是从哪个城市走过来的。于是可以枚举上一个城市k，那么从k走到j就消耗了abs(locations[j] - locations[k])的油，于是有

$f[i][j] = \sum_{k=0}^{n-1}{f[i + abs(locations[j] - locations[k])][k]}$

其中k需要满足k不等于j，且i + abs(locations[j] - locations[k])][k] \<\= fuel

具体实现时，由于所有状态都是从油量更多的状态转移过来的，因此需要从大到小枚举油量进行求解。

另外，这个做法实际上忽略了题目中设定的在一条二维直线上行走的性质。换言之，题目可以认为是在一条数轴上左右横跳，即最终的行进顺序必然是按向左、向右、再向左、再向右这种顺序排布的，当然，第一步也是可以向右，然后再向左的。

如果将两个方向的操作分开求解，那么题目看上去应该可以转化成类似前缀以及后缀来进行求解，即无需再枚举上一个城市，而是只需要从同向的上一个相邻城市进行转移就好了。不过我在这里枚举把细节想清楚，最后并没有尝试实现。

最后附上python代码，依然是上面最朴素的做法，时间复杂度为O(fuel \* n^2)：

```python
class Solution(object):
    def countRoutes(self, locations, start, finish, fuel):
        """
        :type locations: List[int]
        :type start: int
        :type finish: int
        :type fuel: int
        :rtype: int
        """

        n = len(locations)
        f = [[0] * n for _ in range(fuel + 1)]
        f[fuel][start] = 1
        mod = 10 ** 9 + 7
        for i in range(fuel - 1, -1, -1):
            for j in range(n):
                for k in range(n):
                    if j != k and i + abs(locations[j] - locations[k]) <= fuel:
                        f[i][j] += f[i + abs(locations[j] - locations[k])][k]
                        f[i][j] %= mod
        
        res = 0
        for i in range(fuel, -1, -1):
            res += f[i][finish]
            res %= mod
        
        return res
```
