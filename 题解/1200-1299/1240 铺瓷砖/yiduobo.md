---
title: "1240. 铺瓷砖"
aliases: ["yiduobo的每日leetcode 1240.铺瓷砖"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/384989981"
zhihu_id: "384989981"
zhihu_title: "yiduobo的每日leetcode 1240.铺瓷砖"
question_id: "1240"
question: "铺瓷砖"
problem_url: "https://leetcode.cn/problems/tiling-a-rectangle-with-the-fewest-squares/"
created: "2021-06-29T12:23:50+08:00"
updated: "2021-06-29T12:23:50+08:00"
upvotes: 0
comments: 0
---

# 1240. 铺瓷砖

> **[yiduobo的每日leetcode 1240.铺瓷砖](https://zhuanlan.zhihu.com/p/384989981) · 知乎 · 2021-06-29 · 赞同 0**
> 力扣：[1240. 铺瓷砖](https://leetcode.cn/problems/tiling-a-rectangle-with-the-fewest-squares/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1240.铺瓷砖

[力扣](https://leetcode-cn.com/problems/tiling-a-rectangle-with-the-fewest-squares/)

没有想出什么很好的做法，简单看上去应该可以将所有情况归类到样例3中的情况，分别为左上角的8 \* 4的矩形，右上角的5 \* 5的矩形，右下角的6 \* 6的矩形，左下角的7 \* 7的矩形，以及中间的1 \* 1的小矩形，也就是说通过周围的4个矩形以及中间的小矩形来拼凑。

于是一个自然的想法是使用动态规划，令f[i][j]表示长为i，宽为j的矩形最少需要多少瓷砖来拼成，那么对于f[i][j]，我们需要枚举这几个矩形的场合宽，然后递归计算。

另外，f[i][j]显然是与f[j][i]相等的，因此我们当i > j时，我们可以交换i和j，默认i \<\= j。还有一点就是，当j是i的倍数时，设j / i \= k，那么此时的最优解显然是使用k个i \* i的瓷砖来填充。

最后附上python代码：

```python
class Solution(object):
    def tilingRectangle(self, n, m):
        """
        :type n: int
        :type m: int
        :rtype: int
        """

        if n > m:
            n, m = m, n

        f = [[None] * (m + 1) for _ in range(n + 1)]

        return  self.dfs(n, m, f)

    def dfs(self, n, m, f):
        if n > m:
            n, m = m, n
        if f[n][m] is None:
            if m == 0:
                f[n][m] = 0
            elif n % m == 0:
                f[n][m] = n / m
            else:
                f[n][m] = n * m
                for i in range(1, n + 1):
                    for j in range(1, m + 1):
                        for k in range(i, n + 1):
                            for l in range(m - j, m + 1):
                                p1 = self.dfs(i, j, f)
                                p2 = self.dfs(k, m - j, f)
                                p3 = self.dfs(n - k, l, f)
                                p4 = self.dfs(n - i, m - l, f)
                                p5 = self.dfs(k - i, l - (m - j), f)
                                f[n][m] = min(f[n][m], p1 + p2 + p3 + p4 + p5)
        return f[n][m]
```
