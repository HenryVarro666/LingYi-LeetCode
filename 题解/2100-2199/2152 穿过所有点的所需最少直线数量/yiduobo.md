---
title: "2152. 穿过所有点的所需最少直线数量"
aliases: ["yiduobo的每日leetcode 2152.穿过所有点的所需最少直线数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/626827554"
zhihu_id: "626827554"
zhihu_title: "yiduobo的每日leetcode 2152.穿过所有点的所需最少直线数量"
question_id: "2152"
question: "穿过所有点的所需最少直线数量"
problem_url: "https://leetcode.cn/problems/minimum-number-of-lines-to-cover-points/"
created: "2023-05-05T00:31:35+08:00"
updated: "2023-05-05T00:31:35+08:00"
upvotes: 1
comments: 1
---

# 2152. 穿过所有点的所需最少直线数量

> **[yiduobo的每日leetcode 2152.穿过所有点的所需最少直线数量](https://zhuanlan.zhihu.com/p/626827554) · 知乎 · 2023-05-05 · 赞同 1**
> 力扣：[2152. 穿过所有点的所需最少直线数量](https://leetcode.cn/problems/minimum-number-of-lines-to-cover-points/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2152.穿过所有点的所需最少直线数量

[力扣](https://leetcode.cn/problems/minimum-number-of-lines-to-cover-points/)

题目中点的数量不超过10个，因此可以使用状态压缩动态规划来处理。

令f[state]表示覆盖state中这些点所需的最少直线数量，那么对于f[state]，可以直接枚举所有可能的直线，然后通过直线上的点与state计算出next_state，再使用f[state] + 1来更新f[next_state]。

具体实现上，可以先两两枚举这些点，预处理出所有的直线。需要特别注意的是，对于任意得到的直线，还需要枚举其他的点，计算出了枚举这两点之外还有哪些点也在直线上。

最后附上python代码：

```python
class Solution(object):
    def minimumLines(self, points):
        """
        :type points: List[List[int]]
        :rtype: int
        """

        def check(p1, p2, p3):
            x1, y1 = p2[0] - p1[0], p2[1] - p1[1]
            x2, y2 = p3[0] - p1[0], p3[1] - p1[1]
            return x1 * y2 == x2 * y1
        
        candidate = set()
        n = len(points)
        for i in range(n):
            candidate.add((1 << i))
            for j in range(i + 1, n):
                now = (1 << i) | (1 << j)
                for k in range(j + 1, n):
                    if check(points[i], points[j], points[k]):
                        now |= (1 << k)
                candidate.add(now)

        f = [n] * (1 << n)
        f[0] = 0
        for state in range((1 << n)):
            for line in candidate:
                next_state = state | line
                f[next_state] = min(f[next_state], f[state] + 1)
        
        return f[-1]
```
