---
title: "1518. 换酒问题"
aliases: ["yiduobo的每日leetcode 1518.换酒问题"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/421196838"
zhihu_id: "421196838"
zhihu_title: "yiduobo的每日leetcode 1518.换酒问题"
question_id: "1518"
question: "换水问题"
problem_url: "https://leetcode.cn/problems/water-bottles/"
difficulty: "Easy"
created: "2021-10-13T23:40:57+08:00"
updated: "2021-10-13T23:40:57+08:00"
upvotes: 0
comments: 0
---

# 1518. 换酒问题

> **[yiduobo的每日leetcode 1518.换酒问题](https://zhuanlan.zhihu.com/p/421196838) · 知乎 · 2021-10-13 · 赞同 0**
> 力扣：[1518. 换水问题](https://leetcode.cn/problems/water-bottles/) · Easy · 灵茶山艾府：[两种方法：模拟 / O(1) 数学公式（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1518.换酒问题

[力扣](https://leetcode-cn.com/problems/water-bottles/)

还以为是经典的脑筋急转弯问题，即手上有numExchange - 1个空瓶子的时候，可以先赊账喝一瓶，然后赊的这个空瓶子加上手上现有的空瓶子恰好凑够numExchange个空瓶子，然后换一瓶正好换这瓶赊的酒。

但是从样例2来看，似乎是不让赊账的，这样的话需要特别注意任意时刻都必须要满足numBottles要大于等于numExchange。

回到问题。每次换酒，都可以视为使用numExchange个瓶子换来了1个瓶子，也就是说损失了numExchange - 1个瓶子。若某一时刻剩下的瓶子小于numExchange，换酒的过程就中止了。当然，开启换酒操作的前提是初始手上酒的数量numBottles大于等于numExchange。

每换一瓶酒都要损失numExchange - 1个瓶子，那么一个自然的想法就是直接用numBottles去除以numExchange - 1来计算可以换到多少瓶酒，但是这样一来就可能出现赊账的情况。一种可行的做法是先预留出numExchange瓶酒不动，对于其他瓶子做上面的除法。这样一来,即使出现numExchange - 1个空瓶子赊账的情况，也可以认为是这里提前预留出来的numExchange瓶酒换来的这一瓶的瓶子提供的额外的瓶子，而不需要赊账。

最后附上python代码：

```python
class Solution(object):
    def numWaterBottles(self, numBottles, numExchange):
        """
        :type numBottles: int
        :type numExchange: int
        :rtype: int
        """

        res = numBottles
        if numBottles >= numExchange:
            res += (numBottles - numExchange) / (numExchange - 1) + 1
        
        return res
```
