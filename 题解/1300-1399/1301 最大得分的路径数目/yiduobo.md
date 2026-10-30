---
title: "1301. 最大得分的路径数目"
aliases: ["yiduobo的每日leetcode 1301.最大得分的路径数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/二-网格图-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/390813326"
zhihu_id: "390813326"
zhihu_title: "yiduobo的每日leetcode 1301.最大得分的路径数目"
question_id: "1301"
question: "最大得分的路径数目"
problem_url: "https://leetcode.cn/problems/number-of-paths-with-max-score/"
difficulty: "Hard"
rating: 1853
created: "2021-07-18T16:46:34+08:00"
updated: "2021-07-18T16:46:34+08:00"
upvotes: 0
comments: 0
---

# 1301. 最大得分的路径数目

> **[yiduobo的每日leetcode 1301.最大得分的路径数目](https://zhuanlan.zhihu.com/p/390813326) · 知乎 · 2021-07-18 · 赞同 0**
> 力扣：[1301. 最大得分的路径数目](https://leetcode.cn/problems/number-of-paths-with-max-score/) · Hard · 灵茶山艾府：[网格图 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1301.最大得分的路径数目

[力扣](https://leetcode-cn.com/problems/number-of-paths-with-max-score/)

经典的动态规划问题。题目要求从右下角走到左上角，但是过程中并没有什么额外限制，因此我们可以认为问题是从左上角开始走到右下角。

令f[i][j][0]表示走到第i行第j列的最大得分是多少，f[i][j][1]表示得到这个最大得分的路径数目。那么对于f[i][j]：

1、当前的board[x][y] \= 'E'，即位于左上角，应当初始化f[i][j][0] \= 0，f[i][j][1] \= 1

2、当前的board[x][y] \= 'X'，说明当前位置是障碍，那么将f[i][j][0]和f[i][j][1]都置为0

3、当前的board[x][y]为数字或者等于'S'，此时我们应当分别考虑三种走法。

3-1）考察从上方走过来的情况，记对应的最大路径和为v1，对应的路径数目为s1：

若当前的i > 0，且board[i - 1][j]不等于'X'，也就是f[i - 1][j][1]大于0，那么此时可以从board[i - 1][j]走过来，对应的v1就是f[i - 1][j][0]，s1就是f[i - 1][j][1]；其他情况下，从board[i - 1][j]走到board[i][j]是不合法的，那么应当置v1为-1

3-1）考察从左方走过来的情况，记对应的最大路径和为v2，对应的路径数目为s2：

若当前的j > 0，且board[i][j - 1]不等于'X'，也就是f[i][j - 1][1]大于0，那么此时可以从board[i][j - 1]走过来，对应的v2就是f[i][j - 1][0]，s2就是f[i][j - 1][1]；其他情况下，从board[i][j - 1]走到board[i][j]是不合法的，那么应当置v2为-1

3-3）考察从左上方走过来的情况，记对应的最大路径和为v3，对应的路径数目为s3：

若当前的i > 0、j > 0，且board[i - 1][j - 1]不等于'X'，也就是f[i - 1][j - 1][1]大于0，那么此时可以从board[i - 1][j - 1]走过来，对应的v3就是f[i - 1][j - 1][0]，s3就是f[i - 1][j - 1][1]；其他情况下，从board[i - 1][j - 1]走到board[i][j]是不合法的，那么应当置v3为-1

得到v1、v2、v3之后，若此时的v1、v2、v3都为-1，那么说明没法走到board\[i\]\[j\]，于是应当置f\[i\]\[j\]\[0\]\]和f\[i\]\[j\]\[1\]都为0。

若其中有一个大于0，那么此时的最大路径和就是f[i][j][0] \= max(v1, v2, v3) + board[i][j]。当然，若此时的board[i][j]等于'S'，说明走到了右下角，那么可以认为对应的board[i][j]为0。

接下来，只需要判断v1、v2、v3中哪些等于max(v1, v2, v3)，并将对应的s累加到f[i][j][1]当中即可。

动态规划完成后，最终答案就是f[-1][-1][0]和f[-1][-1][1]。

另外，注意到每一轮的结果只与上一轮有关，那么我们可以使用滚动数组省去i这一维。

最后附上python代码：

```python
class Solution(object):
    def pathsWithMaxScore(self, board):
        """
        :type board: List[str]
        :rtype: List[int]
        """

        mod = 10 ** 9 + 7
        m = len(board)
        n = len(board[0])
        f = []
        g = []
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'X':
                    f.append([0, 0])
                elif board[i][j] == 'E':
                    f.append([0, 1])
                else:
                    v1 = v2 = v3 = -1
                    if i > 0 and g[j][1] > 0:
                        v1 = g[j][0]
                        s1 = g[j][1]
                    if j > 0 and f[-1][1] > 0:
                        v2 = f[-1][0]
                        s2 = f[-1][1]
                    if i > 0 and j > 0 and g[j - 1][1] > 0:
                        v3 = g[j - 1][0]
                        s3 = g[j - 1][1]
                    
                    max_v = max(v1, v2, v3)
                    if max_v < 0:
                        f.append([0, 0])
                    else:
                        s = 0
                        if v1 == max_v:
                            s += s1
                        if v2 == max_v:
                            s += s2
                            s %= mod
                        if v3 == max_v:
                            s += s3
                            s %= mod
                        if board[i][j] != 'S':
                            max_v += int(board[i][j])
                        f.append([max_v, s])
            
            g = f[:]
            f = []
        
        return g[-1]
```
