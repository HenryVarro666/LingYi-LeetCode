---
title: "1036. 逃离大迷宫"
aliases: ["yiduobo的每日leetcode 1036.逃离大迷宫"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/370212999"
zhihu_id: "370212999"
zhihu_title: "yiduobo的每日leetcode 1036.逃离大迷宫"
question_id: "1036"
question: "逃离大迷宫"
problem_url: "https://leetcode.cn/problems/escape-a-large-maze/"
created: "2021-05-06T21:18:27+08:00"
updated: "2021-05-06T21:18:27+08:00"
upvotes: 0
comments: 0
---

# 1036. 逃离大迷宫

> **[yiduobo的每日leetcode 1036.逃离大迷宫](https://zhuanlan.zhihu.com/p/370212999) · 知乎 · 2021-05-06 · 赞同 0**
> 力扣：[1036. 逃离大迷宫](https://leetcode.cn/problems/escape-a-large-maze/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1036.逃离大迷宫

[力扣](https://leetcode-cn.com/problems/escape-a-large-maze/)

乍一看题目感觉很难，可能涉及到了计算几何和平面图之类的东西，不过注意到封锁方格的数量最多只有200个，那么就有了一种比较trick的做法。

只有当封锁方格将source和target分到了两个不相连的部分中时，答案才是false。那么对于仅仅200个方格而言，即使利用上边界，可以形成的封闭平面大小也很小。极限情况下应该是这200个方格与两条边界一起构成了一个直角边长为200的等腰直角三角形，其中这些封锁方格扮演了斜边的角色。那么在这个最大的封闭平面中，也仅仅只有(1 + 199) \* 199 / 2 \= 19900个方格。换言之，若source或target被封锁在某个封闭平面内，那么该平面最多也只有19900个格子。

于是我们可以先从source开始进行bfs：

1、若可以直接到达target，那么答案自然是true

2、若bfs在19900步之内结束，那么说明source被封锁起来了，于是返回false

3、若bfs在19900步之后后任然没有结束，那么就说明source必然不在某个封闭平面之内，那么接下来从target开始bfs，同样是判断能否在19900步之内结束bfs

最后附上python代码：

```python
class Solution(object):
    def isEscapePossible(self, blocked, source, target):
        """
        :type blocked: List[List[int]]
        :type source: List[int]
        :type target: List[int]
        :rtype: bool
        """

        max_l = 19900
        blocked_set = set()
        for x, y in blocked:
            blocked_set.add(x * 1000000 + y)

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        q = [source]
        l = 0
        r = 1
        used = set()
        used.add(source[0] * 1000000 + source[1])
        while l < r:
            nowx, nowy = q[l]
            l += 1
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x >= 0 and x < 1000000 and y >= 0 and y < 1000000 and x * 1000000 + y not in blocked_set and x * 1000000 + y not in used:
                    q.append([x, y])
                    r += 1
                    used.add(x * 1000000 + y)
                    if x == target[0] and y == target[1]:
                        return True
            
            if r > 19900:
                break
        
        if r <= 19900:
            return False
        
        q = [target]
        l = 0
        r = 1
        used = set()
        used.add(target[0] * 1000000 + target[1])
        while l < r:
            nowx, nowy = q[l]
            l += 1
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x >= 0 and x < 1000000 and y >= 0 and y < 1000000 and x * 1000000 + y not in blocked_set and x * 1000000 + y not in used:
                    q.append([x, y])
                    r += 1
                    used.add(x * 1000000 + y)
            
            if r > 19900:
                break

        return r > 19900
```
