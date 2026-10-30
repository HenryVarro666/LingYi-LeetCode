---
title: "2293. 极大极小游戏"
aliases: ["yiduobo的每日leetcode 2293.极大极小游戏"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/553380349"
zhihu_id: "553380349"
zhihu_title: "yiduobo的每日leetcode 2293.极大极小游戏"
question_id: "2293"
question: "极大极小游戏"
problem_url: "https://leetcode.cn/problems/min-max-game/"
difficulty: "Easy"
created: "2022-08-13T15:10:14+08:00"
updated: "2022-08-13T15:10:14+08:00"
upvotes: 0
comments: 0
---

# 2293. 极大极小游戏

> **[yiduobo的每日leetcode 2293.极大极小游戏](https://zhuanlan.zhihu.com/p/553380349) · 知乎 · 2022-08-13 · 赞同 0**
> 力扣：[2293. 极大极小游戏](https://leetcode.cn/problems/min-max-game/) · Easy · 灵茶山艾府：[Go 模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2293.极大极小游戏

[力扣](https://leetcode.cn/problems/min-max-game/)

由于题目给出的数组长度较小，同时按照题目描述的过程来看，每一轮都将缩小一半的数据规模，因此可以直接按照题目描述的过程模拟每一轮的操作，直到找出最终答案为止。

最后附上python代码：

```python
class Solution(object):
    def minMaxGame(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        now = nums[:]
        while len(now) > 1:
            next = []
            for index in range(len(now) / 2):
                if index % 2 == 0:
                    next.append(min(now[index * 2], now[index * 2 + 1]))
                else:
                    next.append(max(now[index * 2], now[index * 2 + 1]))
            
            now = next[:]
        
        return now[0]
```
