---
title: "568. 最大休假天数"
aliases: ["yiduobo的每日leetcode 568.最大休假天数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/601315281"
zhihu_id: "601315281"
zhihu_title: "yiduobo的每日leetcode 568.最大休假天数"
question_id: "568"
question: "最大休假天数"
problem_url: "https://leetcode.cn/problems/maximum-vacation-days/"
created: "2023-01-28T02:11:55+08:00"
updated: "2023-01-28T02:11:55+08:00"
upvotes: 0
comments: 1
---

# 568. 最大休假天数

> **[yiduobo的每日leetcode 568.最大休假天数](https://zhuanlan.zhihu.com/p/601315281) · 知乎 · 2023-01-28 · 赞同 0**
> 力扣：[568. 最大休假天数](https://leetcode.cn/problems/maximum-vacation-days/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

568.最大休假天数

[力扣](https://leetcode.cn/problems/maximum-vacation-days/)

经典的动态规划问题。令f[i][j]表示第i天在城市j时可以获得的最大休假天数，那么对于f[i][j]：

1、待在原地不动，那么就有f[i][j] \= f[i - 1][j] + days[i][j]

2、从别的城市过来，那么就有f[i][j] \= max(f[i][j], f[i - 1][k] + days[i][j])，其中flights[k][j] \= 1，表示可以从城市k来到城市j，同时f[i - 1][k]不为空，表示有办法在第i - 1天来到城市k

方便起见，在这里可以将flighs[i][i]也置为1，这样一来就可以将情况1也归入情况2了。

另外，对于由于f每一轮都只与上一轮有关，因此可以省略掉i这一维来节省空间。

最后附上python代码：

```python
class Solution(object):
    def maxVacationDays(self, flights, days):
        """
        :type flights: List[List[int]]
        :type days: List[List[int]]
        :rtype: int
        """

        n = len(flights)
        for index in range(n):
            flights[index][index] = 1
        
        f = [None] * n
        f[0] = 0

        for i in range(len(days[0])):
            g = f[:]
            f = [None] * n
            for j in range(n):
                for k in range(n):
                    if flights[k][j] == 1 and g[k] is not None and (f[j] is None or f[j] < g[k] + days[j][i]):
                        f[j] = g[k] + days[j][i]

        return max(f)
```
