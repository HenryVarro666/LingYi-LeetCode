---
title: "LCP 63. 弹珠游戏"
aliases: ["yiduobo的每日leetcode LCP63.弹珠游戏"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration", "leetcode/simulation", "题单/网格图", "题单/网格图/一-网格图-DFS"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/579546494"
zhihu_id: "579546494"
zhihu_title: "yiduobo的每日leetcode LCP63.弹珠游戏"
question_id: "LCP 63"
question: "弹珠游戏"
problem_url: "https://leetcode.cn/problems/EXvqDp/"
difficulty: "Medium"
created: "2022-11-02T01:43:45+08:00"
updated: "2022-11-02T01:43:45+08:00"
upvotes: 1
comments: 0
---

# LCP 63. 弹珠游戏

> **[yiduobo的每日leetcode LCP63.弹珠游戏](https://zhuanlan.zhihu.com/p/579546494) · 知乎 · 2022-11-02 · 赞同 1**
> 力扣：[LCP 63. 弹珠游戏](https://leetcode.cn/problems/EXvqDp/) · Medium · 灵茶山艾府：[暴力枚举模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP63.弹珠游戏

[力扣](https://leetcode.cn/problems/EXvqDp/)

当一颗弹珠被打进盘子之后，其行进路径其实是固定死了的，那么完全可以枚举所有弹珠的打入位置，判断其能否掉入洞中。另一方面，当某个弹珠以方向d来到位置(x, y)时，其最终结局其实也已经固定死了，那么在这里完全可以使用f[x][y][d]记录弹珠以方向d来到(x, y)时，在多少步内可以落入洞中。如果无法落入洞中，那么可以令f[x][y][d]等于num + 1，表示无法落入洞中。

接下来就只需要枚举每个起点，然后从这个起点开始进行记忆化搜索，计算从这里打入弹珠能否在num步内落入洞中即可。

另外，在具体实现上，对于左转和右转操作，可以将下标变换数组按照右、下、左、上的顺序排布好。当出现了右转时，将方向标记d加上1，反之出现左转时，将d减去1即可。

最后附上python代码：

```python
class Solution(object):
    def ballGame(self, num, plate):
        """
        :type num: int
        :type plate: List[str]
        :rtype: List[List[int]]
        """

        n = len(plate)
        m = len(plate[0])

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        f = [[[None] * 4 for _ in range(m)] for _ in range(n)]
        res = []

        def dfs(nowx, nowy, nowd):
            if f[nowx][nowy][nowd] is not None:
                return f[nowx][nowy][nowd]

            if plate[nowx][nowy] == 'O':
                f[nowx][nowy][nowd] = 0
                return 0
                
            if plate[nowx][nowy] == '.':
                d = nowd
            elif plate[nowx][nowy] == 'E':
                d = (nowd + 1) % 4
            else:
                d = (nowd + 3) % 4
                
            x = nowx + dx[d]
            y = nowy + dy[d]
            if x < 0 or x == n or y < 0 or y == m:
                f[nowx][nowy][nowd] = num + 1
                return num + 1
            
            f[nowx][nowy][nowd] = dfs(x, y, d) + 1
            return f[nowx][nowy][nowd]

        for index in range(1, m - 1):
            if plate[0][index] == '.' and dfs(0, index, 1) <= num:
                res.append([0, index])
            if plate[n - 1][index] == '.' and dfs(n - 1, index, 3) <= num:
                res.append([n - 1, index])
        
        for index in range(1, n - 1):
            if plate[index][0] == '.' and dfs(index, 0, 0) <= num:
                res.append([index, 0])
            if plate[index][m - 1] == '.' and dfs(index, m - 1, 2) <= num:
                res.append([index, m - 1])
        
        return res
```
