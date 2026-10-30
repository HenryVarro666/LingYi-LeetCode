---
title: "986. 区间列表的交集"
aliases: ["yiduobo的每日leetcode 986.区间列表的交集"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/363945049"
zhihu_id: "363945049"
zhihu_title: "yiduobo的每日leetcode 986.区间列表的交集"
question_id: "986"
question: "区间列表的交集"
problem_url: "https://leetcode.cn/problems/interval-list-intersections/"
created: "2021-04-11T15:01:29+08:00"
updated: "2021-04-11T15:01:29+08:00"
upvotes: 0
comments: 0
---

# 986. 区间列表的交集

> **[yiduobo的每日leetcode 986.区间列表的交集](https://zhuanlan.zhihu.com/p/363945049) · 知乎 · 2021-04-11 · 赞同 0**
> 力扣：[986. 区间列表的交集](https://leetcode.cn/problems/interval-list-intersections/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

986.区间列表的交集

[力扣](https://leetcode-cn.com/problems/interval-list-intersections/)

首先我们先来看看如何判断两个区间相交，不妨设这两个区间分别为[x1, y1]，[x2, y2]：

1、当x1 \< x2时:

1-1）若此时有y1 \< x2，那么两个区间不相交

1-2）若此时有x2 \<\= y1 \< y2，那么两个区间相交的部分为[x2, y1]

1-3）若此时有y1 >\= y2，那么两个区间相交的部分为[x2, y2]

综合起来，设min_y \= min(y1, y2)，那么当min_y >\= x2时，相交区间为[x2, min_y]，否则不相交

2、当x1 \= x2时：

2-1）若此时有y1 \< y2，那么两个区间相交的部分为[x1, y1]

2-2）若此时有y1 >\= y2，那么两个区间相交的部分为[x1, y2]

综合起来，设min_y \= min(y1, y2)，那么相交区间为[x1, min_y]

3、当x2 \< x1 \< y2时：

3-1）若此时有y1 \< y2，那么两个区间相交的部分为[x1, y1]

3-2）若此时有y1 >\= y2，那么两个区间相交的部分为[x1, y2]

综合起来，设min_y \= min(y1, y2)，那么相交区间为[x1, min_y]

4、当x1 >\= y2时：

此时只有当x1 \= y2时两个区间会相交于x1，因此相交的部分为[x1, y2]

可以发现，以上每种情况中，设max_x \= max(x1, y2)，那么只有当max_x \<\= min_y时会产生相交，区间恰好就是[max_x， min_y]

接下来，我们就可以利用上面的结论来计算A和B中区间的相交情况。最朴素的做法自然是两两枚举然后进行判断，但是注意到这里的区间已经排序，那么有些性质可以加以利用。

不妨设当前处理到A的第i个区间以及B的第j个区间，那么：

1、若Ay[i] \< By[j]，由于后续的Bx[j + 1]、Bx[j + 2]、...、Bx[-1]都必然大于By[j]，因此也会大于Ay[i]，那么就说明B中后续的区间都不可能再与A中第i个区间产生相交，但反过A中后续区间还可能与B中第j个区间相交。

2、若Ay[i] > By[j]，与情况1对称，此时A中后续区间都不能与B中第j个区间产生相交，但反过来B中后续区间还可能与A中第i个区间相交。

3、若Ay[i] \= By[j]，此时可以综合情况1和情况2，A中后续区间都不可能与B中第j个区间相交，B中后续区间也不可能与A中第i个相交。

有了上述结论，我们就可以使用类似二路归并的做法来求解A和B的相交情况，设当前处理到A的第i个区间以及B的第j个区间：

1、首先通过max_x以及min_y求解当前的区间的相交情况并更新答案

2、若此时Ay[i] \< By[j]，那么就将i往后移动一位

3、若此时Ay[i] > By[j]，那么就将j往后移动一位

4、若此时Ay[i] \= By[j]，那么就同时将i和j往后移动一位

最后附上python代码：

```python
class Solution(object):
    def intervalIntersection(self, firstList, secondList):
        """
        :type firstList: List[List[int]]
        :type secondList: List[List[int]]
        :rtype: List[List[int]]
        """

        i = j = 0
        m = len(firstList)
        n = len(secondList)

        res = []
        while i < m and j < n:
            x1, y1 = firstList[i]
            x2, y2 = secondList[j]
            if max(x1, x2) <= min(y1, y2):
                res.append([max(x1, x2), min(y1, y2)])
            
            if y1 < y2:
                i += 1
            elif y1 > y2:
                j += 1
            else:
                i += 1
                j += 1
        
        return res
```
