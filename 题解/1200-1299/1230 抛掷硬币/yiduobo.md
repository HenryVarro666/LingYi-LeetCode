---
title: "1230. 抛掷硬币"
aliases: ["yiduobo的每日leetcode 1230.抛掷硬币"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/613725538"
zhihu_id: "613725538"
zhihu_title: "yiduobo的每日leetcode 1230.抛掷硬币"
question_id: "1230"
question: "抛掷硬币"
problem_url: "https://leetcode.cn/problems/toss-strange-coins/"
created: "2023-03-13T22:09:14+08:00"
updated: "2023-03-13T22:09:14+08:00"
upvotes: 0
comments: 0
---

# 1230. 抛掷硬币

> **[yiduobo的每日leetcode 1230.抛掷硬币](https://zhuanlan.zhihu.com/p/613725538) · 知乎 · 2023-03-13 · 赞同 0**
> 力扣：[1230. 抛掷硬币](https://leetcode.cn/problems/toss-strange-coins/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1230.抛掷硬币

[力扣](https://leetcode.cn/problems/toss-strange-coins/)

经典的动态规划问题。

令f[i][j]表示抛i次硬币，有j次正面向上的概率。首先初始化f[0][0] \= 1，接下来对于f[i][j]：

1、若j \= 0：

最后这次必然是背面向上，因此就有f[i][j] \= f[i - 1][j] \* (1 - prob[i - 1])

2、若j > 0：

最后这次有prob[i - 1]的概率正面朝上，有(1 - prob[i - 1])的概率背面向上，因此就有

f[i][j] \= f[i - 1][j - 1] \* prob[i - 1] + f[i - 1][j] \* (1 - prob[i - 1])

计算完成后，f[n][target]即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def probabilityOfHeads(self, prob, target):
        """
        :type prob: List[float]
        :type target: int
        :rtype: float
        """

        n = len(prob)
        f = [[0.0] * (n + 1) for _ in range(n + 1)]
        f[0][0] = 1.0
        for i in range(1, n + 1):
            for j in range(0, i + 1):
                if j == 0:
                    f[i][j] = f[i - 1][j] * (1 - prob[i - 1])
                else:
                    f[i][j] = f[i - 1][j - 1] * prob[i - 1] + f[i - 1][j] * (1 - prob[i - 1])
        
        return f[n][target]
```
