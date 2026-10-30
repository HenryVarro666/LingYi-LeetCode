---
title: "2267. 检查是否有合法括号字符串路径"
aliases: ["yiduobo的每日leetcode 2267.检查是否有合法括号字符串路径"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/graph", "leetcode/memoization", "leetcode/jian-zhi", "题单/常用数据结构", "题单/网格图", "题单/动态规划", "题单/常用数据结构/三-栈", "题单/网格图/五-综合应用", "题单/动态规划/二-网格图-DP", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/549206456"
zhihu_id: "549206456"
zhihu_title: "yiduobo的每日leetcode 2267.检查是否有合法括号字符串路径"
question_id: "2267"
question: "检查是否有合法括号字符串路径"
problem_url: "https://leetcode.cn/problems/check-if-there-is-a-valid-parentheses-string-path/"
difficulty: "Hard"
rating: 2085
created: "2022-08-03T01:06:55+08:00"
updated: "2022-08-03T01:06:55+08:00"
upvotes: 0
comments: 0
---

# 2267. 检查是否有合法括号字符串路径

> **[yiduobo的每日leetcode 2267.检查是否有合法括号字符串路径](https://zhuanlan.zhihu.com/p/549206456) · 知乎 · 2022-08-03 · 赞同 0**
> 力扣：[2267. 检查是否有合法括号字符串路径](https://leetcode.cn/problems/check-if-there-is-a-valid-parentheses-string-path/) · Hard · 灵茶山艾府：[添加状态后 DFS + 剪枝优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2267.检查是否有合法括号字符串路径

[力扣](https://leetcode.cn/problems/check-if-there-is-a-valid-parentheses-string-path/)

题目中的合法括号字符串路径必须符合两个条件：

1、最终的路径的任意前缀，左右括号抵消后的结果必须是剩余左括号的数目大于等于0

2、最终路径的括号必须是匹配的

如果只需要满足第一点，那么可以仿照矩阵中的最长路径的做法给出一个二维的状态f[i][j]，表示以格子(i, j)为终点的路径在左右括号抵消后最多能剩余几个左括号。但是需要注意的是，这个做法无法得到最终的答案，因为最后的路径括号必须是刚好匹配的，而这个状态表示很可能为了获取尽量多的左括号导致到了最后依然是左括号过剩。

换言之，对于以(i, j)为终点的路径，并没有一个标准来决定此时应该有多少剩余的左括号，因此在这里需要将所有可能行都考虑进来，也就是说将状态改为f[i][j][k]表示是否存在以(i, j)为终点的路径，在括号抵消后剩余的左括号数目恰好为k个。由于路径最多经过m + n - 1个单元格，因此一条合法的括号路径中任意时刻剩余的左括号数目都不超过100个，因此这个三次方的状态表示勉勉强强可以通过。

当然，这种状态表示法实际上有很多k都是不可能达到的，因此我在这里将状态改成了f[i][j]表示以(i, j)为终点的路径，在括号抵消后所有可能的剩余左括号数目的集合。

至于状态转移，则还是与经典的矩阵中的最长路径一样，考虑从上方或者左侧走到当前单元格的情况，然后利用这两个单元格的信息更新当前单元格即可。

动态规划完成后，如果f[m - 1][n - 1]对应的集合中有0，说明存在一条合法路径。

最后附上python代码：

```python
class Solution(object):
    def hasValidPath(self, grid):
        """
        :type grid: List[List[str]]
        :rtype: bool
        """

        m = len(grid)
        n = len(grid[0])
        f = [[set() for j in range(n)] for i in range(m)]
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '(':
                    delta = 1
                else:
                    delta = -1
                
                if i == 0:
                    if j == 0:
                        if delta == -1:
                            return False
                        else:
                            f[i][j].add(1)
                    else:
                        for cnt in list(f[i][j - 1]):
                            if 0 <= cnt + delta <= m + n - i - j:
                                f[i][j].add(cnt + delta)
                elif j == 0:
                    for cnt in list(f[i - 1][j]):
                        if 0 <= cnt + delta <= m + n - i - j:
                            f[i][j].add(cnt + delta)
                else:
                    for cnt in list(f[i - 1][j]):
                        if 0 <= cnt + delta <= m + n - i - j:
                            f[i][j].add(cnt + delta)
                    
                    for cnt in list(f[i][j - 1]):
                        if 0 <= cnt + delta <= m + n - i - j:
                            f[i][j].add(cnt + delta)

        return 0 in f[-1][-1]
```
