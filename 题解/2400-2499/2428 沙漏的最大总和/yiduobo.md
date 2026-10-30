---
title: "2428. 沙漏的最大总和"
aliases: ["yiduobo的每日leetcode 2428.沙漏的最大总和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/582642641"
zhihu_id: "582642641"
zhihu_title: "yiduobo的每日leetcode 2428.沙漏的最大总和"
question_id: "2428"
question: "沙漏的最大总和"
problem_url: "https://leetcode.cn/problems/maximum-sum-of-an-hourglass/"
difficulty: "Medium"
created: "2022-11-11T21:56:23+08:00"
updated: "2022-11-11T21:56:23+08:00"
upvotes: 0
comments: 0
---

# 2428. 沙漏的最大总和

> **[yiduobo的每日leetcode 2428.沙漏的最大总和](https://zhuanlan.zhihu.com/p/582642641) · 知乎 · 2022-11-11 · 赞同 0**
> 力扣：[2428. 沙漏的最大总和](https://leetcode.cn/problems/maximum-sum-of-an-hourglass/) · Medium · 灵茶山艾府：[遍历](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2428.沙漏的最大总和

[力扣](https://leetcode.cn/problems/maximum-sum-of-an-hourglass/)

题目的沙漏严格定义为工字形块，且这个块的大小也不会放大，那么就可以直接枚举工字形的连接处。对于当前枚举到的位置(x, y)，计算这个位置左上、上方、右上、左下、下方、右下，以及这个格子自身这七个格子的数值之和，取其中最大的作为答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxSum(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        res = 0
        m = len(grid)
        n = len(grid[0])

        dx = [0, -1, -1, -1, 1, 1, 1]
        dy = [0, -1, 0, 1, -1, 0, 1]

        for i in range(1, m - 1):
            for j in range(1, n - 1):
                now = 0
                for index in range(7):
                    now += grid[i + dx[index]][j + dy[index]]
                res = max(res, now)

        return res
```
