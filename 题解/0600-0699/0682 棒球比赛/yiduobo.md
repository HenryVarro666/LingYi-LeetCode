---
title: "682. 棒球比赛"
aliases: ["yiduobo的每日leetcode 682.棒球比赛"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/stack", "leetcode/array", "leetcode/simulation", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/303230419"
zhihu_id: "303230419"
zhihu_title: "yiduobo的每日leetcode 682.棒球比赛"
question_id: "682"
question: "棒球比赛"
problem_url: "https://leetcode.cn/problems/baseball-game/"
difficulty: "Easy"
created: "2020-11-20T22:20:00+08:00"
updated: "2020-11-20T22:20:00+08:00"
upvotes: 0
comments: 0
---

# 682. 棒球比赛

> **[yiduobo的每日leetcode 682.棒球比赛](https://zhuanlan.zhihu.com/p/303230419) · 知乎 · 2020-11-20 · 赞同 0**
> 力扣：[682. 棒球比赛](https://leetcode.cn/problems/baseball-game/) · Easy · 灵茶山艾府：[用列表模拟（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

682.棒球比赛

[力扣](https://leetcode-cn.com/problems/baseball-game/)

注意到题目中的所有特殊操作都跟最近的一次或者两次得分有关，因此很自然就想到使用栈来维护得分的序列，而特殊操作则通过操作栈顶元素来完成。

最后附上python代码：

```python
class Solution(object):
    def calPoints(self, ops):
        """
        :type ops: List[str]
        :rtype: int
        """

        stack = []
        for op in ops:
            if op == 'C':
                stack.pop()
            elif op == 'D':
                stack.append(stack[-1] * 2)
            elif op == '+':
                stack.append(stack[-1] + stack[-2])
            else:
                stack.append(int(op))
        
        return sum(stack)
```
