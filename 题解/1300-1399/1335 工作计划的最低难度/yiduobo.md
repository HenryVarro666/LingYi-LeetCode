---
title: "1335. 工作计划的最低难度"
aliases: ["yiduobo的每日leetcode 1335.工作计划的最低难度"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/monotonic-stack", "题单/动态规划", "题单/动态规划/五-划分型-DP", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/395616459"
zhihu_id: "395616459"
zhihu_title: "yiduobo的每日leetcode 1335.工作计划的最低难度"
question_id: "1335"
question: "工作计划的最低难度"
problem_url: "https://leetcode.cn/problems/minimum-difficulty-of-a-job-schedule/"
difficulty: "Hard"
rating: 2035
created: "2021-08-02T22:56:44+08:00"
updated: "2021-08-02T22:56:44+08:00"
upvotes: 1
comments: 0
---

# 1335. 工作计划的最低难度

> **[yiduobo的每日leetcode 1335.工作计划的最低难度](https://zhuanlan.zhihu.com/p/395616459) · 知乎 · 2021-08-02 · 赞同 1**
> 力扣：[1335. 工作计划的最低难度](https://leetcode.cn/problems/minimum-difficulty-of-a-job-schedule/) · Hard · 灵茶山艾府：[两种思路：动态规划/单调栈（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1335.工作计划的最低难度

[力扣](https://leetcode-cn.com/problems/minimum-difficulty-of-a-job-schedule/)

动态规划的题目，令f[i][j]表示前i天，完成前j个任务所需的最低难度。

首先，由于每天都必须完成至少一个工作，因此当j \< i时，f[i][j]都是不合法的。

接下来对于f[i][j]，我们至少应该选择第j个任务来执行，因此可以初始化

f[i][j] \= f[i - 1][j - 1] + jobDifficult[j]

接下来，我们可以从j - 1开始向前枚举，选择当天的工作，那么就有

f[i][j] \= min(f[i][j], f[i - 1][k - 1] + max(jobDifficult[k], ..., jobDifficult[j])

对于后面max的求解，我们可以通过倒序遍历来优化效率。

注意到每天的状态都至于前一天有关，因此可以优化掉i这一维。

另外，本题也可以利用单调性来进行优化。

具体来说，若f[i][k1]与f[i][k2]都合法，那么当k1 \< k2时，必然有f[i][k1] \<\= f[i][k2]

因此对于f[i][j]而言，若上一个大于jobDifficult[j]的位置为k，那么此时的f[i - 1][k + 1]到f[i - 1][j - 1]都大于等于f[i - 1][k]，同时无论从中间哪个位置开始，今天执行任务的难度都是jobDifficult[j]，因此我们只需要考虑f[i - 1][k]。同样的，对于jobDifficult[k]而言，我们也能找到上一个更大的位置，这样一来一个递减的单调栈来记录每一轮可能的候选位置。

我在这里偷懒，并没有进行这个优化。

最后附上python代码：

```python
class Solution(object):
    def minDifficulty(self, jobDifficulty, d):
        """
        :type jobDifficulty: List[int]
        :type d: int
        :rtype: int
        """

        n = len(jobDifficulty)
        if n < d:
            return -1

        g = [jobDifficulty[0]]
        for j in range(1, n):
            g.append(max(jobDifficulty[j], g[-1]))

        for i in range(1, d):
            f = [0] * i
            for j in range(i, n):
                f.append(g[j - 1] + jobDifficulty[j])
                ma = max(jobDifficulty[j], jobDifficulty[j - 1])
                for k in range(j - 2, i - 2, -1):
                    f[-1] = min(f[-1], g[k] + ma)
                    ma = max(ma, jobDifficulty[k])
            
            g = f[:]
        
        return g[-1]
```
