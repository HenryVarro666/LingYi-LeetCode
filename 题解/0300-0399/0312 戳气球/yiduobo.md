---
title: "312. 戳气球"
aliases: ["yiduobo的每日leetcode 312.戳气球"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/158773400"
zhihu_id: "158773400"
zhihu_title: "yiduobo的每日leetcode 312.戳气球"
question_id: "312"
question: "戳气球"
problem_url: "https://leetcode.cn/problems/burst-balloons/"
created: "2020-07-11T19:16:57+08:00"
updated: "2020-07-11T19:16:57+08:00"
upvotes: 0
comments: 0
---

# 312. 戳气球

> **[yiduobo的每日leetcode 312.戳气球](https://zhuanlan.zhihu.com/p/158773400) · 知乎 · 2020-07-11 · 赞同 0**
> 力扣：[312. 戳气球](https://leetcode.cn/problems/burst-balloons/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

312.戳气球<https://leetcode-cn.com/problems/burst-balloons/>

经典的动态规划题目，有一道类似的题目叫做石子归并，是当时入门动态规划做过的。

这种区间类的动态规划，一般就是f[i][j]表示从i开始到j怎么怎么样，这里表示的则是从i到j这一段戳剩下i和j之后最大的硬币数，那么直接枚举分割点cut_pos，优先将从i到cut_pos这一段戳剩下i、cut_pos以及cut_pos到j这一段戳剩下j、cut_pos，最后戳cut_pos，于是就有

f[i][j] \= max(f[i][cut_pos] + f[cut_pos][j] + nums[i] \* nums[j] \* nums[cut_pos]

根据题目的提示，在两侧加上两个1之后恰好能完美适配上面的状态转移方程。

另外，当i \= j或i \= j - 1时，f[i][j]都为0。

我在这里使用的是记忆化搜索实现，相对好写一些。

正常来说，这类动态规划的时间复杂度一般在O(n^3)，但是如果状态转移方程满足四边形不等式，那么通过记录之前状态的最优决策点可以反过来指导之后枚举cut_pos的范围，从而将时间复杂度降到O(n^2)。我简单算了一下，似乎这里是不满足四边形不等式的，于是无法进一步优化了。

最后附上python代码：

```python
class Solution(object):
    def maxCoins(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        nums = [1] + nums + [1]
        f = [[None] * len(nums) for _ in range(len(nums))]

        return self.dfs(0, len(nums) - 1, f, nums)

    def dfs(self, left, right, f, nums):
        if f[left][right] is not None:
            return f[left][right]

        if left >= right - 1:
            f[left][right] = 0
            return f[left][right]

        f[left][right] = 0
        for cut_pos in range(left + 1, right):
            f[left][right] = max(f[left][right], self.dfs(left, cut_pos, f, nums) + self.dfs(cut_pos, right, f, nums) + nums[left] * nums[right] * nums[cut_pos])

        return f[left][right]
```
