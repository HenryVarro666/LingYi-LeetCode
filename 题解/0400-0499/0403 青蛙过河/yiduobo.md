---
title: "403. 青蛙过河"
aliases: ["yiduobo的每日leetcode 403.青蛙过河"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/183978733"
zhihu_id: "183978733"
zhihu_title: "yiduobo的每日leetcode 403.青蛙过河"
question_id: "403"
question: "青蛙过河"
problem_url: "https://leetcode.cn/problems/frog-jump/"
created: "2020-08-14T23:39:14+08:00"
updated: "2020-08-14T23:39:14+08:00"
upvotes: 0
comments: 0
---

# 403. 青蛙过河

> **[yiduobo的每日leetcode 403.青蛙过河](https://zhuanlan.zhihu.com/p/183978733) · 知乎 · 2020-08-14 · 赞同 0**
> 力扣：[403. 青蛙过河](https://leetcode.cn/problems/frog-jump/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

403.青蛙过河<https://leetcode-cn.com/problems/frog-jump/>

这一题乍一看跟先前某道题目很像，但是注意到这里每次跳的步长是有下限的，因此不能再使用之前的贪心法。我采用的是记忆化搜索的做法，用f[i][j]表示如果这一步从石头i跳到了石头j，那么最后是否可能到达终点。

对于f[i][j]，这一步是从石头i跳到了石头j，那么就可以计算出这一步的跳跃距离k。

接下来枚举k - 1、k、k + 1，那么从石头j起跳，下一步到达的位置可能是stones[j] + k - 1，stone[j] + k以及stones[j] + k + 1。判断在这些位置上是否存在石头next，如果存在的话，那么递归计算f[j][next]。只要存在任意f[j][next]为真，那么就有f[i][j]为真，否则f[i][j]为假。

计算完成后，f[0][1]即为最终的答案。

对于判断是否存在next，可以先使用一个pos_dict建立每个石头的位置到石头编号的映射，这样一来就可以在常数时间内判断从石头j起跳下一跳能到哪些石头上了。

另外需要注意的是，题目要求青蛙只能往前跳，因此每次跳跃时都必须满足next > j。

最后附上python代码：

```python
class Solution(object):
    def canCross(self, stones):
        """
        :type stones: List[int]
        :rtype: bool
        """

        if stones[1] != 1:
            return False

        pos_dict = {}
        for index, pos in enumerate(stones):
            pos_dict[pos] = index

        f = [[None] * len(stones) for _ in range(len(stones))]
        return self.dfs(0, 1, f, stones, pos_dict)

    def dfs(self, prev_pos, now, f, stones, pos_dict):
        if now == len(stones) - 1:
            return True

        if f[prev_pos][now] is not None:
            return False

        prev_len = stones[now] - stones[prev_pos]
        for k in range(-1, 2):
            next_pos = pos_dict.get(stones[now] + prev_len + k, 0)
            if next_pos > now and self.dfs(now, next_pos, f, stones, pos_dict):
                return True

        f[prev_pos][now] = False
        return False
```
