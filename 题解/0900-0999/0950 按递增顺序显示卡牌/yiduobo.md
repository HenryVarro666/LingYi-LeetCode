---
title: "950. 按递增顺序显示卡牌"
aliases: ["yiduobo的每日leetcode 950.按递增顺序显示卡牌"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/359679671"
zhihu_id: "359679671"
zhihu_title: "yiduobo的每日leetcode 950.按递增顺序显示卡牌"
question_id: "950"
question: "按递增顺序显示卡牌"
problem_url: "https://leetcode.cn/problems/reveal-cards-in-increasing-order/"
created: "2021-03-24T23:20:17+08:00"
updated: "2021-03-24T23:20:17+08:00"
upvotes: 1
comments: 0
---

# 950. 按递增顺序显示卡牌

> **[yiduobo的每日leetcode 950.按递增顺序显示卡牌](https://zhuanlan.zhihu.com/p/359679671) · 知乎 · 2021-03-24 · 赞同 1**
> 力扣：[950. 按递增顺序显示卡牌](https://leetcode.cn/problems/reveal-cards-in-increasing-order/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

950.按递增顺序现实卡牌

[力扣](https://leetcode-cn.com/problems/reveal-cards-in-increasing-order/)

直接正向构造是比较复杂的，那么可以先看看能否反向构造，即从后往前看，逐个将当前的最大值对应的卡牌加入到牌组当中。

观察样例，首先：

1、插入最大值[17]

2、此时要插入当前最大值13，得到[13, 17]，但具体插入的方法还无法确定，但可以明确的一点是每轮新插入的卡牌必然是插入在卡组头部的

3、此时要插入当前最大值11，从[13, 17]变为[11, 17, 13]，插入方式任然无法确定

4、此时要插入当前最大值7，从[11, 17, 13]变为[7, 13, 11, 17]。此时可以发现，每一轮就是将上一轮的卡组末尾重新插入到卡组头部，然后将当前要插入的卡牌再插入到卡组头部

验证后续的5、3、2都满足这一假设。更一般的，如果从题目给出的执行操作出发也可以得出该结论。不妨设当前的卡组为AB[XX...X]，那么执行操作之后得到的是A展示，然后B移动到卡组末尾，那么此时的卡组就变成了[XX...X]B。换言之，从[XX...X]B倒推加入A的情况就应该将B移动到卡组头部，然后在卡组头部再插入A。

此时，就得到了一种构造的方法，可以按照数值从大到小排序，然后再逐个将卡牌按上述构造方法插入到卡组当中。由于这里卡组头尾都有插入删除，因此可以使用双向队列来做。不过注意到如果倒着看卡组的头尾，每一轮构造也可以认为是将队列头部移动到队列尾部，然后在队列尾部插入当前最大值，于是可以只是用普通的队列，然后维护一个队列头部的下标。

最后附上python代码：

```python
class Solution(object):
    def deckRevealedIncreasing(self, deck):
        """
        :type deck: List[int]
        :rtype: List[int]
        """

        sorted_deck = sorted(deck, reverse=True)
        q = [sorted_deck[0]]
        l = 0
        for num in sorted_deck[1:]:
            q.append(q[l])
            q.append(num)
            l += 1
        
        return q[l:][::-1]
```
