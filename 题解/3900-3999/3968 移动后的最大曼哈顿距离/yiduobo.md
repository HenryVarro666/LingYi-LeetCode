---
title: "3968. 移动后的最大曼哈顿距离"
aliases: ["yiduobo的每日leetcode 3968.移动后的最大曼哈顿距离"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2052161188969161166"
zhihu_id: "2052161188969161166"
zhihu_title: "yiduobo的每日leetcode 3968.移动后的最大曼哈顿距离"
question_id: "3968"
question: "移动后的最大曼哈顿距离"
problem_url: "https://leetcode.cn/problems/maximum-manhattan-distance-after-all-moves/"
difficulty: "Medium"
created: "2026-06-24T22:29:47+08:00"
updated: "2026-06-24T22:29:51+08:00"
upvotes: 0
comments: 0
---

# 3968. 移动后的最大曼哈顿距离

> **[yiduobo的每日leetcode 3968.移动后的最大曼哈顿距离](https://zhuanlan.zhihu.com/p/2052161188969161166) · 知乎 · 2026-06-24 · 赞同 0**
> 力扣：[3968. 移动后的最大曼哈顿距离](https://leetcode.cn/problems/maximum-manhattan-distance-after-all-moves/) · Medium · 灵茶山艾府：[贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3968.移动后的最大曼哈顿距离

<https://leetcode.cn/problems/maximum-manhattan-distance-after-all-moves/>

题目给出一个由字符'U'、'D'、'L'、'R'和'\_'组成的字符串moves。

从原点(0, 0)出发，每个字符表示二维平面上的一次移动：

- 'U'：向上移动一个单位
- 'D'：向下移动一个单位
- 'L'：向左移动一个单位
- 'R'：向右移动一个单位
- '\_'：可以独立地替换为其他四种字符中的一个，并进行对应的移动

问执行完所有移动后，能够达到的距离原点的最大曼哈顿距离。

题目需要计算的是距离原点的最大曼哈顿距离，那么就意味着水平和竖直方向上的移动互不影响。因此在这里可以先对moves进行一趟遍历，计算水平和竖直方向上两种不同移动的数量之差，记为h和v，那么如果不考虑'\_'，最终答案就是abs(v) + abs(h)。

而对于所有的'\_'，在这里只需顺着水平或者竖直方向上较多的那一种移动，进一步向远离远点的方向移动就行了，因此在上面的遍历过程还需要额外记录'\_'的数量space，那么最终答案就是abs(v) + abs(h) + space。

最后附上python代码：

```python
class Solution(object):
    def maxDistance(self, moves):
        """
        :type moves: str
        :rtype: int
        """
        
        v = 0
        h = 0
        space = 0
        for c in moves:
            if c == 'U':
                v += 1
            elif c == 'D':
                v -= 1
            elif c == 'L':
                h -= 1
            elif c == 'R':
                h += 1
            else:
                space += 1
        
        return abs(v) + abs(h) + space
```
