---
title: "1357. 每隔n个顾客打折"
aliases: ["yiduobo的每日leetcode 1357.每隔n个顾客打折"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/398830608"
zhihu_id: "398830608"
zhihu_title: "yiduobo的每日leetcode 1357.每隔n个顾客打折"
question_id: "1357"
question: "每隔n个顾客打折"
problem_url: "https://leetcode.cn/problems/apply-discount-every-n-orders/"
created: "2021-08-11T22:27:18+08:00"
updated: "2021-08-11T22:27:18+08:00"
upvotes: 1
comments: 0
---

# 1357. 每隔n个顾客打折

> **[yiduobo的每日leetcode 1357.每隔n个顾客打折](https://zhuanlan.zhihu.com/p/398830608) · 知乎 · 2021-08-11 · 赞同 1**
> 力扣：[1357. 每隔n个顾客打折](https://leetcode.cn/problems/apply-discount-every-n-orders/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1357.每隔n个顾客打折

[力扣](https://leetcode-cn.com/problems/apply-discount-every-n-orders/)

比较基础的题目，按照题目意思计算每个顾客的花销，并统计当前是第几个顾客。每到第n个顾客时，并打折然后重置计数器。

最后附上python代码：

```python
class Cashier(object):

    def __init__(self, n, discount, products, prices):
        """
        :type n: int
        :type discount: int
        :type products: List[int]
        :type prices: List[int]
        """

        l = len(products)
        self.price_list = [0] * 201
        for index in range(l):
            self.price_list[products[index]] = prices[index]
        self.cnt = 0
        self.discount = discount
        self.n = n

    def getBill(self, product, amount):
        """
        :type product: List[int]
        :type amount: List[int]
        :rtype: float
        """
        
        res = 0
        for index in range(len(product)):
            res += self.price_list[product[index]] * amount[index]
        
        self.cnt += 1
        if self.cnt == self.n:
            res *= 1 - self.discount * 1.0 / 100
            self.cnt = 0
        
        return res

# Your Cashier object will be instantiated and called as such:
# obj = Cashier(n, discount, products, prices)
# param_1 = obj.getBill(product,amount)
```
