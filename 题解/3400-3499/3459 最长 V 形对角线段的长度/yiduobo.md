---
title: "3459. 最长V形对角线段的长度"
aliases: ["yiduobo的每日leetcode 3459.最长V形对角线段的长度"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/二-网格图-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1894838992928753538"
zhihu_id: "1894838992928753538"
zhihu_title: "yiduobo的每日leetcode 3459.最长V形对角线段的长度"
question_id: "3459"
question: "最长 V 形对角线段的长度"
problem_url: "https://leetcode.cn/problems/length-of-longest-v-shaped-diagonal-segment/"
difficulty: "Hard"
rating: 2337
created: "2025-04-13T20:28:27+08:00"
updated: "2025-04-13T20:28:27+08:00"
upvotes: 1
comments: 0
---

# 3459. 最长V形对角线段的长度

> **[yiduobo的每日leetcode 3459.最长V形对角线段的长度](https://zhuanlan.zhihu.com/p/1894838992928753538) · 知乎 · 2025-04-13 · 赞同 1**
> 力扣：[3459. 最长 V 形对角线段的长度](https://leetcode.cn/problems/length-of-longest-v-shaped-diagonal-segment/) · Hard · 灵茶山艾府：[记忆化搜索+最优性剪枝（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3459.最长V形对角线的长度

[3459. 最长 V 形对角线段的长度 - 力扣（LeetCode）](https://leetcode.cn/problems/length-of-longest-v-shaped-diagonal-segment/description/)

题目给出一个大小为n \* m的二维整数矩阵grid，其中grid的每个元素的值都在0到2之间。定义V形对角线为：

1、起点为所在单元格的值为1

2、后续单元格的值需要按照2、0、2、0、...的顺序出现

3、这条对角线一开始需要按照某个特定的对角线方向前进，期间可以执行最多一次顺时针90度转向，让前进方向变成另一个对角线方向

问矩阵中最长的V形对角线段长度为多少。如果不存在，则返回0。

由于题目中的路线可以执行一次转向操作，那么在这里肯定是要分方向进行讨论的。在这里可以先按顺时针顺序，规定向右上方走为方向0，向右下方走为方向1，向左下方走位方向2，向左上方走为方向3，那么对于当前的方向d，顺时针转向后的方向就是(d + 1) % 4。

接下来不妨先考虑转向后的走法，因为此时无需考虑在哪里转向，也无需考虑值为1的单元格，相对简单。令f[i][j][d]表示从单元格(i, j)开始，沿着方向d行走，且只经过值为0或者2的单元格时可以走过的最多单元格数目，那么对于f[i][j][d]，先通过d计算对应的下一个单元格(nxt_i, nxt_j)，具体来说：

当d \= 0时：nxt_i \= i - 1，nxt_j \= j + 1

当d \= 1时：nxt_i \= i + 1，nxt_j \= j + 1

当d \= 2时：nxt_i \= i + 1，nxt_j \= j - 1

当d \= 3时：nxt_i \= i - 1，nxt_j \= j - 1

那么对于f[i][j][d]，忽略所有grid[i][j]等于1的情况，而对于grid[i][j]不为1的情况，若grid[i][j] + grid[nxt_i][nxt_j] \= 2时，就有f[i][j][d] \= f[nxt_i][nxt_j][d] + 1，否则就有f[i][j][d] \= 1。

具体计算时需要注意遍历的顺序。在这里可以从上向下遍历计算d为0和3的情况，然后从下向上遍历计算d为1和2的情况。

得到f之后，按理说应该如法炮制，使用类似的方法计算未转向前从每个单元格出发可以行走的最多单元格数目。不过此时需要考虑值为1的单元格，还需要考虑转向的情况，实现起来会比较麻烦。

注意到本题中规定了从值为1的单元格出发，而1越多0和2就越少，也就是说可以作为起点的单元格越多，可以用作路径中的单元格就越少，直观感觉上来说暴力枚举起点以及转向前的路径应该也是可行的，因此我在这里选择直接枚举所有值为1的单元格，然后枚举转向前的方向d，沿着d不断行走直到无法继续行走为止。对于行走过程中的每个单元格，通过上面计算得到的f来计算在当前位置转向后可以得到的路径长度并更新最终答案。

最后附上python代码：

```python
class Solution(object):
    def lenOfVDiagonal(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        
        dx = [-1, 1, 1, -1]
        dy = [1, 1, -1, -1]
        n = len(grid)
        m = len(grid[0])
        f = [[[0] * 4 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 1:
                    continue
                
                if i - 1 >= 0:
                    if j - 1 >= 0 and grid[i - 1][j - 1] + grid[i][j] == 2:
                        f[i][j][3] = f[i - 1][j - 1][3] + 1
                    else:
                        f[i][j][3] = 1
                
                    if j + 1 < m and grid[i - 1][j + 1] + grid[i][j] == 2:
                        f[i][j][0] = f[i - 1][j + 1][0] + 1
                    else:
                        f[i][j][0] = 1

                else:
                    f[i][j][3] = 1
                    f[i][j][0] = 1

        for i in range(n - 1, -1, -1):
            for j in range(m):
                if grid[i][j] == 1:
                    continue
                
                if i + 1 < n:
                    if j - 1 >= 0 and grid[i + 1][j - 1] + grid[i][j] == 2:
                        f[i][j][2] = f[i + 1][j - 1][2] + 1
                    else:
                        f[i][j][2] = 1

                    if j + 1 < m and grid[i + 1][j + 1] + grid[i][j] == 2:
                        f[i][j][1] = f[i + 1][j + 1][1] + 1
                    else:
                        f[i][j][1] = 1

                else:
                    f[i][j][2] = 1
                    f[i][j][1] = 1

        res = 0
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 1:
                    for d in range(4):
                        target = 2
                        x = i + dx[d]
                        y = j + dy[d]
                        length = 1
                        res = max(res, 1)
                        while 0 <= x < n and 0 <= y < m and grid[x][y] == target:
                            length += 1
                            res = max(res, length + f[x][y][(d + 1) % 4] - 1)
                            target = 2 - target
                            x += dx[d]
                            y += dy[d]
                        
        
        return res
```
