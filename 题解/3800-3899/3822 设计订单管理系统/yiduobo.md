---
title: "3822. 设计订单管理系统"
aliases: ["yiduobo的每日leetcode 3822.设计订单管理系统"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2001433720310210684"
zhihu_id: "2001433720310210684"
zhihu_title: "yiduobo的每日leetcode 3822.设计订单管理系统"
question_id: "3822"
question: "设计订单管理系统"
problem_url: "https://leetcode.cn/problems/design-order-management-system/"
created: "2026-02-01T23:25:22+08:00"
updated: "2026-02-01T23:25:22+08:00"
upvotes: 2
comments: 0
---

# 3822. 设计订单管理系统

> **[yiduobo的每日leetcode 3822.设计订单管理系统](https://zhuanlan.zhihu.com/p/2001433720310210684) · 知乎 · 2026-02-01 · 赞同 2**
> 力扣：[3822. 设计订单管理系统](https://leetcode.cn/problems/design-order-management-system/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3822.设计订单管理系统

<https://leetcode.cn/problems/design-order-management-system/description/>

题目要求设计一个简单的交易平台订单管理系统。

每个订单都有一个关联的orderId，一个orderType("buy"或"sell")，以及一个price。

如果订单没有被取消，那么就会被认为是有效的。

要求实现OrderManagementSystem类：

- OrderManagementSystem()：初始化订单管理系统
- void addOrder(int orderId, string orderType, int price)：添加一个具有给定属性的新有效订单。保证orderId互不相同
- void modifyOrder(int orderId, int newPrice)：修改现有订单的价格。保证该订单存在且有效
- void cancelOrder(int orderId)：取消一个现有的订单。保证该订单存在且有效
- vector\<int> getOrdersAtPrice(string orderType, int price)：返回所有匹配给定orderType以及price的有效订单的orderId。若不存在此类订单，则返回空列表

题目保证所有操作的总次数不超过2000次。

由于题目保证所有操作的次数不超过2000次，因此在这里使用一个O(n^2)的算法就足够了，于是只需使用一个数组orders记录所有的订单。每个订单可以通过长度为3的子数组表示，即[orderId, orderType, price]。对于每种操作：

- addOrder：新增一个子数组，添加到orders末尾
- modifyOrder：遍历orders，找出orderId对应的子数组，然后修改对应的价格
- cancelOrder：遍历orders，找出orderId对应的子数组在orders中的下标，然后pop掉
- getOrdersAtPrice：遍历orders，找出orderType与price匹配的所有订单，将对应的orderId加入答案中

最后附上python代码：

```python
class OrderManagementSystem(object):

    def __init__(self):
        self.orders = []

    def addOrder(self, orderId, orderType, price):
        """
        :type orderId: int
        :type orderType: str
        :type price: int
        :rtype: None
        """
        self.orders.append([orderId, orderType, price])

    def modifyOrder(self, orderId, newPrice):
        """
        :type orderId: int
        :type newPrice: int
        :rtype: None
        """
        for index in range(len(self.orders)):
            if self.orders[index][0] == orderId:
                self.orders[index][2] = newPrice
                break

    def cancelOrder(self, orderId):
        """
        :type orderId: int
        :rtype: None
        """
        for index in range(len(self.orders)):
            if self.orders[index][0] == orderId:
                break
        self.orders.pop(index)

    def getOrdersAtPrice(self, orderType, price):
        """
        :type orderType: str
        :type price: int
        :rtype: List[int]
        """
        res = []
        for index in range(len(self.orders)):
            if self.orders[index][1] == orderType and self.orders[index][2] == price:
                res.append(self.orders[index][0])
        
        return res

# Your OrderManagementSystem object will be instantiated and called as such:
# obj = OrderManagementSystem()
# obj.addOrder(orderId,orderType,price)
# obj.modifyOrder(orderId,newPrice)
# obj.cancelOrder(orderId)
# param_4 = obj.getOrdersAtPrice(orderType,price)
```
