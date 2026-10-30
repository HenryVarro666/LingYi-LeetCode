---
title: "764. 最大加号标志"
aliases: ["yiduobo的每日leetcode 764.最大加号标志"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/338856642"
zhihu_id: "338856642"
zhihu_title: "yiduobo的每日leetcode 764.最大加号标志"
question_id: "764"
question: "最大加号标志"
problem_url: "https://leetcode.cn/problems/largest-plus-sign/"
created: "2020-12-23T00:44:00+08:00"
updated: "2020-12-23T00:44:00+08:00"
upvotes: 0
comments: 0
---

# 764. 最大加号标志

> **[yiduobo的每日leetcode 764.最大加号标志](https://zhuanlan.zhihu.com/p/338856642) · 知乎 · 2020-12-23 · 赞同 0**
> 力扣：[764. 最大加号标志](https://leetcode.cn/problems/largest-plus-sign/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

764.最大加号标志

[力扣](https://leetcode-cn.com/problems/largest-plus-sign/)

题目要求找出二维01数组中最大的加号，那么可以将问题分成为求数组中的每个点，其上、下、左、右四个方向分别有多少个连续的1，那么以这个点为中心的加号长度就是这四个方向中最短的那一个。

我的做法比较暴力，直接使用四个二维数组left、right、up、down储存对应个结果。需要注意的是，再进行扫描的时候需要按照合理的方向，例如对于up数组，需要先循环列再循环行，而对于down数组，则需要先循环列再反向循环行。

状态的转移也很简单，以up数组为例，若当前字符为1，那么up[i][j] \= up[i - 1][j] + 1，否则up[i][j] \= 0。当然，对于边界的情况也需要特别注意。

依次求出这四个数组之后，遍历数组中的每个位置，那么以当前位置为中心的加号的长度就是min(left[i][j], right[i][j], up[i][j], down[i][j])，然后用这个值去更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def orderOfLargestPlusSign(self, N, mines):
        """
        :type N: int
        :type mines: List[List[int]]
        :rtype: int
        """

        left = [[0] * N for _ in range(N)]
        right = [[0] * N for _ in range(N)]
        up = [[0] * N for _ in range(N)]
        down = [[0] * N for _ in range(N)]

        mine_set = set()
        for x, y in mines:
            mine_set.add((x, y))
        
        for i in range(N):
            for j in range(N):
                if (i, j) in mine_set:
                    left[i][j] = 0
                elif j == 0:
                    left[i][j] = 1
                else:
                    left[i][j] = left[i][j - 1] + 1
        
        for i in range(N):
            for j in range(N - 1, -1, -1):
                if (i, j) in mine_set:
                    right[i][j] = 0
                elif j == N - 1:
                    right[i][j] = 1
                else:
                    right[i][j] = right[i][j + 1] +1
        
        for j in range(N):
            for i in range(N):
                if (i, j) in mine_set:
                    up[i][j] = 0
                elif i == 0:
                    up[i][j] = 1
                else:
                    up[i][j] = up[i - 1][j] + 1
        
        for j in range(N):
            for i in range(N - 1, -1, -1):
                if (i, j) in mine_set:
                    down[i][j] = 0
                elif i == N - 1:
                    down[i][j] = 1
                else:
                    down[i][j] = down[i + 1][j] + 1

        res = 0
        for i in range(N):
            for j in range(N):
                res = max(res, min(left[i][j], right[i][j], up[i][j], down[i][j]))
        
        return res
```
