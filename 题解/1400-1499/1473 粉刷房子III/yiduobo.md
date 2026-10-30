---
title: "1473. 粉刷房子III"
aliases: ["yiduobo的每日leetcode 1473.粉刷房子III"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/414732273"
zhihu_id: "414732273"
zhihu_title: "yiduobo的每日leetcode 1473.粉刷房子III"
question_id: "1473"
question: "粉刷房子III"
problem_url: "https://leetcode.cn/problems/paint-house-iii/"
created: "2021-09-27T23:27:46+08:00"
updated: "2021-09-27T23:27:46+08:00"
upvotes: 0
comments: 0
---

# 1473. 粉刷房子III

> **[yiduobo的每日leetcode 1473.粉刷房子III](https://zhuanlan.zhihu.com/p/414732273) · 知乎 · 2021-09-27 · 赞同 0**
> 力扣：[1473. 粉刷房子III](https://leetcode.cn/problems/paint-house-iii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1473.粉刷房子III

[力扣](https://leetcode-cn.com/problems/paint-house-iii/)

动态规划的题目，令f[i][j][k]表示前i栋房子，组成了j个街区，最后一个街区房子的颜色为k时的最小代价。

为了对其数组下标，可以将houses里面的颜色全部减去1，接下来先考察边界情况。

1、当i等于0时，此时的j必然只能是1：

若此时houses[0]为-1，需要选择一种颜色，那么此时需要枚举每种颜色k，就有

f[0][1][k] \= cost[i][k]

若此时houses[0]不为-1，那么此时没有粉刷的必要，就有

f\[0\]\[1\]\[houses\[0\]\] \= 0

2、接下来考察一般情况。对于i > 0的情况，此时可能形成的街区也最多只有i + 1个，那么此时j的枚举范围就是1到i + 1。与上面类似：

若此时houses[i]为-1，需要选择一种颜色，接下来同样是枚举每种颜色k，若在当前房子刷上这种颜色，那么此时也有两种情况：

2-1）当前刷的颜色k与上一个街区的颜色一致，那么就有

f[i][j][k] \= f[i - 1][j][k] + cost[i][k]

2-2）当前刷的颜色k与上一个街区不同，那么需要枚举上一个街区的颜色p，就有

f[i][j][k] \= min(f[i][j][k], f[i - 1][j - 1][p] + cost[i][k])

若此时houses[i]不为-1，同样是需要考察当前刷的颜色与上一个街区是否相同，那么需要枚举上一个街区的颜色k，就有

2-3）当前houses[i]的颜色与上一个街区的颜色一致，那么就有

f[i][j][k] \= min(f[i][j][k], f[i - 1][j][k])

2-4）当前houses[i]的颜色与上一个街区的颜色不同，那么就有

f\[i\]\[j\]\[houses\[i\]\] \= min(f\[i\]\[j\]\[houses\[i\]\], f\[i - 1\]\[j - 1\]\[k\])

动态规划完成后，需要枚举每种颜色k，而最终答案就是f[m - 1][target - 1][k]中的最小值。

注意到这里每一轮的状态只与上一轮有关，因此可以通过滚动数组优化掉i这一维。

除此之外，仔细观察状态转移方程，每次需要枚举上一个街区颜色时，转移方程分别为

2-2）中的f[i][j][k] \= min(f[i][j][k], f[i - 1][j - 1][p] + cost[i][k])

2-4）中的f\[i\]\[j\]\[houses\[i\]\] \= min(f\[i\]\[j\]\[houses\[i\]\], f\[i - 1\]\[j - 1\]\[k\])

可以发现，后面这两项实际上从(i - 1, j - 1)的组合状态转移到(i, j)的组合，而且取的都是其中的最小值，那么就可以在上一轮动态规划的过程中顺便记录下来这里的最小值，从而省去枚举的时间。当然，2-2）以及2-4）的前提条件是当前这一轮粉刷的颜色与上一个街区不同，因此在记录最小值时，需要记录下最小值、最小值对应的颜色以及次小值。若最小值对应的颜色与上一个街区相同时，状态转移的时候就应当使用次小值。

不过我在这里偷懒，并没有实现这个优化。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, houses, cost, m, n, target):
        """
        :type houses: List[int]
        :type cost: List[List[int]]
        :type m: int
        :type n: int
        :type target: int
        :rtype: int
        """

        houses = [x - 1 for x in houses]
        
        for i in range(m):
            f = [[None] * n for _ in range(target + 1)]
            if i == 0:
                if houses[i] == -1:
                    for k in range(n):
                        f[1][k] = cost[0][k]
                else:
                    f[1][houses[i]] = 0
            else:
                for j in range(1, target + 1):
                    if j > i + 1:
                        continue
                    if houses[i] == -1:
                        for k in range(n):
                            if g[j][k] is not None and f[j][k] is None:
                                f[j][k] = g[j][k] + cost[i][k]
                            for p in range(n):
                                if p != k:
                                    if g[j - 1][p] is not None and (f[j][k] is None or g[j - 1][p] + cost[i][k] < f[j][k]):
                                        f[j][k] = g[j - 1][p] + cost[i][k]
                    else:
                        for k in range(n):
                            if k == houses[i]:
                                if g[j][k] is not None and (f[j][houses[i]] is None or g[j][k] < f[j][houses[i]]):
                                    f[j][houses[i]] = g[j][k]
                            else:
                                if g[j - 1][k] is not None and (f[j][houses[i]] is None or g[j - 1][k] < f[j][houses[i]]):
                                    f[j][houses[i]] = g[j - 1][k]
        
            g = f[:]

        res = None
        for k in range(n):
            if f[-1][k] is not None and (res is None or res > f[-1][k]):
                res = f[-1][k]
        
        if res is None:
            res = -1
        
        return res
```
