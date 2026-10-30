---
title: "3009. 折线图上的最大交点数量"
aliases: ["yiduobo的每日leetcode 3009.折线图上的最大交点数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/693761773"
zhihu_id: "693761773"
zhihu_title: "yiduobo的每日leetcode 3009.折线图上的最大交点数量"
question_id: "3009"
question: "折线图上的最大交点数量"
problem_url: "https://leetcode.cn/problems/count-the-number-of-houses-at-a-certain-distance-i/"
created: "2024-04-21T23:39:06+08:00"
updated: "2024-04-21T23:39:06+08:00"
upvotes: 0
comments: 0
---

# 3009. 折线图上的最大交点数量

> **[yiduobo的每日leetcode 3009.折线图上的最大交点数量](https://zhuanlan.zhihu.com/p/693761773) · 知乎 · 2024-04-21 · 赞同 0**
> 力扣：[3009. 折线图上的最大交点数量](https://leetcode.cn/problems/count-the-number-of-houses-at-a-certain-distance-i/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3009.折线图上的最大交点数量

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-the-number-of-houses-at-a-certain-distance-i/description/)

题目给出一条折线，问这条折线上出现的最多的纵坐标值数量。又由于折线的转折点都出现在整数点上，那么最终答案也必然是落在某个整数值上，因为若最终答案落在非整数点上，就可以将这个值向上或者向下平移到整点值也不会影响答案的大小。

有了这一点，就可以将折线拆分成若干的线段，然后利用差分数组来计算。不过需要注意的是，这里拆分出来的线段只能是前开后闭或者前闭后开的，因为转折点不能计算多次。我在这里选择的是拆分成前闭后开的线段，这样的会遗留下最后这个点，需要单独计算。例如样例一，拆分得到的线段就是[1, 2)，[2, 1)，[1, 2)，[2, 1)，[1, 3)，[3, 2)，以及一个单点值2。

对于开闭区间的处理方式，一种经典的处理方法是乘2。由于接下来需要使用差分数组，因此先要保证线段的起点和终点有序。对于样例一，得到的就是[1, 2)，(1, 2]，[1, 2)，(1, 2]，[1, 3)，(2, 3]。接下来将乘以2运用进来。如果是闭点，就直接乘以2。如果是开点，乘以2之后就需要尽量向另一端靠近。例如[1, 2)应该变成[2, 3]，而(1, 2]则应该变成[3, 4]，那么最终得到的区间就是[2, 3]，[3, 4]，[2, 3]，[3, 4]，[2, 5]，[5, 6]。另外还有一个单独的2，直接转化成[4, 4]。

得到线段后，按起点从小到大进行排序，然后使用差分数组来计算就行了。

最后附上python代码：

```python
class Solution(object):
    def maxIntersectionCount(self, y):
        """
        :type y: List[int]
        :rtype: int
        """

        points = []
        for index in range(1, len(y)):
            if y[index] > y[index - 1]:
                left, right = y[index - 1] * 2, y[index] * 2 - 1
            else:
                left, right = y[index] * 2 + 1, y[index - 1] * 2
            
            points.append([left, -1])
            points.append([right, 1])
        
        points.append([y[-1] * 2, -1])
        points.append([y[-1] * 2, 1])

        points.sort()
        now = 0
        res = 0
        for v, delta in points:
            now -= delta
            res = max(now, res)
        
        return res
```
