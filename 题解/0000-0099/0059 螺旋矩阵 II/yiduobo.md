---
title: "59. 螺旋矩阵 II"
aliases: ["yiduobo的每日leetcode 59.螺旋矩阵 II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/128675063"
zhihu_id: "128675063"
zhihu_title: "yiduobo的每日leetcode 59.螺旋矩阵 II"
question_id: "59"
question: "螺旋矩阵 II"
problem_url: "https://leetcode.cn/problems/spiral-matrix-ii/"
difficulty: "Medium"
created: "2020-04-10T21:28:35+08:00"
updated: "2020-04-10T21:28:35+08:00"
upvotes: 0
comments: 0
---

# 59. 螺旋矩阵 II

> **[yiduobo的每日leetcode 59.螺旋矩阵 II](https://zhuanlan.zhihu.com/p/128675063) · 知乎 · 2020-04-10 · 赞同 0**
> 力扣：[59. 螺旋矩阵 II](https://leetcode.cn/problems/spiral-matrix-ii/) · Medium · 灵茶山艾府：[利用方向向量简化代码（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

59.螺旋矩阵 II<https://leetcode-cn.com/problems/spiral-matrix-ii/submissions/>

又是螺旋矩阵的问题，思路与之前的54题螺旋矩阵一样（传送门在此[yiduobo：yiduobo的每日leetcode 54.螺旋矩阵](https://zhuanlan.zhihu.com/p/127382668)），都是从外往内每次处理一个矩形，然后对于每个矩形同样是分为上边、右边、下边、左边依次进行处理。这个题目因为规定了都是正方形，所以实际上还简单一些。不过需要注意的是，当n为奇数时，中心点的四边都是重叠的，只需要处理依次。

最后附上python代码：

```python
class Solution(object):
    def generateMatrix(self, n):
        """
        :type n: int
        :rtype: List[List[int]]
        """

        res = [[0 for index in range(n)] for index in range(n)]

        now = 1
        for index in range((n + 1) / 2):
            x1 = y1 = index
            x2 = y2 = n - index - 1

            if x1 == x2:
                res[x1][y1] = now
            else:
                for pos in range(y1, y2):
                    res[x1][pos] = now
                    now += 1
                for pos in range(x1, x2):
                    res[pos][y2] = now
                    now += 1
                for pos in range(y2, y1, -1):
                    res[x2][pos] = now
                    now += 1
                for pos in range(x2, x1, -1):
                    res[pos][y1] = now
                    now += 1
        return res
```
