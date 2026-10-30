---
title: "294. 翻转游戏II"
aliases: ["yiduobo的每日leetcode 294.翻转游戏II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/595337665"
zhihu_id: "595337665"
zhihu_title: "yiduobo的每日leetcode 294.翻转游戏II"
question_id: "294"
question: "翻转游戏II"
problem_url: "https://leetcode.cn/problems/flip-game-ii/"
created: "2022-12-30T00:25:40+08:00"
updated: "2022-12-30T00:25:40+08:00"
upvotes: 0
comments: 0
---

# 294. 翻转游戏II

> **[yiduobo的每日leetcode 294.翻转游戏II](https://zhuanlan.zhihu.com/p/595337665) · 知乎 · 2022-12-30 · 赞同 0**
> 力扣：[294. 翻转游戏II](https://leetcode.cn/problems/flip-game-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

294.翻转游戏II

[力扣](https://leetcode.cn/problems/flip-game-ii/)

非常典型的nim游戏问题，最常规的做法就是利用sg函数来进行求解。sg函数简单来说可以认为是基于不同阶后继状态的可融合，对于复杂后继状态的某种优化求解。一个简单的例子就是例如本题中有12个'+'，那么翻转中间的两根，将其转化到4 + 6的模式，那么就必须综合考虑4和6这两种情况的融合，但4和6自身也是有一些可操作空间的，所以需要使用某个办法来表示各个状态对胜负以及先后手的影响。更具体的内容这里就不展开介绍了，但是学习sg函数有关的内容有助于处理后续一系列的类似问题。

具体实现上，对于某个状态state，若其为必败态，那么sg[state] \= 0，否则就枚举其所有的后继状态并使用集合统计起来，集合中未出现的最小自然数就是其对应的sg值。

而对于多个平等的状态，最终结果则是这些状态各自的sg值取异或。

最后附上python代码：

```python
class Solution(object):
    def canWin(self, currentState):
        """
        :type currentState: str
        :rtype: bool
        """

        f = {0: 0, 1: 0}

        def calc(x):
            if x in f:
                return f[x]
            
            mex = set()
            for y in range(x - 1):
                mex.add(calc(y) ^ (calc(x - 2 - y)))
            
            f[x] = 0
            while f[x] in mex:
                f[x] += 1
            return f[x]

        cnt = 0
        res = 0
        for char in currentState:
            if char == '+':
                cnt += 1
            else:
                if cnt > 0:
                    res ^= calc(cnt)
                cnt = 0
        
        if cnt > 0:
            res ^= calc(cnt)

        return res != 0
```
