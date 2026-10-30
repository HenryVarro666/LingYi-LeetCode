---
title: "2158. 每天绘制新区域的数量"
aliases: ["yiduobo的每日leetcode 2158.每天绘制新区域的数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/627123333"
zhihu_id: "627123333"
zhihu_title: "yiduobo的每日leetcode 2158.每天绘制新区域的数量"
question_id: "2158"
question: "每天绘制新区域的数量"
problem_url: "https://leetcode.cn/problems/amount-of-new-area-painted-each-day/"
created: "2023-05-06T01:42:42+08:00"
updated: "2023-05-06T01:42:42+08:00"
upvotes: 0
comments: 0
---

# 2158. 每天绘制新区域的数量

> **[yiduobo的每日leetcode 2158.每天绘制新区域的数量](https://zhuanlan.zhihu.com/p/627123333) · 知乎 · 2023-05-06 · 赞同 0**
> 力扣：[2158. 每天绘制新区域的数量](https://leetcode.cn/problems/amount-of-new-area-painted-each-day/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2158.每天绘制新区域的数量

[力扣](https://leetcode.cn/problems/amount-of-new-area-painted-each-day/)

题目按顺序给出一系列区间，要求：

1、求出当前区间中已经被填充的格子数量，并返回区间长度减去这个数量

2、将当前区间全部填充

由于本题是区间填充，而不是区间叠加加减，因此不太方便使用树状数组，所以我在这里选择使用线段树来求解。题目中的两种操作实际上就是区间和以及区间赋值操作，另外，由于一旦某个区间被填充后，后续的所有操作都无法影响到该区间，因此在具体处理时可以利用区间和以及区间长度很方便地实现区间填充。

最后附上python代码：

```python
class Solution(object):
    def amountPainted(self, paint):
        """
        :type paint: List[List[int]]
        :rtype: List[int]
        """

        def get(now, left, right, start, end):
            if s[now] == right - left + 1:
                return end - start + 1
            
            if left == start and right == end:
                return s[now]
            
            mid = (left + right) >> 1
            if end <= mid:
                return get(now + now + 1, left, mid, start, end)
            elif start > mid:
                return get(now + now + 2, mid + 1, right, start, end)
            else:
                return get(now + now + 1, left, mid, start, mid) + get(now + now + 2, mid + 1, right, mid + 1, end)
        
        def add(now, left, right, start, end):
            if s[now] == right - left + 1:
                return

            if left == start and right == end:
                s[now] = right - left + 1
                return
            
            mid = (left + right) >> 1
            if end <= mid:
                add(now + now + 1, left, mid, start, end)
            elif start > mid:
                add(now + now + 2, mid + 1, right, start, end)
            else:
                add(now + now + 1, left, mid, start, mid)
                add(now + now + 2, mid + 1, right, mid + 1, end)
            
            s[now] = s[now + now + 1] + s[now + now + 2]

        s = [0] * 131072
        res = []
        for start, end in paint:
            res.append(end - start - get(0, 0, 65535, start, end - 1))
            add(0, 0, 65535, start, end - 1)

        return res
```
