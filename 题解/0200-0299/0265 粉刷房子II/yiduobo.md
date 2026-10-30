---
title: "265. 粉刷房子II"
aliases: ["yiduobo的每日leetcode 265.粉刷房子II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/593492075"
zhihu_id: "593492075"
zhihu_title: "yiduobo的每日leetcode 265.粉刷房子II"
question_id: "265"
question: "粉刷房子II"
problem_url: "https://leetcode.cn/problems/paint-house-ii/"
created: "2022-12-21T23:52:03+08:00"
updated: "2022-12-21T23:52:03+08:00"
upvotes: 0
comments: 0
---

# 265. 粉刷房子II

> **[yiduobo的每日leetcode 265.粉刷房子II](https://zhuanlan.zhihu.com/p/593492075) · 知乎 · 2022-12-21 · 赞同 0**
> 力扣：[265. 粉刷房子II](https://leetcode.cn/problems/paint-house-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

265.粉刷房子II

[力扣](https://leetcode.cn/problems/paint-house-ii/)

之前256题的加强版，从3种颜色升级到了k种颜色，不过之前的做法依然适用。令f[i][j]表示粉刷前i栋房子，最后一栋房子的颜色为j时需要的最小代价，那么对于f[i][j]，就有

f[i][j] \= min(f[i - 1][k]) + cost[i][j]，这里的k不能等于j

这种算法的时间复杂度为O(nk^2)，对于本题的数据规模是完全够用了，不过也还存在更好的做法。

注意到转移的复杂度主要集中在求min(f[i - 1][k])这里。如果不存在k不等于j的限制，那么就可以在i - 1这一轮都计算完毕之后，再遍历所有的颜色，找出其中的最小值并将这个值记录下来，这样一来f[i][j]的更新就可以直接通过这个最小值来进行了

而本题在加上k不等于j的限制之后，就可能出现两种情况：

1、第i - 1轮最小值的颜色与j不同。

这种情况下可以直接使用i - 1这一轮的最小值来进行状态转移

2、第i - 1轮最小值的颜色与j相同。

此时不能使用i - 1这一轮的最小值来进行状态转移，因为这样的话就相当于f[i][j]从f[i - 1][j]转移过来了。因此就需要从剩下的f[i - 1][k]中找出最小值，其中k不等于j。

这种情况下，重新遍历f[i - 1][k]找出最小值，或者在找出f[i - 1]最小值的同时也找出次小值都是可行的做法。

对于前者，由于每一轮只会出现一次这种情况，因此遍历的复杂度均摊下来也是O(1)的。

对于后者，第i - 1轮中的次小值实际上就是f[i - 1][k]中的最小值，此时直接使用i - 1轮的次小值来进行状态转移就行了

另外，与256题相同，本题的状态转移也只与上一轮的状态有关，因此可以滚动掉i这一维来节省空间。

最后附上python代码：

```python
class Solution(object):
    def minCostII(self, costs):
        """
        :type costs: List[List[int]]
        :rtype: int
        """

        for index in range(len(costs)):
            if index == 0:
                f = costs[0][:]
            else:
                g = f[:]
                for color in range(len(g)):
                    if color == first_color:
                        f[color] = second_val + costs[index][color]
                    else:
                        f[color] = first_val + costs[index][color]
            
            first_val = None
            first_color = None
            second_val = None
            second_color = None
            for color in range(len(f)):
                if first_val is None or f[color] < first_val:
                    first_val, second_val = f[color], first_val
                    first_color, second_color = color, first_color
                elif second_val is None or f[color] < second_val:
                    second_val = f[color]
                    second_color = color
        
        return min(f)
```
