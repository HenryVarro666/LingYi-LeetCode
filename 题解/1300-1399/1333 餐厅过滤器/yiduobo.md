---
title: "1333. 餐厅过滤器"
aliases: ["yiduobo的每日leetcode 1333.餐厅过滤器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/395227816"
zhihu_id: "395227816"
zhihu_title: "yiduobo的每日leetcode 1333.餐厅过滤器"
question_id: "1333"
question: "餐厅过滤器"
problem_url: "https://leetcode.cn/problems/filter-restaurants-by-vegan-friendly-price-and-distance/"
created: "2021-08-01T19:49:52+08:00"
updated: "2021-08-01T19:49:52+08:00"
upvotes: 0
comments: 0
---

# 1333. 餐厅过滤器

> **[yiduobo的每日leetcode 1333.餐厅过滤器](https://zhuanlan.zhihu.com/p/395227816) · 知乎 · 2021-08-01 · 赞同 0**
> 力扣：[1333. 餐厅过滤器](https://leetcode.cn/problems/filter-restaurants-by-vegan-friendly-price-and-distance/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1333.餐厅过滤器

[力扣](https://leetcode-cn.com/problems/filter-restaurants-by-vegan-friendly-price-and-distance/)

题目描述和输入都是一大堆，但是理清楚之后实际上是很容易的题目。

首先一趟扫描，按照素食友好、价格以及距离筛选出候选餐厅，并将其对应的rating和id加入到候选数组candidate当中，接下来按照rating为第一关键字，id为第二关键字对candidate排序后输出对应餐厅的id即可。

最后附上python代码：

```python
class Solution(object):
    def filterRestaurants(self, restaurants, veganFriendly, maxPrice, maxDistance):
        """
        :type restaurants: List[List[int]]
        :type veganFriendly: int
        :type maxPrice: int
        :type maxDistance: int
        :rtype: List[int]
        """

        candidate = []
        for id, r, v, p, d in restaurants:
            if veganFriendly and not v:
                continue
            if p > maxPrice:
                continue
            if d > maxDistance:
                continue
            candidate.append([r, id])
        
        return [x[1] for x in sorted(candidate, key=lambda d:(-d[0], -d[1]))]
```
