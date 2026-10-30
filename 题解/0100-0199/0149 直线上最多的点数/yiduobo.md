---
title: "149. 直线上最多的点数"
aliases: ["yiduobo的每日leetcode 149.直线上最多的点数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/geometry", "leetcode/hash-table", "leetcode/math", "题单/面试经典-150-题", "题单/面试经典-150-题/数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/143114533"
zhihu_id: "143114533"
zhihu_title: "yiduobo的每日leetcode 149.直线上最多的点数"
question_id: "149"
question: "直线上最多的点数"
problem_url: "https://leetcode.cn/problems/max-points-on-a-line/"
difficulty: "Hard"
created: "2020-05-23T22:21:03+08:00"
updated: "2020-05-23T22:21:03+08:00"
upvotes: 0
comments: 0
---

# 149. 直线上最多的点数

> **[yiduobo的每日leetcode 149.直线上最多的点数](https://zhuanlan.zhihu.com/p/143114533) · 知乎 · 2020-05-23 · 赞同 0**
> 力扣：[149. 直线上最多的点数](https://leetcode.cn/problems/max-points-on-a-line/) · Hard · 灵茶山艾府：[暴力枚举（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

149.直线上最多的点数<https://leetcode-cn.com/problems/max-points-on-a-line/>

目前只想到平方的做法，不知道如果用到计算几何方面的东西能不能继续往下优化。

平方的做法主要思路为直线除了斜截式，即y \= kx + b这种形式之外，还可以使用点斜式表示，即我们先选取一个基准点p，那么过p的直线可以写成y - py \= k(x - px)的形式。于是可以枚举剩下的点，计算出k。若两个点得到的k相同，那么其位于同一条直线上。统计同一直线上点的数量取最大值即为答案。

这里有两个需要特别注意的地方：

第一个是计算k的时候需要用到除法，可能会出现损失精度的情况。我在这里的处理办法是直接记录下分子与分母。这样做还有一个好处就是对于垂直的直线k也是没有意义的，而用分子分母的方式也可以将其记录下来。

第二个可能出现点重叠的情况。这种情况下k是没有意义的，因此需要额外统计出重叠的点，这些点不参与k的计算与比较。

最后附上python代码：

```python
class Solution(object):
    def maxPoints(self, points):
        """
        :type points: List[List[int]]
        :rtype: int
        """

        if len(points) < 3:
            return len(points)

        res = 0
        for index, point1 in enumerate(points):
            x1, y1 = point1
            param_dict = {}
            same_point_cnt = 1
            for point2 in points[index + 1:]:
                x2, y2 = point2
                
                part1 = y2 - y1
                part2 = x2 - x1

                if part1 == 0 and part2 == 0:
                    same_point_cnt += 1
                    continue

                
                flag = False
                for key in param_dict:
                    if part1 * key[1] == part2 * key[0]:
                        param_dict[key] += 1
                        flag = True
                        break

                if not flag:
                    param_dict[(part1, part2)] = 1

            if param_dict:
                same_line_cnt = max(param_dict.values())
            else:
                same_line_cnt = 0
                
            res = max(res, same_line_cnt + same_point_cnt)

        return res
```
