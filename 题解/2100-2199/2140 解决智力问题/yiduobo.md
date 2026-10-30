---
title: "2140. 解决智力问题"
aliases: ["yiduobo的每日leetcode 2140.解决智力问题"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/一-入门-DP", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/528882414"
zhihu_id: "528882414"
zhihu_title: "yiduobo的每日leetcode 2140.解决智力问题"
question_id: "2140"
question: "解决智力问题"
problem_url: "https://leetcode.cn/problems/solving-questions-with-brainpower/"
difficulty: "Medium"
rating: 1709
created: "2022-06-14T23:08:08+08:00"
updated: "2022-06-14T23:08:08+08:00"
upvotes: 0
comments: 0
---

# 2140. 解决智力问题

> **[yiduobo的每日leetcode 2140.解决智力问题](https://zhuanlan.zhihu.com/p/528882414) · 知乎 · 2022-06-14 · 赞同 0**
> 力扣：[2140. 解决智力问题](https://leetcode.cn/problems/solving-questions-with-brainpower/) · Medium · 灵茶山艾府：[打家劫舍变形题，查表法 / 刷表法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2140.解决智力问题

[力扣](https://leetcode.cn/problems/solving-questions-with-brainpower/)

动态规划的题目。与常规的动态规划不同，由于题目的要求是解决了某个问题后之后不能再解决后续的若干问题，因此本题的状态表示应该是f[i]表示处理从第i题到第n - 1题的最大收益，那么对于f[i]：

1、首先是边界情况。当i \= n - 1时，显然有f[i] \= questions[n - 1][0]

2、接下来对于i \< n - 1，那么有两种选择：

2-1）跳过第i题，那么就有f[i] \= f[i + 1]

2-2）解决第i题，那么不能解决后续的从i + 1到i + questions[i][1]的这些题，因此就有

f[i] \= f[i + questions[i] + 1] + questions[i][0]

当然，如果这里i + questions[i] + 1 >\= n，说明解决了第i题后之后所有的题都不能再解决了，因此此时应该是

f[i] \= questions[i][0]

接下来只需从后向前一趟遍历，计算每个f[i]，最终答案就是f[0]。

最后附上python代码：

```python
class Solution(object):
    def mostPoints(self, questions):
        """
        :type questions: List[List[int]]
        :rtype: int
        """

        n = len(questions)
        f = [0] * n
        f[-1] = questions[-1][0]
        for index in range(n - 2, -1, -1):
            f[index] = f[index + 1]
            if index + questions[index][1] + 1 < n:
                f[index] = max(f[index], f[index + questions[index][1] + 1] + questions[index][0])
            else:
                f[index] = max(f[index], questions[index][0])

        return f[0]
```
