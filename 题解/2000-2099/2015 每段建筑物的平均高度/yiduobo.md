---
title: "2015. 每段建筑物的平均高度"
aliases: ["yiduobo的每日leetcode 2015.每段建筑物的平均高度"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/624944390"
zhihu_id: "624944390"
zhihu_title: "yiduobo的每日leetcode 2015.每段建筑物的平均高度"
question_id: "2015"
question: "每段建筑物的平均高度"
problem_url: "https://leetcode.cn/problems/average-height-of-buildings-in-each-segment/"
created: "2023-04-26T03:37:43+08:00"
updated: "2023-04-26T03:37:43+08:00"
upvotes: 0
comments: 0
---

# 2015. 每段建筑物的平均高度

> **[yiduobo的每日leetcode 2015.每段建筑物的平均高度](https://zhuanlan.zhihu.com/p/624944390) · 知乎 · 2023-04-26 · 赞同 0**
> 力扣：[2015. 每段建筑物的平均高度](https://leetcode.cn/problems/average-height-of-buildings-in-each-segment/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

2015.每段建筑物的平均高度

[力扣](https://leetcode.cn/problems/average-height-of-buildings-in-each-segment/)

如果将街道视为数组，那么一栋位于区间[l, r]，且高度为h的建筑就可以视为在数组[l, r]这一段加上h，问最后数组上每一段的平均值。由于是离线计算，那么在这里可以使用差分数组来处理。具体来说，就是将各个建筑左右边界全部收集起来然后一趟排序，接下来一趟遍历，计算前缀的高度和以及建筑数目，然后计算平均高度即可。

最后附上python代码：

```python
class Solution(object):
    def averageHeightOfBuildings(self, buildings):
        """
        :type buildings: List[List[int]]
        :rtype: List[List[int]]
        """

        points = []
        for left, right, avg in buildings:
            points.append([left * 2, avg])
            points.append([right * 2 - 1, avg])
        
        cnt = 0
        last = 0
        s = 0
        res = []
        for p, v in sorted(points):
            t = p % 2
            p = (p + 1) / 2
            if cnt > 0 and last != p:
                if res and last == res[-1][1] and s / cnt == res[-1][2]:
                    res[-1][1] = p
                else:
                    res.append([last, p, s / cnt])
            
            last = p
            if t == 0:
                cnt += 1
                s += v
            else:
                cnt -= 1
                s -= v

        return res
```
