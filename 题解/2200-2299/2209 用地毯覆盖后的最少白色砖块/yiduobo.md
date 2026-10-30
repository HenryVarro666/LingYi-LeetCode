---
title: "2209. 用地毯覆盖后的最少白色砖块"
aliases: ["yiduobo的每日leetcode 2209.用地毯覆盖后的最少白色砖块"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/prefix-sum", "题单/动态规划", "题单/动态规划/五-划分型-DP", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/539921217"
zhihu_id: "539921217"
zhihu_title: "yiduobo的每日leetcode 2209.用地毯覆盖后的最少白色砖块"
question_id: "2209"
question: "用地毯覆盖后的最少白色砖块"
problem_url: "https://leetcode.cn/problems/minimum-white-tiles-after-covering-with-carpets/"
difficulty: "Hard"
rating: 2106
created: "2022-07-10T19:36:10+08:00"
updated: "2022-07-10T19:36:10+08:00"
upvotes: 3
comments: 1
---

# 2209. 用地毯覆盖后的最少白色砖块

> **[yiduobo的每日leetcode 2209.用地毯覆盖后的最少白色砖块](https://zhuanlan.zhihu.com/p/539921217) · 知乎 · 2022-07-10 · 赞同 3**
> 力扣：[2209. 用地毯覆盖后的最少白色砖块](https://leetcode.cn/problems/minimum-white-tiles-after-covering-with-carpets/) · Hard · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推到空间优化！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2209.用地毯覆盖后的最少白色砖块

[力扣](https://leetcode.cn/problems/minimum-white-tiles-after-covering-with-carpets/)

非常标准的动态规划题，令f[i][j]表示用前i块地毯来覆盖第0到第j块砖，覆盖不到的白色砖块的数量。

首先考虑特殊情况。当numCarpets \* carpetLen >\= len(floor)时，说明可以实行全覆盖，此时答案必然是0。

接下来是一般情况。

首先考虑边界。当i \= 0，即不使用任何地毯时，f[i] \= sum(floor[:i])，即f[i]是floor从0到i的一个前缀和。

接下来是i > 0的情况。对于f[i][j]：

1、当j \< carpetLen时，显然有f[i][j] \= 0

2、当j >\= carpetLen时，有两种策略。如果不适用当前这块地毯，就有f[i][j] \= f[i][j - 1] + floor[j]。如果使用，那么就有f[i][j] \= f[i - 1][j - carpetLen]。总和起来，就有

f[i][j] \= min(f[i][j - 1] + floor[j], f[i - 1][j - carpetLen]

动态规划完成后，f[-1][-1]就是最终答案。

另外，注意到这里的f每一轮的状态只与上一轮有关，因此可以使用滚动数组省去i这一维。

最后附上python代码：

```python
class Solution(object):
    def minimumWhiteTiles(self, floor, numCarpets, carpetLen):
        """
        :type floor: str
        :type numCarpets: int
        :type carpetLen: int
        :rtype: int
        """

        n = len(floor)
        if numCarpets * carpetLen >= n:
            return 0
        
        f = [int(floor[0])]
        for index in range(1, n):
            f.append(f[-1] + int(floor[index]))
        
        for i in range(numCarpets):
            g = f[:]
            f = []
            for j in range(n):
                if j < carpetLen:
                    f.append(0)
                else:
                    f.append(min(f[j - 1] + int(floor[j]), g[j - carpetLen]))
        
        return f[-1]
```
