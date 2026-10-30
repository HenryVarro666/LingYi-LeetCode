---
title: "2241. 设计一个ATM机器"
aliases: ["yiduobo的每日leetcode 2241.设计一个ATM机器"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/design", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/545403312"
zhihu_id: "545403312"
zhihu_title: "yiduobo的每日leetcode 2241.设计一个ATM机器"
question_id: "2241"
question: "设计一个 ATM 机器"
problem_url: "https://leetcode.cn/problems/design-an-atm-machine/"
difficulty: "Medium"
created: "2022-07-24T00:55:33+08:00"
updated: "2022-07-24T00:55:33+08:00"
upvotes: 0
comments: 0
---

# 2241. 设计一个ATM机器

> **[yiduobo的每日leetcode 2241.设计一个ATM机器](https://zhuanlan.zhihu.com/p/545403312) · 知乎 · 2022-07-24 · 赞同 0**
> 力扣：[2241. 设计一个 ATM 机器](https://leetcode.cn/problems/design-an-atm-machine/) · Medium · 灵茶山艾府：[模拟（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2241.设计一个ATM机器

[力扣](https://leetcode.cn/problems/design-an-atm-machine/)

题目需要实现存钱和取钱两种功能。

对于存钱操作，使用一个list记录当前机器里每个种类钞票的数量就行了。

对于取钱操作，按照题目描述是使用的贪心法一步步执行就好了，样例中取不出钱的例子也从说明了当物品权重没有倍数关系时是不能使用贪心法求解背包问题的。

最后附上python代码：

```python
class ATM(object):

    def __init__(self):
        self.cnt_list = [0] * 5
        self.v = [20, 50, 100, 200, 500]

    def deposit(self, banknotesCount):
        """
        :type banknotesCount: List[int]
        :rtype: None
        """
        for index, cnt in enumerate(banknotesCount):
            self.cnt_list[index] += cnt

    def withdraw(self, amount):
        """
        :type amount: int
        :rtype: List[int]
        """
        res = [0] * 5
        for index in range(4, -1, -1):
            res[index] = amount / self.v[index]
            if res[index] > self.cnt_list[index]:
                res[index] = self.cnt_list[index]
            amount -= res[index] * self.v[index]
        
        if amount != 0:
            return [-1]
        
        for index in range(5):
            self.cnt_list[index] -= res[index]
        return res

# Your ATM object will be instantiated and called as such:
# obj = ATM()
# obj.deposit(banknotesCount)
# param_2 = obj.withdraw(amount)
```
