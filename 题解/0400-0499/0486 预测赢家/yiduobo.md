---
title: "486. 预测赢家"
aliases: ["yiduobo的每日leetcode 486.预测赢家"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/game-theory", "题单/动态规划", "题单/数学算法", "题单/动态规划/十四-博弈-DP", "题单/数学算法/四-博弈论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/250949638"
zhihu_id: "250949638"
zhihu_title: "yiduobo的每日leetcode 486.预测赢家"
question_id: "486"
question: "预测赢家"
problem_url: "https://leetcode.cn/problems/predict-the-winner/"
difficulty: "Medium"
created: "2020-09-17T20:59:45+08:00"
updated: "2020-09-17T20:59:45+08:00"
upvotes: 0
comments: 0
---

# 486. 预测赢家

> **[yiduobo的每日leetcode 486.预测赢家](https://zhuanlan.zhihu.com/p/250949638) · 知乎 · 2020-09-17 · 赞同 0**
> 力扣：[486. 预测赢家](https://leetcode.cn/problems/predict-the-winner/) · Medium · 灵茶山艾府：[教你一步步思考 DP：记忆化搜索 -> 递推 -> 空间优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

486.预测赢家<https://leetcode-cn.com/problems/predict-the-winner/>

注意到题目要求每次只能从左侧或者右侧取数，那么就可以使用区间动态去解决。具体来说就是设f[i][j]表示先手玩家在i到j这一段采取最优策略时最多可以拿到多少分。对于f[i][j]，若先手玩家取了nums[i]，那么后手玩家之后能取到的最大得分就是f[i + 1][j]；而先手玩家如果去了nums[j]，那么后手玩家之后取到的最大得分就是f[i][j - 1]。由于nums[i]到nums[j]的和是恒定的，因此就可以得到

f[i][j] \= nums[i] + nums[i + 1] + ... + nums[j] - min(f[i + 1][j], f[i][j - 1])

对于前面的nums这一串，可以使用前缀和来进行优化，于是最后就是

f[i][j] \= sum[j + 1] - sum[i] - min(f[i + 1][j], f[i][j - 1])

计算出最终的f[0][n - 1]之后，若这个值大于等于sum[-1]的一半，那么就是先手必胜，否则就是后手必胜。

最后附上python代码：

```python
class Solution(object):
    def PredictTheWinner(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        if len(nums) <= 2:
            return True

        sum_list = [nums[0]]
        for num in nums[1:]:
            sum_list.append(sum_list[-1] + num)

        f = [[None] * len(nums) for _ in range(len(nums))]

        return self.dfs(0, len(nums) - 1, nums, f, sum_list) * 2 >= sum_list[-1]

    def dfs(self, l, r, nums, f, sum_list):
        if f[l][r] is not None:
            return f[l][r]

        if r - l + 1 <= 2:
            f[l][r] = max(nums[l], nums[r])
            return f[l][r]

        if l == 0:
            s = sum_list[r]
        else:
            s = sum_list[r] - sum_list[l - 1]

        f[l][r] = s - min(self.dfs(l + 1, r, nums, f, sum_list), self.dfs(l, r - 1, nums, f, sum_list))
        return f[l][r]
```
