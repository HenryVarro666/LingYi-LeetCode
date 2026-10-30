---
title: "1937. 扣分后的最大得分"
aliases: ["yiduobo的每日leetcode 1937.扣分后的最大得分"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/dp", "leetcode/dp-2", "题单/动态规划", "题单/动态规划/二-网格图-DP", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/488458245"
zhihu_id: "488458245"
zhihu_title: "yiduobo的每日leetcode 1937.扣分后的最大得分"
question_id: "1937"
question: "扣分后的最大得分"
problem_url: "https://leetcode.cn/problems/maximum-number-of-points-with-cost/"
difficulty: "Medium"
rating: 2106
created: "2022-03-27T17:03:43+08:00"
updated: "2022-03-27T17:03:43+08:00"
upvotes: 0
comments: 0
---

# 1937. 扣分后的最大得分

> **[yiduobo的每日leetcode 1937.扣分后的最大得分](https://zhuanlan.zhihu.com/p/488458245) · 知乎 · 2022-03-27 · 赞同 0**
> 力扣：[1937. 扣分后的最大得分](https://leetcode.cn/problems/maximum-number-of-points-with-cost/) · Medium · 灵茶山艾府：[DP 优化技巧：拆项+前后缀最大值](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1937.扣分后的最大得分

[力扣](https://leetcode-cn.com/problems/maximum-number-of-points-with-cost/)

经典的动态规划问题。令f[i][j]表示前i行，最后一行选择了第j列这个格子时所能得到的最大分数，那么对于f[i][j]，其上一行可能选择任何一个位置，那么就有

f[i][j] \= max(f[i - 1][0] - j, ... ,f[i - 1][j - 1] - 1, f[i - 1][j], f[i - 1][j + 1] - 1, ... , f[i - 1][n -1] - (n - 1 - j)) + points[i][j]

常规来看，这里O(mn)的状态表示，状态转移的复杂度为O(n)，所以最终时间复杂度为O(m \* n^2)，还有优化的余地。对于上面这个状态转移的式子，不妨拆成两个部分来看。

首先是小于等于j的部分，有

f[i][j] \= max(f[i - 1][0] - j, f[i - 1][j - 1] - (j - 1), ..., f[i - 1][j]) + points[i][j]

方便起见，记max(f[i - 1][0] - j, f[i - 1][j - 1] - (j - 1), ... , f[i - 1][j])为left_max[i][j]，即

f[i][j] \= left_max[i][j] + points[i][j]

那么对于f[i][j - 1]，同样有

f[i][j - 1] \= left_max[i][j - 1] + points[i][j]

在这里考察left_max[i][j]与left_max[i][j - 1]的关系：

left_max[i][j] \= max(f[i - 1][0] - j, f[i - 1][j - 1] - (j - 1), ... , f[i - 1][j - 1] - 1, f[i - 1][j])

left_max[i][j - 1] \= max(f[i - 1][0] - (j - 1), f[i - 1][j -1] - (j - 2), ..., f[i - 1][j - 1])

可以发现，在left_max[i][j]中，除了最后一项f[i - 1][j]之外，其他的项都恰好等于left_max[i][j - 1]中的项再减去1，于是就有left_max[i][j] \= max(left_max[i][j - 1] - 1, f[i - 1][j])

这样一来，就可以正序一趟遍历，在均摊O(1)的时间复杂度内求出所有的left_max了。

接下来是大于等于j的部分，有

f[i][j] \= max(f[i - 1][n - 1] - (n - 1 - j), f[i - 1][n - 2] - (n - 2 - j), ..., f[i - 1][j + 1] - 1, f[i - 1][j])

类似的，对于max的部分也可以设置一个right_max，同样是考察right_max[i][j]与right_max[i][j + 1]的关系：

right_max[i][j] \= max(f[i - 1][n - 1] - (n - 1 - j), f[i - 1][n - 2] - (n - 2 - j), ..., f[i - 1][j +1] - 1, f[i - 1][j])

right_max[i][j + 1] \= max(f[i - 1][n - 1] - (n - 1 - (j + 1)), f[i - 1][n - 2] - (n - 2 - (j + 1)), ... , f[i - 1][j + 1])

可以发现，在right_max[i][j]中，除了最后一项f[i - 1][j]之外，其他的项都恰好等于right_max[i][j + 1]中的项再减去1，于是就有right_max[i][j] \= max(right_max[i][j + 1] - 1, f[i - 1][j])

同样的，在这里就可以逆序一趟遍历，在均摊O(1)的时间复杂度内求出所有的right_max了。

有了left_max和right_max之后，f[i][j]就可以通过max(left_max[i][j], right_max[i][j]) + points[i][j]计算得到，从而在均摊O(1)的时间复杂度内完成了第i层的状态转移。

另外，由于这里的状态转移只依赖当前这一层和上一层，因此可以省去i这一维，使用两个数组来滚动迭代。

最后附上python代码：

```python
class Solution(object):
    def maxPoints(self, points):
        """
        :type points: List[List[int]]
        :rtype: int
        """

        m = len(points)
        n = len(points[0])

        f = points[0][:]
        for i in range(1, m):
            g = []

            now = f[0]
            g.append(now)
            for j in range(1, n):
                now = max(now - 1, f[j])
                g.append(now)
            
            now = f[-1]
            g[-1] = max(g[-1], now)
            for j in range(n - 2, -1, -1):
                now = max(now - 1, f[j])
                g[j] = max(g[j], now)
            
            for j in range(n):
                g[j] += points[i][j]
            
            f = g[:]
        
        return max(f)
```
