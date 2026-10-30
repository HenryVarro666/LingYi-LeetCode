---
title: "2043. 简易银行系统"
aliases: ["yiduobo的每日leetcode 2043.简易银行系统"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/design", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/510390913"
zhihu_id: "510390913"
zhihu_title: "yiduobo的每日leetcode 2043.简易银行系统"
question_id: "2043"
question: "简易银行系统"
problem_url: "https://leetcode.cn/problems/simple-bank-system/"
difficulty: "Medium"
created: "2022-05-06T21:18:20+08:00"
updated: "2022-05-06T21:18:20+08:00"
upvotes: 0
comments: 0
---

# 2043. 简易银行系统

> **[yiduobo的每日leetcode 2043.简易银行系统](https://zhuanlan.zhihu.com/p/510390913) · 知乎 · 2022-05-06 · 赞同 0**
> 力扣：[2043. 简易银行系统](https://leetcode.cn/problems/simple-bank-system/) · Medium · 灵茶山艾府：[题目怎么说，我们就怎么做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2043.简易银行系统

[力扣](https://leetcode-cn.com/problems/simple-bank-system/)

确实是挺简易的。。只需要使用一个dict记录每个用户当前的存款数即可。

对于题目中的三种操作，首先需要判断操作的账号是否在1到n之间，接下来需要判断出钱的这一方账户里面是否有足够的钱。如果都没问题，那么就执行对应的操作。

最后附上python代码：

```python
class Bank(object):

    def __init__(self, balance):
        """
        :type balance: List[int]
        """
        self.balance = balance[:]

    def transfer(self, account1, account2, money):
        """
        :type account1: int
        :type account2: int
        :type money: int
        :rtype: bool
        """
        if account1 < 1 or account1 > len(self.balance):
            return False
        if account2 < 1 or account2 > len(self.balance):
            return False
        if self.balance[account1 - 1] < money:
            return False
        
        self.balance[account1 - 1] -= money
        self.balance[account2 - 1] += money
        return True

    def deposit(self, account, money):
        """
        :type account: int
        :type money: int
        :rtype: bool
        """
        if account < 0 or account > len(self.balance):
            return False
        
        self.balance[account - 1] += money
        return True

    def withdraw(self, account, money):
        """
        :type account: int
        :type money: int
        :rtype: bool
        """
        if account < 0 or account > len(self.balance):
            return False
        if self.balance[account - 1] < money:
            return False
        
        self.balance[account - 1] -= money
        return True

# Your Bank object will be instantiated and called as such:
# obj = Bank(balance)
# param_1 = obj.transfer(account1,account2,money)
# param_2 = obj.deposit(account,money)
# param_3 = obj.withdraw(account,money)
```
