---
title: "LCP 57. 打地鼠"
aliases: ["yiduobo的每日leetcode LCP57.打地鼠"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/578611310"
zhihu_id: "578611310"
zhihu_title: "yiduobo的每日leetcode LCP57.打地鼠"
question_id: "LCP 57"
question: "打地鼠"
created: "2022-10-29T23:46:15+08:00"
updated: "2022-10-29T23:46:15+08:00"
upvotes: 0
comments: 0
---

# LCP 57. 打地鼠

> **[yiduobo的每日leetcode LCP57.打地鼠](https://zhuanlan.zhihu.com/p/578611310) · 知乎 · 2022-10-29 · 赞同 0**
> 力扣：LCP 57. 打地鼠

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP57.打地鼠

[力扣](https://leetcode.cn/problems/ZbAuEH/)

常规的动态规划算法是比较容易想到的。将地鼠按出现时间从小到大排序，然后令f[i]表示如果一定要敲打moles[i]表示的地鼠，那么在第0到第i只地鼠中最多可以打到多少只地鼠。

对于f[i]，设moles[i]在时间t出没于位置(x, y)，那么：

1、如果在此之前一只地鼠都没打过，那么只需当前的位置(x, y)距离锤子的初始位置(1, 1)的曼哈顿距离小于等于当前的时间t，那么就一定可以打到当前这只地鼠，即abs(x - 1) + abs(y - 1) \<\= t时，初始化f[i] \= 1，否则f[i] \= 0

2、当然，在打moles[i]之前也可能打过其他的地鼠，那么就可以枚举上一只被打的地鼠j，设其在时间t'出没于位置(x', y')，只需abs(x - x') + abs(y - y') \<\= t - t'，就可以在打完moles[j]之后将锤子移动到(x, y)然后打moles[i]，于是就有f[i] \= max(f[i], f[j] + 1)

上面算法的时间复杂度为O(n^2)，对于本题的数据规模显然是太大了，需要想办法进行优化。注意到本题中的地图大小仅为3 \* 3，换言之，在4秒内锤子一定可以从地图中的任意位置移动到另一个位置。那么对于上面状态转移方程中的情况2而言，其中所有出没时间t' \<\= t - 4的地鼠j是无需判断锤子是否来得及移动的，也就是说只需要保留其中f[j]最大的那个地鼠。

具体实现上，可以使用一个变量p表示最小的满足t' > t - 4的j，同时使用一个变量ma表示f[0]到f[p - 1]中的最大值。当i向后移动的，p也随着向后移动，同时随着p的移动更新ma，这个过程的时间复杂度是均摊O(1)的。得到ma之后，就可以利用ma + 1来更新f[i]了。除此之外，剩下的t' > t - 4的地鼠最多只有4 \* 3 \* 3 \= 36只，那么在这里可以依旧采取枚举的做法，枚举p到i - 1之间的所有j，并利用f[j] + 1来更新f[i]。

这样一来，最终的时间复杂度就从O(n^2)降到了O(n)。

值得一提的是，由于每一时刻只可能打到一只地鼠，因此如果先将地鼠按照时间聚合起来的话，那么最终状态转移的枚举数量就可以从36降低到3，也是非常大的一个优化。我在这里偷懒，就没有加上这个优化了。

最后附上python代码：

```python
class Solution(object):
    def getMaximumNumber(self, moles):
        """
        :type moles: List[List[int]]
        :rtype: int
        """

        n = len(moles)
        moles.sort(key=lambda d:d[0])
        f = [0] * n
        p = 0
        ma = 0
        for i in range(n):
            t, x, y = moles[i]
            while t - moles[p][0] >= 4:
                ma = max(ma, f[p])
                p += 1
                
            if p > 0:
                f[i] = ma + 1
            elif abs(x - 1) + abs(y - 1) <= t:
                f[i] = 1

            for j in range(i - 1, p - 1, -1):
                if f[j] > 0 and abs(x - moles[j][1]) + abs(y - moles[j][2]) <= t - moles[j][0]:
                    f[i] = max(f[i], f[j] + 1)

        return max(f)
```
