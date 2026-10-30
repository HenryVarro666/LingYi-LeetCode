---
title: "813. 最大平均值和的分组"
aliases: ["yiduobo的每日leetcode 813.最大平均值和的分组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/343820754"
zhihu_id: "343820754"
zhihu_title: "yiduobo的每日leetcode 813.最大平均值和的分组"
question_id: "813"
question: "最大平均值和的分组"
problem_url: "https://leetcode.cn/problems/largest-sum-of-averages/"
created: "2021-01-13T22:15:45+08:00"
updated: "2021-01-13T22:15:45+08:00"
upvotes: 1
comments: 0
---

# 813. 最大平均值和的分组

> **[yiduobo的每日leetcode 813.最大平均值和的分组](https://zhuanlan.zhihu.com/p/343820754) · 知乎 · 2021-01-13 · 赞同 1**
> 力扣：[813. 最大平均值和的分组](https://leetcode.cn/problems/largest-sum-of-averages/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

813.最大平均值和的分组

[力扣](https://leetcode-cn.com/problems/largest-sum-of-averages/)

动态规划的题目，令f[i][j]表示从第i个数开始到末尾，分为j组可以得到的最大平均值和。那么对于f[i][j]：

1、若此时的j为1，那么说明剩下的所有数都需要分到一个组内，那么就有

f[i][j] \= (a[i] + a[i + 1] + ... + a[n-1]) / (n - i)

2、若此时的j大于1，那么我们需要枚举当前这一组的末尾index，然后将i到index分为一组，那么此时就有

f[i][j] \= (a[i] + a[i + 1] + ... + a[index]) / (index - i + 1) + f[index + 1][j - 1]

对于上面平均值计算，可以利用前缀和来进行优化。

我在这里采用的是记忆化搜索的写法，对于边界条件的判断相对方便一点。

最后附上python代码：

```python
class Solution(object):
    def largestSumOfAverages(self, A, K):
        """
        :type A: List[int]
        :type K: int
        :rtype: float
        """

        n = len(A)
        s = [A[0]]
        for index in range(1, n):
            s.append(s[-1] + A[index])
        
        f = [[None] * K for _ in range(n)]
        return self.dfs(0, K - 1, A, n, s, f)
    
    def dfs(self, now, K, A, n, s, f):
        if f[now][K] is None:
            if K == 0:
                if now == 0:
                    f[now][K] = s[-1] * 1.0 / n
                else:
                    f[now][K] = (s[-1] - s[now - 1]) * 1.0 / (n - now)
            else:
                f[now][K] = 0
                for index in range(now, n - K):
                    if now == 0:
                        part_avg = s[index] * 1.0 / (index + 1)
                    else:
                        part_avg = (s[index] - s[now - 1]) * 1.0 / (index - now + 1)

                    f[now][K] = max(f[now][K], self.dfs(index + 1, K - 1, A, n, s, f) + part_avg)
        
        return f[now][K]
```
