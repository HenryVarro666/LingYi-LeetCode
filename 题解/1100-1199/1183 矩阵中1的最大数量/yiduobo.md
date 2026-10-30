---
title: "1183. 矩阵中1的最大数量"
aliases: ["yiduobo的每日leetcode 1183.矩阵中1的最大数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/612446778"
zhihu_id: "612446778"
zhihu_title: "yiduobo的每日leetcode 1183.矩阵中1的最大数量"
question_id: "1183"
question: "矩阵中1的最大数量"
problem_url: "https://leetcode.cn/problems/maximum-number-of-ones/"
created: "2023-03-08T23:18:45+08:00"
updated: "2023-03-08T23:18:45+08:00"
upvotes: 0
comments: 0
---

# 1183. 矩阵中1的最大数量

> **[yiduobo的每日leetcode 1183.矩阵中1的最大数量](https://zhuanlan.zhihu.com/p/612446778) · 知乎 · 2023-03-08 · 赞同 0**
> 力扣：[1183. 矩阵中1的最大数量](https://leetcode.cn/problems/maximum-number-of-ones/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1183.矩阵中1的最大数量

[力扣](https://leetcode.cn/problems/maximum-number-of-ones/)

直接设计填充方案是比较困难的，不妨先进行一些分割。

方便起见，下面用s来表示正方形边长sideLength。

注意到题目要求任何s \* s的正方形中的1的数量为maxOnes，那么不妨从左上角开始逐个分割大小为s \* s的正方形。令m \= width / s，n \= h / s，一共可以分割的正方形数量就是m \* n个，因此可以先将m \* n \* maxOnes累加到答案中。

接下俩，矩形中还会剩下三个部分：

1、右侧的一共n个矩形，这些矩形的宽w \= width % s，高为s

2、下方的一共m个矩形，这些矩形的高h \= height % s，宽为s

3、右下角的一个矩形，这个矩形的高h \= height % s，宽w \= width % s

更一般的，3中的矩形也被包含在1和2中的所有矩形，因此可以将这些矩形视为

a）右侧的一共n个矩形，这些矩形宽为w \= width % s，高为s - h \= s - height % s

b）下方的一共m个矩形，这些矩形宽为s - w \= s - width % s，高为h \= height % s

c）右侧n个、下方m个、右下角的1个，共m + n + 1个矩形，这些矩形宽为w \= width % s，高h \= height % s

由于一开始划分出去的m \* n个小正方形中的1的数量是固定的，为了使得最终答案最大，就需要尽量在多出来的这些矩形中填充1。很明显，应该先填充c中的矩形，然后根据m和n的大小关系，决定接下来填充a还是b的矩形。

具体来说：

a）对于情况a中的n个矩形，若此时还可用的1的数量，也就是maxOnes \<\= (s - h) \* w，那么此时的1不够填充这种矩形。此时只需将n \* maxOnes累加到答案中并返回，否则就需要将n \* (s - h) \* w累加到答案中，同时将maxOnes减去(s - h) \* w

b）对于情况b中的m个矩形，若此时还可用的1的数量，也就是maxOnes \<\= (s - w) \* h，那么此时的1不够填充这种矩形。此时只需将m \* maxOnes累加到答案中并返回，否则就需要将m \* (s - w) \* h累加到答案中，同时将maxOnes减去(s - w) \* h

c）对于情况c中的(m + n + 1)个矩形，若此时还可用的1的数量，也就是maxOnes \<\= w \* h，那么此时的1不够填充这种矩形。此时只需将(m + n + 1) \* maxOnes累加到答案中并返回，否则就需要将(m + n + 1) \* w \* h累加到答案中，同时将maxOnes减去w \* h

对于上面这三种矩形，优先处理c中的矩形，接下来对于剩下的maxOnes，若n > m，那么优先处理a中的矩形，再处理b中的矩形，反之就需要优先处理b中的矩形，再处理a中的矩形。

最后附上python代码：

```python
class Solution(object):
    def maximumNumberOfOnes(self, width, height, sideLength, maxOnes):
        """
        :type width: int
        :type height: int
        :type sideLength: int
        :type maxOnes: int
        :rtype: int
        """

        m = width / sideLength
        w = width % sideLength

        n = height / sideLength
        h = height % sideLength

        res = m * n * maxOnes

        if h * w >= maxOnes:
            res += (m + n + 1) * maxOnes
        else:
            res += (m + n + 1) * (w * h)
            maxOnes -= w * h
            if m < n:
                if (sideLength - h) * w >= maxOnes:
                    res += n * maxOnes
                else:
                    res += n * (sideLength - h) * w
                    maxOnes -= (sideLength - h) * w
                    if (sideLength - w) * h >= maxOnes:
                        res += m * maxOnes
                    else:
                        res += m * (sideLength - w) * h
            
            else:
                if (sideLength - w) * h >= maxOnes:
                    res += m * maxOnes
                else:
                    res += m * (sideLength - w) * h
                    maxOnes -= (sideLength - w) * h
                    if (sideLength - h) * w >= maxOnes:
                        res += n * maxOnes
                    else:
                        res += n * (sideLength - h) * w
        
        return res
```
