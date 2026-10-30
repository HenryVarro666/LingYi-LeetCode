---
title: "3522. 执行指令后的得分"
aliases: ["yiduobo的每日leetcode 3522.执行指令后的得分"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1902566794390143067"
zhihu_id: "1902566794390143067"
zhihu_title: "yiduobo的每日leetcode 3522.执行指令后的得分"
question_id: "3522"
question: "执行指令后的得分"
problem_url: "https://leetcode.cn/problems/calculate-score-after-performing-instructions/"
difficulty: "Medium"
created: "2025-05-09T22:07:08+08:00"
updated: "2025-05-09T22:07:08+08:00"
upvotes: 2
comments: 0
---

# 3522. 执行指令后的得分

> **[yiduobo的每日leetcode 3522.执行指令后的得分](https://zhuanlan.zhihu.com/p/1902566794390143067) · 知乎 · 2025-05-09 · 赞同 2**
> 力扣：[3522. 执行指令后的得分](https://leetcode.cn/problems/calculate-score-after-performing-instructions/) · Medium · 灵茶山艾府：[两种写法：vis 数组标记 / 原地修改（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3522.执行指令后的得分

[3522. 执行指令后的得分 - 力扣（LeetCode）](https://leetcode.cn/problems/calculate-score-after-performing-instructions/description/)

题目给出两个数组instructions和values，两个数组的长度都为n。

接下来需要根据一下规则模拟一个过程：

1、从下标index \= 0开始执行指令，初始得分为0

2、若instructions[index]为'add'，那么就将values[index]累加到得分当中，然后移动到下一个指令index + 1

3、若instructions[index]为'jump'，那么就跳转到index + values[index]，但是不修改得分

若某一时刻下标超出数组边界，或者来到了之前已经执行过的指令，那么就停止上面的过程。

问最终的得分是多少。

题目的描述很清晰，直接按照描述执行模拟就行了。另外根据停止条件，需要使用一个集合记录已经处理过的指令下标。具体来说，初始化访问下标集合vis为空，同时初始化下标now和得分res为0，然后开始模拟。若instructions[now]是jump，就将values[now]累积到now中，否则将values[now]累加到res中，然后将now加上1。重复此过程直到now越界，或者出现在vis中为止。

最后附上python代码：

```python
class Solution(object):
    def calculateScore(self, instructions, values):
        """
        :type instructions: List[str]
        :type values: List[int]
        :rtype: int
        """
        
        vis = set()
        res = 0
        now = 0
        while 0 <= now < len(instructions) and now not in vis:
            vis.add(now)
            if instructions[now] == 'jump':
                now += values[now]
            else:
                res += values[now]
                now += 1
        
        return res
```
