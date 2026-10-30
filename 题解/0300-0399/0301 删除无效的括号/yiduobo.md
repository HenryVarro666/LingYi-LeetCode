---
title: "301. 删除无效的括号"
aliases: ["yiduobo的每日leetcode 301.删除无效的括号"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/157889096"
zhihu_id: "157889096"
zhihu_title: "yiduobo的每日leetcode 301.删除无效的括号"
question_id: "301"
question: "删除无效的括号"
problem_url: "https://leetcode.cn/problems/remove-invalid-parentheses/"
created: "2020-07-08T21:15:53+08:00"
updated: "2020-07-08T21:15:53+08:00"
upvotes: 0
comments: 0
---

# 301. 删除无效的括号

> **[yiduobo的每日leetcode 301.删除无效的括号](https://zhuanlan.zhihu.com/p/157889096) · 知乎 · 2020-07-08 · 赞同 0**
> 力扣：[301. 删除无效的括号](https://leetcode.cn/problems/remove-invalid-parentheses/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

301.删除无效的括号<https://leetcode-cn.com/problems/remove-invalid-parentheses/>

动态规划的题目，用记忆化搜索实现起来比较方便。

g[left][right]表示s中left到right这一段至少需要删除几个括号才能达成合法的状态，f[left][right]则为g[left][right]所对应的合法状态的集合。

那么对于f[left][right]：

1、若left\=right，说明此时只有一个字符s[left]:

此时若s[left]为左括号或者右括号，那么一定是不合法的，于是f[left][right]为空字符串，而g[left][right]\=1，表示需要删去该括号。

其他情况下可以直接保留s[left]，于是f[left][right]为集合(s[left])，而g[left][right] \= 0。

2、若s[left]不为左括号'(':

此时若s[left]为右括号')'，那么s[left]必须被删去，于是f[left][right] \= f[left + 1][right]，而g[left][right] \= g[left + 1][right] + 1，表示在g[left + 1][right]的基础上删去了s[left]。

其他情况下同样是保留s[left]，于是f[left][right]需要对f[left + 1][right]中的每个解都添加上s[left]，而g[left][right] \= g[left + 1][right]。

3、若s[right]不为右括号')':

同上，若s[right]为左括号'('，那么需要删去s[right]，于是f[left][right] \= f[left][right - 1]，而g[left][right] \= g[left][right - 1] + 1，表示在g[left][right - 1]的基础上删去了s[right]。

其他情况下需要保留s[right]，于是f[left][right]需要对f[left][right - 1]中的每个解都添加上s[right]，而g[left][right] \= g[left][right - 1]。

4、由于2和3都不成立，那么此时s[left][right]一定是形如 (XX..XXX) 的字符串：

1）可以保留两端的括号，于是f[left][right]可以从f[left + 1][right - 1]转移过来，即f[left][right] \= '(' + x + ')'，其中x为f[left + 1][right - 1]中的可行解。g[left][right]就是等于g[left + 1][right - 1]。

2）也可以left + 1到right - 1之间寻找分割点cut_pos，分别求解f[left][cut_pos]以及f[cut_pos + 1][right]。若此时g[left][cut_pos] + g[cut_pos + 1][right]要由于当前的g[left][right]的话，那么使用f[left][cut_pos]拼接上f[cut_pos + 1][right]作为f[left][right]。

最后的答案就是f[0][len(s) - 1]

二维的状态，每次转移需要枚举cut_pos，那么在状态的枚举上是O(n^3)的复杂度。但是在O(n^2)状态中，答案在f中的合并复杂度不太好计算，但是应该不会太高。总的来说应该比搜索好很多。

最后附上python代码：

```python
class Solution(object):
    def removeInvalidParentheses(self, s):
        """
        :type s: str
        :rtype: List[str]
        """

        if not s:
            return ['']

        f = [[None] * len(s) for _ in range(len(s))]
        g = [[None] * len(s) for _ in range(len(s))]
        self.dfs(0, len(s) - 1, s, f, g)

        return f[0][len(s) - 1]

    def dfs(self, left, right, s, f, g):
        if f[left][right] is not None:
            return

        if left == right:
            if s[left] not in ['(', ')']:
                f[left][right] = set([s[left]])
                g[left][right] = 0
            else:
                f[left][right] = set([''])
                g[left][right] = 1
            return

        if s[left] != '(':
            self.dfs(left + 1, right, s, f, g)
            if s[left] == ')':
                f[left][right] = f[left + 1][right]
                g[left][right] = g[left + 1][right] + 1
            else:
                f[left][right] = set([s[left] + x for x in f[left + 1][right]])
                g[left][right] = g[left + 1][right]
            return

        if s[right] != ')':
            self.dfs(left, right - 1, s, f, g)
            if s[right] == '(':
                f[left][right] = f[left][right - 1]
                g[left][right] = g[left][right - 1] + 1
            else:
                f[left][right] = set([x + s[right] for x in f[left][right - 1]])
                g[left][right] = g[left][right - 1]
            return

        if left == right - 1:
            f[left][right] = set(['()'])
            g[left][right] = 0
            return

        self.dfs(left + 1, right - 1, s, f, g)
        f[left][right] = set(['(' + x + ')' for x in f[left + 1][right - 1]])
        min_len = g[left + 1][right - 1]

        choose_pos = []
        for cut_pos in range(left, right):
            self.dfs(left, cut_pos, s, f, g)
            self.dfs(cut_pos + 1, right, s, f, g)
            cut_len = g[left][cut_pos] + g[cut_pos + 1][right]
            if cut_len < min_len:
                min_len = cut_len
                choose_pos = [cut_pos]
            elif cut_len == min_len:
                choose_pos.append(cut_pos)

        if min_len != g[left + 1][right - 1]:
            f[left][right] = set()

        for cut_pos in choose_pos:
            for first_part in f[left][cut_pos]:
                for second_part in f[cut_pos + 1][right]:
                    f[left][right].add(first_part + second_part)

        g[left][right] = min_len
```
