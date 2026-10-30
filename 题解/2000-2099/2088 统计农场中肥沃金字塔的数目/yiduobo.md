---
title: "2088. 统计农场中肥沃金字塔的数目"
aliases: ["yiduobo的每日leetcode 2088.统计农场中肥沃金字塔的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "leetcode/dp", "leetcode/dp-2", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/518918302"
zhihu_id: "518918302"
zhihu_title: "yiduobo的每日leetcode 2088.统计农场中肥沃金字塔的数目"
question_id: "2088"
question: "统计农场中肥沃金字塔的数目"
problem_url: "https://leetcode.cn/problems/count-fertile-pyramids-in-a-land/"
difficulty: "Hard"
rating: 2105
created: "2022-05-24T00:48:12+08:00"
updated: "2022-05-24T00:48:12+08:00"
upvotes: 0
comments: 0
---

# 2088. 统计农场中肥沃金字塔的数目

> **[yiduobo的每日leetcode 2088.统计农场中肥沃金字塔的数目](https://zhuanlan.zhihu.com/p/518918302) · 知乎 · 2022-05-24 · 赞同 0**
> 力扣：[2088. 统计农场中肥沃金字塔的数目](https://leetcode.cn/problems/count-fertile-pyramids-in-a-land/) · Hard · 灵茶山艾府：[O(mn) 动态规划](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2088.统计农场中肥沃金字塔的数目

[力扣](https://leetcode.cn/problems/count-fertile-pyramids-in-a-land/)

经典动态规划问题的翻版，一般看到的都是统计正方形，在这里统计的则是金字塔。

由于题目中正反金字塔的构成是完全一致的，因此在这里可以将其视为等价的问题，只需要在动态规划最终计算时将枚举行的顺序反过来就好了。题目的金字塔是非常规整的，顶部必然是单个的格子，这也为后续的处理减低了不少难度。

在这里不妨考虑向上的金字塔。令f[i][j]表示顶部为(i, j)的向上的金字塔的最大高度，那么：

1、首先grid[i][j]这个格子就必须是肥沃的，要不然f[i][j]必然为0

2、接下来，需要想办法判断从i + 1开始的接下来的若干行是否是一个全部由肥沃土地构成的梯形。对于这个问题，直接判断并不方便，但是第i + 1行仅有三个格子需要判断，而通过这三个格子构造的金字塔恰好可以覆盖住整个梯形，即通过f[i + 1][j - 1], f[i + 1][j]以及f[i + 1][j + 1]来判断从第i + 1行开始向下完整的梯形最多有多高，那么就有f[i][j] \= min(f[i + 1][j - 1], f[i + 1][j], f[i + 1][j + 1]) + 1

需要注意的是，上面的计算方法会将高度等于0，也就是只有单个格子的情况也算作金字塔，因此在计算最终答案时需要去掉这种情况。

另外，在这里每一行的结果只与上一行或者下一行有关，因此可以使用滚动数组来优化空间。

最后附上python代码：

```python
class Solution(object):
    def countPyramids(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        res = 0
        
        f = grid[0][:]
        for i in range(1, m):
            g = f[:]
            f = []
            for j in range(n):
                if j == 0 or j == n - 1:
                    f.append(grid[i][j])
                elif grid[i][j] == 0:
                    f.append(0)
                else:
                    f.append(min(g[j - 1], g[j], g[j + 1]) + 1)

                if f[-1] > 0:
                    res += f[-1] - 1
        
        f = grid[m - 1][:]
        for i in range(m - 2, -1, -1):
            g = f[:]
            f = []
            for j in range(n):
                if j == 0 or j == n - 1:
                    f.append(grid[i][j])
                elif grid[i][j] == 0:
                    f.append(0)
                else:
                    f.append(min(g[j - 1], g[j], g[j + 1]) + 1)

                if f[-1] > 0:
                    res += f[-1] - 1
        
        return res
```
