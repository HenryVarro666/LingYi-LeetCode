---
title: "293. 翻转游戏"
aliases: ["yiduobo的每日leetcode 293.翻转游戏"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/595180961"
zhihu_id: "595180961"
zhihu_title: "yiduobo的每日leetcode 293.翻转游戏"
question_id: "293"
question: "翻转游戏"
problem_url: "https://leetcode.cn/problems/flip-game/"
created: "2022-12-29T14:16:58+08:00"
updated: "2022-12-29T14:16:58+08:00"
upvotes: 0
comments: 0
---

# 293. 翻转游戏

> **[yiduobo的每日leetcode 293.翻转游戏](https://zhuanlan.zhihu.com/p/595180961) · 知乎 · 2022-12-29 · 赞同 0**
> 力扣：[293. 翻转游戏](https://leetcode.cn/problems/flip-game/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

293.翻转游戏

[力扣](https://leetcode.cn/problems/flip-game/)

题目只要求找出一次操作后的字符串，那么只需一趟遍历，找出连续出现两次的加号，将其替换成减号后加入到答案数组中即可。

最后附上python代码：

```python
class Solution(object):
    def generatePossibleNextMoves(self, currentState):
        """
        :type currentState: str
        :rtype: List[str]
        """

        res = []
        n = len(currentState)
        for index in range(n - 1):
            if currentState[index] == currentState[index + 1] == '+':
                res.append(currentState[:index] + '--' + currentState[index + 2:])
        
        return res
```
