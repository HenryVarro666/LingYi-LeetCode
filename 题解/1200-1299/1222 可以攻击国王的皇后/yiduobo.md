---
title: "1222. 可以攻击国王的皇后"
aliases: ["yiduobo的每日leetcode 1222.可以攻击国王的皇后"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/383403635"
zhihu_id: "383403635"
zhihu_title: "yiduobo的每日leetcode 1222.可以攻击国王的皇后"
question_id: "1222"
question: "可以攻击国王的皇后"
problem_url: "https://leetcode.cn/problems/queens-that-can-attack-the-king/"
difficulty: "Medium"
created: "2021-06-23T23:50:13+08:00"
updated: "2021-06-23T23:50:13+08:00"
upvotes: 0
comments: 0
---

# 1222. 可以攻击国王的皇后

> **[yiduobo的每日leetcode 1222.可以攻击国王的皇后](https://zhuanlan.zhihu.com/p/383403635) · 知乎 · 2021-06-23 · 赞同 0**
> 力扣：[1222. 可以攻击国王的皇后](https://leetcode.cn/problems/queens-that-can-attack-the-king/) · Medium · 灵茶山艾府：[统计能被国王「看到」的皇后（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1222.可以攻击国王的皇后

[力扣](https://leetcode-cn.com/problems/queens-that-can-attack-the-king/)

国王可能从八个方向上受到攻击，但同一方向上只有最近的皇后能攻击到国王，因此我们不应该从皇后出发，而应该从国王出发，分别向八个方向前进。

遍历八个方向，开始向边界前进。若途中遇到皇后，说明在这个方向上将被当前位置上的皇后攻击，因此要将这个皇后加入到答案。若在这个方向上走到棋盘边界还没有遇到皇后，则说明这个方向上不会受到攻击。

最后附上python代码：

```python
class Solution(object):
    def queensAttacktheKing(self, queens, king):
        """
        :type queens: List[List[int]]
        :type king: List[int]
        :rtype: List[List[int]]
        """

        queen_set = set()
        for x, y in queens:
            queen_set.add((x, y))
        dx = [0, 1, 1, 1, 0, -1, -1, -1]
        dy = [1, 1, 0, -1, -1, -1, 0, 1]
        res = []
        for index in range(8):
            nowx, nowy = king
            while True:
                nowx += dx[index]
                nowy += dy[index]
                if nowx < 0 or nowx == 8 or nowy < 0 or nowy == 8:
                    break
                if (nowx, nowy) in queen_set:
                    res.append([nowx, nowy])
                    break
        
        return res
```
