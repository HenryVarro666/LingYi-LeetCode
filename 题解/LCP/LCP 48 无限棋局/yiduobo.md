---
title: "LCP 48. 无限棋局"
aliases: ["yiduobo的每日leetcode LCP48.无限棋局"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/常用数据结构", "题单/数学算法", "题单/贪心算法", "题单/常用数据结构/编程能力强化训练", "题单/数学算法/四-博弈论", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/576915301"
zhihu_id: "576915301"
zhihu_title: "yiduobo的每日leetcode LCP48.无限棋局"
question_id: "LCP 48"
question: "无限棋局"
problem_url: "https://leetcode.cn/problems/fsa7oZ/"
difficulty: "Hard"
created: "2022-10-25T01:35:53+08:00"
updated: "2022-10-25T01:35:53+08:00"
upvotes: 0
comments: 0
---

# LCP 48. 无限棋局

> **[yiduobo的每日leetcode LCP48.无限棋局](https://zhuanlan.zhihu.com/p/576915301) · 知乎 · 2022-10-25 · 赞同 0**
> 力扣：[LCP 48. 无限棋局](https://leetcode.cn/problems/fsa7oZ/) · Hard · 灵茶山艾府：[分类讨论+枚举](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP48.无限棋局

[力扣](https://leetcode.cn/problems/fsa7oZ/)

题目给出一个五子棋的棋局，轮到黑行动，问三步之内能否分出胜负。

首先，如果当前盘面上有5缺1的黑子，那么将其填充成5连，黑就能取胜。

接下来，如果不存在5缺1的黑子，那么就可以按照上面找5缺1黑子的做法，找出所有的5缺1白子。此时可以分为两种情况：

1、存在5缺1的白子，黑棋被迫进行防守

2、不存在5缺1的白子，黑棋可以尝试发展一处黑子

对于情况1，如果存在两个位置可以使得白子形成5连，说明黑防守不过来，此时白能取胜。若只存在一个位置可以使得白子形成5连，那么黑就应该在这里防守，且白子下一步也应该选择防守。

对于情况2，若不存在5缺1的白子，那么黑子没有必要进行防守，可以选择任意位置发展一处黑子，然后白子应该针对性进行防守。

综合起来可以发现，一共只有四种情况：

1、黑棋可以直接取胜

2、黑棋无法直接取胜，但是白子存在两处或以上的5缺1需要防守，此时白棋取胜

3、黑棋无法直接取胜，但是白子存在一处5缺1的防守，此时黑子需要在此防守。如果在本次防守后黑子出现了两处或以上的5缺1需要防守，此时黑棋取胜，否则和棋

4、黑棋无法直接取胜，且无需防守白子。此时黑子可以选择在任意位置发展一处黑子。枚举所有发展黑子的位置，若在此种情况下黑子出现了两处或以上的5缺1需要防守，那么黑棋取胜，否则和棋

落子的思路其实很直观，但是在具体实现上，判断5缺1和情况4中选择发展黑子的位置需要特别注意。

首先是判断5缺1。由于这个缺1可以缺在任意位置上，即XXXX\_，\_XXXX，XX_XX这些情况都是5缺1，那么保险起见，对于(x, y)这颗棋子，需要考虑两条对角线以及水平竖直一共4个方向，同时需要考虑所有的5种起始位置。

而对于发展黑子而言，发展出去的黑子离现有的最大距离不应该超过2，否则就相当于发展了一个孤立的黑子，不可能仅通过之后的一步形成5连。另外，对于发展出来的黑子，需要检测的也只是包含这枚黑子的5缺1，而无需检测其他的黑子，因为一开始已经检测过一次了。

最后附上python代码：

```python
class Solution(object):
    def gobang(self, pieces):
        """
        :type pieces: List[List[int]]
        :rtype: str
        """

        piece_dict = {}
        for x, y, c in pieces:
            piece_dict[(x, y)] = c

        dx = [0, 1, 1, 1]
        dy = [1, 1, 0, -1]

        def check_line(sx, sy, check_c, dx, dy):
            fill_x, fill_y = None, None
            for length in range(5):
                x = sx + length * dx
                y = sy + length * dy
                c = piece_dict.get((x, y))
                if c == check_c:
                    continue
                if (c == 1 - check_c) or (fill_x is not None):
                    return None, None
                fill_x, fill_y = x, y
            
            return fill_x, fill_y

        def check_point(x, y, c):
            fill_set = set()
            for length in range(0, 5):
                for index in range(4):
                    fill_x, fill_y = check_line(x - length * dx[index], y - length * dy[index], c, dx[index], dy[index])
                    if fill_x is not None:
                        fill_set.add((fill_x, fill_y))
        
            return fill_set

        need_fill = set()
        for x, y, c in pieces:
            if c == 0:
                if len(check_point(x, y, c)):
                    return 'Black'
                
            else:
                need_fill.update(check_point(x, y, c))
        
        if len(need_fill) >= 2:
            return 'White'

        if len(need_fill) == 1:
            candidate = need_fill
        else:
            candidate = set()
            for x, y, c in pieces:
                if c == 0:
                    for index in range(4):
                        if piece_dict.get((x + dx[index], y + dy[index]), None) is None:
                            candidate.add((x + dx[index], y + dy[index]))
                            if piece_dict.get((x + dx[index] * 2, y + dy[index] * 2), None) is None:
                                candidate.add((x + dx[index] * 2, y + dy[index] * 2))
                        if piece_dict.get((x - dx[index], y - dy[index]), None) is None:
                            candidate.add((x - dx[index], y - dy[index]))
                            if piece_dict.get((x - dx[index] * 2, y - dy[index] * 2), None) is None:
                                candidate.add((x - dx[index] * 2, y - dy[index] * 2))

        for x, y in candidate:
            piece_dict[(x, y)] = 0
            if len(check_point(x, y, 0)) >= 2:
                return 'Black'
            piece_dict.pop((x, y))

        return 'None'
```
