---
title: "2280. 表示一个折线图的最少线段数"
aliases: ["yiduobo的每日leetcode 2280.表示一个折线图的最少线段数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/geometry", "leetcode/math", "leetcode/sorting", "题单/数学算法", "题单/数学算法/五-计算几何"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/551181047"
zhihu_id: "551181047"
zhihu_title: "yiduobo的每日leetcode 2280.表示一个折线图的最少线段数"
question_id: "2280"
question: "表示一个折线图的最少线段数"
problem_url: "https://leetcode.cn/problems/minimum-lines-to-represent-a-line-chart/"
difficulty: "Medium"
rating: 1681
created: "2022-08-08T14:15:31+08:00"
updated: "2022-08-08T14:15:31+08:00"
upvotes: 0
comments: 0
---

# 2280. 表示一个折线图的最少线段数

> **[yiduobo的每日leetcode 2280.表示一个折线图的最少线段数](https://zhuanlan.zhihu.com/p/551181047) · 知乎 · 2022-08-08 · 赞同 0**
> 力扣：[2280. 表示一个折线图的最少线段数](https://leetcode.cn/problems/minimum-lines-to-represent-a-line-chart/) · Medium · 灵茶山艾府：[判断三点共线](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2280.表示一个折线图的最少线段数

[力扣](https://leetcode.cn/problems/minimum-lines-to-represent-a-line-chart/)

首先考虑边界情况。当图中只有一个点时，答案为0。当图中只有两个点时，答案为1。

接下来考虑一般情况。可以发现，如果相邻的三点不在一条直线上，那么就会产生一条折线，于是可以将所有点先按照x坐标从小到大排序，然后一趟遍历，判断相邻的三点是否共线。

对于三点共线问题，可以先求出第一个点与第二个点形成的向量，以及第二个点与第三个点形成的向量，然后通过叉积判断两个向量是否共线就行了。

最后附上python代码：

```python
class Solution(object):
    def minimumLines(self, stockPrices):
        """
        :type stockPrices: List[List[int]]
        :rtype: int
        """

        res = 0
        if len(stockPrices) == 1:
            return 0
        elif len(stockPrices) == 2:
            return 1
        else:
            sorted_info = sorted(stockPrices, key=lambda d:d[0])
            px, py = sorted_info[1][0] - sorted_info[0][0], sorted_info[1][1] - sorted_info[0][1]
            for index in range(2, len(sorted_info)):
                qx, qy = sorted_info[index][0] - sorted_info[index - 1][0], sorted_info[index][1] - sorted_info[index - 1][1]
                if px * qy != py * qx:
                    res += 1
                    px, py = qx, qy
        
        return res + 1
```
