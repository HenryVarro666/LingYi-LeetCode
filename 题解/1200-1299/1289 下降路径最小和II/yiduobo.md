---
title: "1289. 下降路径最小和II"
aliases: ["yiduobo的每日leetcode 1289.下降路径最小和II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/389428071"
zhihu_id: "389428071"
zhihu_title: "yiduobo的每日leetcode 1289.下降路径最小和II"
question_id: "1289"
question: "下降路径最小和II"
problem_url: "https://leetcode.cn/problems/minimum-falling-path-sum-ii/"
created: "2021-07-13T22:51:33+08:00"
updated: "2021-07-13T22:51:33+08:00"
upvotes: 1
comments: 0
---

# 1289. 下降路径最小和II

> **[yiduobo的每日leetcode 1289.下降路径最小和II](https://zhuanlan.zhihu.com/p/389428071) · 知乎 · 2021-07-13 · 赞同 1**
> 力扣：[1289. 下降路径最小和II](https://leetcode.cn/problems/minimum-falling-path-sum-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1289.下降路径最小和II

[力扣](https://leetcode-cn.com/problems/minimum-falling-path-sum-ii/)

经典的动态规划问题，令f[i][j]表示前i行，终点为第j列时的最优解，那么对于f[i][j]，显然应该从上一层最小的位置转移过来。不过注意到题目还有相邻数字不能在同一列这个条件，那么若上一层最小的位置就是j，此时就应当从上一层次小的位置转移过来。

换言之，我们只需要在计算完一层之后保留住当前层最小的两个值以及对应的位置，那么在下一层的迭代时就可以利用这两个值快速迭代了。

另外，注意到每一层的值都只与上一层有关，那么可以使用滚动数组来优化空间。

最后附上python代码：

```python
class Solution(object):
    def minFallingPathSum(self, arr):
        """
        :type arr: List[List[int]]
        :rtype: int
        """

        n = len(arr)
        f = arr[0][:]

        for i in range(1, n):
            m1 = m2 = None
            p = None
            for j, num in enumerate(f):
                if m1 is None:
                    m1 = num
                    p = j
                elif m1 > num:
                    m2 = m1
                    m1 = num
                    p = j
                elif m2 is None or m2 > num:
                    m2 = num

            g = arr[i][:]
            for j in range(n):
                if j != p:
                    g[j] += m1
                else:
                    g[j] += m2
            
            f = g[:]

        return min(f)
```
