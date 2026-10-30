---
title: "1444. 切披萨的方案数"
aliases: ["yiduobo的每日leetcode 1444.切披萨的方案数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/prefix-sum", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/410806185"
zhihu_id: "410806185"
zhihu_title: "yiduobo的每日leetcode 1444.切披萨的方案数"
question_id: "1444"
question: "切披萨的方案数"
problem_url: "https://leetcode.cn/problems/number-of-ways-of-cutting-a-pizza/"
difficulty: "Hard"
rating: 2127
created: "2021-09-15T23:45:22+08:00"
updated: "2021-09-15T23:45:22+08:00"
upvotes: 0
comments: 0
---

# 1444. 切披萨的方案数

> **[yiduobo的每日leetcode 1444.切披萨的方案数](https://zhuanlan.zhihu.com/p/410806185) · 知乎 · 2021-09-15 · 赞同 0**
> 力扣：[1444. 切披萨的方案数](https://leetcode.cn/problems/number-of-ways-of-cutting-a-pizza/) · Hard · 灵茶山艾府：[击败 100%！从递归到递推到优化，教你一步步思考动态规划！（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1444.切披萨的方案数

[力扣](https://leetcode-cn.com/problems/number-of-ways-of-cutting-a-pizza/)

由于每次切割只能横切或者纵切，同时每次都会留下下面或者右边的部分，那么很自然想到使用动态规划，令f[c][i][j]表示对于以(i, j)为左上角，(m - 1, n - 1)为右下角的披萨切c刀的方案数，那么对于f[c][i][j]：

1、当c\=0时，表示不需要进行切割，那么此时只需要检测此时的披萨上是否有苹果，若有那么f[c][i][j] \= 1，否则f[c][i][j] \= 0

2、当c>0时，我们则需要对披萨进行切割。首先将f[c][i][j]初始化为0，接下来：

2-1）考虑横切，将靠上的第i到第h行切割出去，这里h的取值范围为(i, m - 2)，那么若切割出去的披萨上有苹果，那么就有

f[c][i][j] +\= f[c - 1][h + 1][j]

即这次切割出去之后，剩下的c - 1刀需要切割以(h +1, j)为左上角的披萨，即f[c - 1][h + 1][j]

2-2）在考虑横切，将靠左的第j列到第v列切割出去，这里v的取值范围为(j, n - 2)，那么若切割出去的披萨上有苹果，那么就有

f[c][i][j] +\= f[c - 1][i][v + 1]

即这次切割出去之后，剩下的c - 1刀需要切割以(i, v + 1)为左上角的披萨，即f[c - 1][i][v + 1]

剩下的问题就是如何判断一块披萨上是否有苹果。由于这里的苹果是静态的，那么使用二维前缀和就能解决这个问题。换言之，对于以(x1, y1)为左上角，(x2, y2)为右下角的披萨而言，上面的苹果数目就是

s[x2][y2] - s[x2][y1 - 1] - s[x1 - 1][y2] + s[x1 - 1][y1 - 1]

这里的s[x][y]表示以(0, 0)为左上角，(x, y)为右下角的披萨上的苹果的数目。

而对于这个s[x][y]，先设pizza[x][y]为苹果时p[x][y]为1，否则为0，那么就有

s[x][y] \= s[x - 1][y] + s[x][y - 1] - s[x - 1][y - 1] + p[x][y]

于是可以先预处理出所有的s[x][y]，然后执行动态规划，最终f[k - 1][0][0]即为最终答案。另外，注意到这里状态转移每一步只跟上一步有关，因此还可以使用滚动数组来优化空间。

最后附上python代码：

```python
class Solution(object):
    def ways(self, pizza, k):
        """
        :type pizza: List[str]
        :type k: int
        :rtype: int
        """

        m = len(pizza)
        n = len(pizza[0])

        prefix_s = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if pizza[i][j] == 'A':
                    delta = 1
                else:
                    delta = 0

                if i == 0:
                    if j == 0:
                        prefix_s[i][j] = delta
                    else:
                        prefix_s[i][j] = prefix_s[i][j - 1] + delta
                elif j == 0:
                    prefix_s[i][j] = prefix_s[i - 1][j] + delta
                else:
                    prefix_s[i][j] = prefix_s[i - 1][j] + prefix_s[i][j - 1] - prefix_s[i - 1][j - 1] + delta
        
        mod = 10 ** 9 + 7
        for c in range(k):
            f = [[0] * n for _ in range(m)]
            for i in range(m - 1, -1, -1):
                for j in range(n - 1, -1, -1):
                    if c == 0:
                        if self.check(i, j, m - 1, n - 1, prefix_s):
                            f[i][j] = 1
                        else:
                            f[i][j] = 0
                    else:
                        for h in range(i, m - 1):
                            if self.check(i, j, h, n - 1, prefix_s):
                                f[i][j] += g[h + 1][j]
                                f[i][j] %= mod

                        for v in range(j, n - 1):
                            if self.check(i, j, m - 1, v, prefix_s):
                                f[i][j] += g[i][v + 1]
                                f[i][j] %= mod
                
            g = f[:]

        return f[0][0]

    def check(self, x1, y1, x2, y2, prefix_s):
        if x1 == 0:
            if y1 == 0:
                s = prefix_s[x2][y2] > 0
            else:
                s = prefix_s[x2][y2] - prefix_s[x2][y1 - 1]
        elif y1 == 0:
            s = prefix_s[x2][y2] - prefix_s[x1 - 1][y2]
        else:
            s = prefix_s[x2][y2] - prefix_s[x1 - 1][y2] - prefix_s[x2][y1 - 1] + prefix_s[x1 - 1][y1 - 1]
        
        return s > 0
```
