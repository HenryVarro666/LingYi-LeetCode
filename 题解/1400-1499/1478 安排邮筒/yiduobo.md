---
title: "1478. 安排邮筒"
aliases: ["yiduobo的每日leetcode 1478.安排邮筒"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/415554160"
zhihu_id: "415554160"
zhihu_title: "yiduobo的每日leetcode 1478.安排邮筒"
question_id: "1478"
question: "安排邮筒"
problem_url: "https://leetcode.cn/problems/allocate-mailboxes/"
created: "2021-09-29T22:32:24+08:00"
updated: "2021-09-29T22:32:24+08:00"
upvotes: 0
comments: 0
---

# 1478. 安排邮筒

> **[yiduobo的每日leetcode 1478.安排邮筒](https://zhuanlan.zhihu.com/p/415554160) · 知乎 · 2021-09-29 · 赞同 0**
> 力扣：[1478. 安排邮筒](https://leetcode.cn/problems/allocate-mailboxes/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1478.安排邮箱

[力扣](https://leetcode-cn.com/problems/allocate-mailboxes/)

动态规划的题目，先将房子按下标从小到大排序，接下来令f[i][j]表示前i栋房子，安排j个邮筒的最小距离总和。那么对于f[i][j]：

1、首先考虑边界情况。当j等于1时，最终答案就是使用1个邮筒管理整个街区的代价。在这里不妨引入dis[l][r]表示使用一个邮筒管理第l到r这些房子所需的最小代价，那么这里就有

f[i][1] \= dis[0][i]

2、对于j > 1的情况：

2-1）若j >\= i + 1，那么此时可以为每栋房子都安排一个邮筒，于是有

f[i][j] \= 0

2-2）若j \< i + 1，那么可以从j - 1到i之间枚举一个cut_pos，由前j - 1个邮箱管理第0到cut_pos - 1栋房子，而后面的第cut_pos到第i栋房子则有最后一个邮箱管理，那么就有

f[i][j] \= f[cut_pos - 1][j - 1] + dis[cut_pos][i]

注意到这里j这一维每次只与上一轮有关，因此可以通过滚动数组优化掉这一维。

接下来则是需要求解出dis。对于dis[l][r]：

1、同样先考察边界情况。当l \= r时，dis[l][r]显然为0

2、当l \= r - 1时有三种情况：

方便起见，设邮箱的位置为p

2-1）当邮箱被安排在l前方时，那么就有

dis[l][r] \= (houses[l] - p) + (houses[r] - p)

将houses[r]写成houses[l] + (houses[r] - houses[l])，那么可以将式子变形为

dis[l][r] \= (houses[r] - houses[l]) + (houses[l] - p) \* 2

2-2）当邮箱被安排在l到r之间时，那么就有

dis[l][r] \= (p - houses[l]) + (houses[r] - p) \= houses[r] - houses[l]

2-3）当邮箱被安排在r后方时，那么就有

dis[l][r] \= (p - houses[l]) + (p - houses[r])

将houses[l]写成houses[r] - (houses[r] - houses[l])，那么可以将式子变形为

dis[l][r] \= (houses[r] - houses[l]) + (p - houses[r]) \* 2

对比这三种情况，可以发现此时将邮箱安排在houses[l]到houses[r]之间的任意点，其距离总和最小

3、更一般的，对于一个邮箱管理多栋房子的情况，若房子数目为奇数，那么应该将邮箱安排在最中间的房子，若房子数目为偶数，则应该将邮箱安排在最中间两栋房子之间。

具体证明也很简单，将所有房子从两侧开始，两两一组进行分组。若邮箱被安排在某一组房子的外侧，那么此时对于其更外侧组的房子而言，最终距离不变；而对于这一组房子以及其内侧的组的房子而言，根据情况2的结论，此时显然多出了一些距离，因此这种安排方式是不如将邮箱安排在最中央的。

根据上面的结论，就同样可以使用动态规划，对于dis[l][r]而言：

1、当l \= r时，就有

dis[l][r] \= 0

2、当l \< r时，就有

dis[l][r] \= dis[l + 1][r - 1] + houses[r] - houses[l]

最后附上python代码：

```python
class Solution(object):
    def minDistance(self, houses, k):
        """
        :type houses: List[int]
        :type k: int
        :rtype: int
        """

        houses = sorted(houses)
        n = len(houses)
        dis = [[None] * n for _ in range(n)]
        for l in range(n):
            for i in range(n):
                j = i + l
                if j > n - 1:
                    break
                if i == j:
                    dis[i][j] = 0
                elif i == j - 1:
                    dis[i][j] = houses[j] - houses[i]
                else:
                    dis[i][j] = dis[i + 1][j - 1] + houses[j] - houses[i]
        
        for j in range(1, k + 1):
            f = [None] * n
            for i in range(n):
                if j == 1:
                    f[i] = dis[0][i]
                elif j >= i + 1:
                    f[i] = 0
                else:
                    for cut_pos in range(j - 1, i + 1):
                        if f[i] is None or f[i] > g[cut_pos - 1] + dis[cut_pos][i]:
                            f[i] = g[cut_pos - 1] + dis[cut_pos][i]
            
            g = f[:]

        return f[-1]
```
