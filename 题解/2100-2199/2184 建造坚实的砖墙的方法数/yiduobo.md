---
title: "2184. 建造坚实的砖墙的方法数"
aliases: ["yiduobo的每日leetcode 2184.建造坚实的砖墙的方法数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/627401196"
zhihu_id: "627401196"
zhihu_title: "yiduobo的每日leetcode 2184.建造坚实的砖墙的方法数"
question_id: "2184"
question: "建造坚实的砖墙的方法数"
problem_url: "https://leetcode.cn/problems/number-of-ways-to-build-sturdy-brick-wall/"
created: "2023-05-07T02:26:29+08:00"
updated: "2023-05-07T02:26:29+08:00"
upvotes: 0
comments: 0
---

# 2184. 建造坚实的砖墙的方法数

> **[yiduobo的每日leetcode 2184.建造坚实的砖墙的方法数](https://zhuanlan.zhihu.com/p/627401196) · 知乎 · 2023-05-07 · 赞同 0**
> 力扣：[2184. 建造坚实的砖墙的方法数](https://leetcode.cn/problems/number-of-ways-to-build-sturdy-brick-wall/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2184.建造坚实的砖墙的方法数

[力扣](https://leetcode.cn/problems/number-of-ways-to-build-sturdy-brick-wall/)

首先，由于每一行的长度不超过10，那么可以使用状态压缩来表示当前这一行有哪些位置是砖缝，然后就可以通过状态压缩动态规划来计算当前这些砖在单一的行中可以砌成什么样。

具体实现上，可以用过lowbit操作分离出每个state的最低位的1，然后检测是否存在长度适配的砖头。若存在，就可以将state右移，右移的位数与这块砖头的长度一致，然后重复此过程直到无法适配，或者全部适配上。

需要注意在这里最左侧的边界不应该考虑在状态内，但最右侧的边界应该考虑进去，因为只有最右侧被某块砖的边界覆盖住，这一行才是完整的一行。因此在计算完所有状态是否可行后，应该取1 \<\< (width - 1)到(1 \<\< width) - 1间的状态加入到堆砌方案候选集当中。

得到candidate后，则可以从下到上再次使用动态规划。

令f[i][state]表示最下面的i行中，最上面这一行的堆砌方式为state时的可行方案数。那么对于f[i][state]，可以从candidate中枚举所有的可行方案，只要当前枚举到的方案cand与state按位与等于0，那么就说明cand与state是没有对齐的砖缝的，因此就有f[i + 1][cand] +\= f[i][state]。

计算完成后，只需将整面墙最上面这一行所有state对应的方案数累加起来即为最终答案。

另外，注意到每一行只需下面这一行有关，因此可以使用滚动数组来节省掉i这一行。

最后附上python代码：

```python
class Solution(object):
    def buildWall(self, height, width, bricks):
        """
        :type height: int
        :type width: int
        :type bricks: List[int]
        :rtype: int
        """

        move_mapping = {}
        for b in bricks:
            if b > width:
                continue
            move_mapping[1 << (b - 1)] = b

        f = [False] * (1 << width)
        f[0] = True
        for state in range(1 << width):
            lowbit = state & -state
            if lowbit in move_mapping and f[state >> move_mapping[lowbit]]:
                f[state] = True
        
        candidate = []
        for state in range(1 << (width - 1), 1 << width):
            if f[state]:
                candidate.append(state ^ (1 << (width - 1)))

        mod = 10 ** 9 + 7
        g = [0] * (1 << (width - 1))
        g[0] = 1
        for _ in range(height):
            h = g[:]
            g = [0] * (1 << (width - 1))
            for state in range(1 << (width - 1)):
                for cand in candidate:
                    if state & cand == 0:
                        g[cand] += h[state]
                        if g[cand] >= mod:
                            g[cand] -= mod
        
        res = 0
        for state in range(1 << (width - 1)):
            res += g[state]
            if res >= mod:
                res -= mod

        return res
```
