---
title: "4056. 统计相交区间对I & 4057. 统计相交区间对II"
aliases: ["yiduobo的每日leetcode 4056.统计相交区间对I && 4057.统计相交区间对II", "4056. 统计相交区间对I", "4057. 统计相交区间对II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/two-pointers", "leetcode/sorting", "leetcode/medium", "leetcode/binary-search"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2085170177138861438"
zhihu_id: "2085170177138861438"
zhihu_title: "yiduobo的每日leetcode 4056.统计相交区间对I && 4057.统计相交区间对II"
question_id: ["4056", "4057"]
question: ["统计相交区间对 I", "统计相交区间对 II"]
problem_url: ["https://leetcode.cn/problems/number-of-intersecting-interval-pairs-i/", "https://leetcode.cn/problems/number-of-intersecting-interval-pairs-ii/"]
difficulty: ["Easy", "Medium"]
created: "2026-09-21T01:10:31+08:00"
updated: "2026-09-21T01:10:43+08:00"
upvotes: 2
comments: 0
---

# 4056. 统计相交区间对I & 4057. 统计相交区间对II

> **[yiduobo的每日leetcode 4056.统计相交区间对I && 4057.统计相交区间对II](https://zhuanlan.zhihu.com/p/2085170177138861438) · 知乎 · 2026-09-21 · 赞同 2**
> 力扣：[4056. 统计相交区间对 I](https://leetcode.cn/problems/number-of-intersecting-interval-pairs-i/) · Easy · 灵茶山艾府：[非暴力做法（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[4057. 统计相交区间对 II](https://leetcode.cn/problems/number-of-intersecting-interval-pairs-ii/) · Medium · 灵茶山艾府：[两种方法：排序 + 二分/双指针（Python/Java/C++/Go）](../4057%20统计相交区间对%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4056.统计相交区间对I

<https://leetcode.cn/problems/number-of-intersecting-interval-pairs-i/>

4057.统计相交区间对II

<https://leetcode.cn/problems/number-of-intersecting-interval-pairs-ii/description/>

题目给出一个包含n个元素的二维整数数组intervals，其中intervals\[index\] \= \[start\[index\], end\[index\]\]，表示从start\[index\]到end\[index\]的闭区间。

要求相交的区间对数量，若两个区间至少有一个公共点，则称二者相交，仅共享一个端点的情况也算作相交。

第二题的数据规模较大，n可达10^5。

题目需要计算所有相交的区间对数量，那么在这里就可以针对每个区间，统计其左侧有多少个区间与其相交，这样就可以做到不重不漏。

而对于一个区间[x, y]，其左侧区间如果与之相交，唯一需要满足的条件就是左侧区间的终点大于等于x，换句话说，就是这些区间目前还没有关闭。

基于这一点，就可以将所有区间的起点和终点都收集起来，按照位置为第一关键字从小到大，起点在前终点在后为第二关键字进行排序，接下来遍历这些点，并使用一个变量cnt记录目前尚未关闭的区间。

对于一个点p：

1、若其为区间起点，那么就需要先检测这个区间与左侧有多少个区间相交。根据定义，此时尚未关闭的区间都与其相交，一共就是cnt个，因此需要将cnt累加到答案中。接下来，由于当前区间是一个新的尚未关闭的区间，因此还需要将cnt再加上1

2、若其为区间终点，则说明有一个区间关闭了，此时将cnt减1即可

最后附上python代码：

```python
class Solution(object):
    def countIntersectingIntervals(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: int
        """
        
        points = []
        for x, y in intervals:
            points.append((x, 0))
            points.append((y, 1))
        
        points.sort()
        cnt = 0
        res = 0
        for p, t in points:
            if t == 0:
                res += cnt
                cnt += 1
            else:
                cnt -= 1
        
        return res
```
