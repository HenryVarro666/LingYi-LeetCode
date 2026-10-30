---
title: "77. 组合"
aliases: ["yiduobo的每日leetcode 77.组合"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/backtracking", "题单/链表-二叉树与回溯", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/四-回溯", "题单/面试经典-150-题/回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/133534751"
zhihu_id: "133534751"
zhihu_title: "yiduobo的每日leetcode 77.组合"
question_id: "77"
question: "组合"
problem_url: "https://leetcode.cn/problems/combinations/"
difficulty: "Medium"
created: "2020-04-19T23:36:25+08:00"
updated: "2020-04-19T23:36:25+08:00"
upvotes: 0
comments: 0
---

# 77. 组合

> **[yiduobo的每日leetcode 77.组合](https://zhuanlan.zhihu.com/p/133534751) · 知乎 · 2020-04-19 · 赞同 0**
> 力扣：[77. 组合](https://leetcode.cn/problems/combinations/) · Medium · 灵茶山艾府：[【视频讲解】回溯+剪枝优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

77.组合<https://leetcode-cn.com/problems/combinations/>

经典的搜索回溯题。依然是每轮操作将一个数加入到now中，然后进行下一轮操作。

因为题目中要求的是组合，因此我们可以要求now满足单调递增，于是在每次操作时，只需要尝试now[-1] + 1到n之间的数即可。为了方便起见，可以首先令now[0] \= 0，来处理边界情况。

最后附上python代码：

```python
class Solution(object):
    def combine(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: List[List[int]]
        """

        now = [0]
        res = []

        self.dfs(0, n, k, now, res)
        return res

    def dfs(self, level, n, k, now, res):
        if level == k:
            res.append(now[1:])
            return

        for index in range(now[-1] + 1, n + 1):
            now.append(index)
            self.dfs(level + 1, n, k, now, res)
            now.pop()
```
