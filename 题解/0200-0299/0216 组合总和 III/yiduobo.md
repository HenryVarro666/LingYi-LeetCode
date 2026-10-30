---
title: "216. 组合总和 III"
aliases: ["yiduobo的每日leetcode 216.组合总和 III"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/math", "leetcode/backtracking", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/四-回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/148154039"
zhihu_id: "148154039"
zhihu_title: "yiduobo的每日leetcode 216.组合总和 III"
question_id: "216"
question: "组合总和 III"
problem_url: "https://leetcode.cn/problems/combination-sum-iii/"
difficulty: "Medium"
created: "2020-06-13T23:48:19+08:00"
updated: "2020-06-13T23:48:19+08:00"
upvotes: 0
comments: 0
---

# 216. 组合总和 III

> **[yiduobo的每日leetcode 216.组合总和 III](https://zhuanlan.zhihu.com/p/148154039) · 知乎 · 2020-06-13 · 赞同 0**
> 力扣：[216. 组合总和 III](https://leetcode.cn/problems/combination-sum-iii/) · Medium · 灵茶山艾府：[【视频讲解】回溯+剪枝优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

216.组合总和III <https://leetcode-cn.com/problems/combination-sum-iii/>

这个问题应该能用动态规划来做，不过最后要求输出所有的解，可能会稍微麻烦一点，总的来说还是f[i][j][k]表示和为i，取了j次，最大取到k的所有解。j次这一维可以滚动优化掉，不过此时i就需要从大到小来进行迭代了。

我在这里选择了比较简单的搜索回溯法，每次枚举当前选取数中最后一个数now[-1] + 1至9，选择之后加入now然后继续搜索，直到sum(now) \= n且len(now) \= k，或者剩下的数满足不了答案。

最后附上python代码：

```python
class Solution(object):
    def combinationSum3(self, k, n):
        """
        :type k: int
        :type n: int
        :rtype: List[List[int]]
        """

        res = []
        self.dfs(n, k, [0], res)

        return res

    def dfs(self, n, k, now, res):
        if n == 0:
            if k == 0:
                res.append(now[1:])
            return

        if (9 + 9 - k + 1) * k / 2 < n:
            return

        for num in range(now[-1] + 1, 10):
            now.append(num)
            self.dfs(n - num, k - 1, now, res)
            now.pop()
```
