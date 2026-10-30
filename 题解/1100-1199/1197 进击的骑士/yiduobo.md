---
title: "1197. 进击的骑士"
aliases: ["yiduobo的每日leetcode 1197.进击的骑士"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/612766772"
zhihu_id: "612766772"
zhihu_title: "yiduobo的每日leetcode 1197.进击的骑士"
question_id: "1197"
question: "进击的骑士"
problem_url: "https://leetcode.cn/problems/minimum-knight-moves/"
created: "2023-03-10T02:20:35+08:00"
updated: "2023-03-10T02:20:35+08:00"
upvotes: 1
comments: 3
---

# 1197. 进击的骑士

> **[yiduobo的每日leetcode 1197.进击的骑士](https://zhuanlan.zhihu.com/p/612766772) · 知乎 · 2023-03-10 · 赞同 1**
> 力扣：[1197. 进击的骑士](https://leetcode.cn/problems/minimum-knight-moves/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1197.进击的骑士

[力扣](https://leetcode.cn/problems/minimum-knight-moves/)

目标点(x, y)的两维都被限制在300之内，因此即使不考虑任何优化，也只需在300 \* 300大小的棋盘内做一次bfs，时间复杂度方面是完全没有问题的。

更优的做法则是利用一些线性代数的知识来进行优化，具体来说，本题中马实际上只有4中跳法，也就是题目图中右半边的1点、2点、4点、5点这四个方向上的跳法，而题目图中左侧的四种跳法则可以认为是右侧四种跳法反着跳的结果。于是问题就转化成了给出两个4元的不定方程，要求四个未知数的绝对值之和最小。

由于马的走法之间存在一些冲突的地方，因此在产生抵消后可能出现一些步数的损耗，例如2点方向跳5步，来到(10, 5)，接下来4点方向反跳3步，来到(4, 8)，也就是话费了5 + 3 \= 8步来到了(4, 8)，然而对于(4, 8)这个位置，显然可以通过往1点方向跳4步得到。换言之，在某两个方向上的步数不可能同时大于某个阈值，否则就会出现另一方向上步数更少的替代方案。于是可以先分析出各个方向的组合上步数阈值，就可以在这个阈值内枚举其中两个方向上的步数，然后利用方程求解剩下两个方向上的步数即可。

我在这里偷懒，直接使用的暴力bfs。

最后附上python代码：

```python
class Solution(object):
    def minKnightMoves(self, x, y):
        """
        :type x: int
        :type y: int
        :rtype: int
        """

        

        dx = [1, 2, 2, 1, -1, -2, -2, -1]
        dy = [2, 1, -1, -2, -2, -1, 1, 2]

        q = [[0, 0]]
        vis = set()
        vis.add((0, 0))
        head, tail = 0, 1
        res = 0
        while (x, y) not in vis:
            res += 1
            for nowx, nowy in q[head : tail]:
                for index in range(8):
                    nx = nowx + dx[index]
                    ny = nowy + dy[index]
                    if -300 <= nx <= 300 and -300 <= ny <= 300 and (nx, ny) not in vis:
                        vis.add((nx, ny))
                        q.append([nx, ny])
            
            head, tail = tail, len(q)
        
        return res
```
