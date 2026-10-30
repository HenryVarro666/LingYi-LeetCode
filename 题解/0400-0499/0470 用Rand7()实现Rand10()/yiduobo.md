---
title: "470. 用Rand7()实现Rand10()"
aliases: ["yiduobo的每日leetcode 470.用Rand7()实现Rand10()"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/231995367"
zhihu_id: "231995367"
zhihu_title: "yiduobo的每日leetcode 470.用Rand7()实现Rand10()"
question_id: "470"
question: "用Rand7()实现Rand10()"
problem_url: "https://leetcode.cn/problems/implement-rand10-using-rand7/"
created: "2020-09-10T18:13:05+08:00"
updated: "2020-09-10T18:13:05+08:00"
upvotes: 1
comments: 0
---

# 470. 用Rand7()实现Rand10()

> **[yiduobo的每日leetcode 470.用Rand7()实现Rand10()](https://zhuanlan.zhihu.com/p/231995367) · 知乎 · 2020-09-10 · 赞同 1**
> 力扣：[470. 用Rand7()实现Rand10()](https://leetcode.cn/problems/implement-rand10-using-rand7/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

470.用Rand()实现Rand10() <https://leetcode-cn.com/problems/implement-rand10-using-rand7/>

经典的拒绝采样的题目，在这里连续调用两次Rand7()，那么一共有7 \* 7 \= 49种可能性。我们可以取其中的40种可能，分配给rand10()的10种可能。若恰好遇到剩下的9种可能，那么就再连续调用两次Rand7()。

最后附上python代码：

```python
# The rand7() API is already defined for you.
# def rand7():
# @return a random integer in the range 1 to 7

class Solution(object):
    def rand10(self):
        """
        :rtype: int
        """

        while True:
            tmp = (rand7() - 1) * 7 + rand7()
            if tmp <= 40:
                return (tmp - 1) / 4 + 1
```
