---
title: "296. 最佳的碰头地点"
aliases: ["yiduobo的每日leetcode 296.最佳的碰头地点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/595338424"
zhihu_id: "595338424"
zhihu_title: "yiduobo的每日leetcode 296.最佳的碰头地点"
question_id: "296"
question: "最佳的碰头地点"
problem_url: "https://leetcode.cn/problems/best-meeting-point/"
created: "2022-12-30T00:28:33+08:00"
updated: "2022-12-30T00:28:33+08:00"
upvotes: 0
comments: 0
---

# 296. 最佳的碰头地点

> **[yiduobo的每日leetcode 296.最佳的碰头地点](https://zhuanlan.zhihu.com/p/595338424) · 知乎 · 2022-12-30 · 赞同 0**
> 力扣：[296. 最佳的碰头地点](https://leetcode.cn/problems/best-meeting-point/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

296.最佳的碰头地点

[力扣](https://leetcode.cn/problems/best-meeting-point/)

首先，注意到行和列互相之间不会产生影响，因此在这里可以分开求解最佳的行和最佳的列。

接下来，如果单独考虑行或者列，可以发现这是经典的最优位置问题，最终答案就是取中位数的位置最佳。

于是现在就得到了一种算法：先遍历矩形找出其中为1的点，并分别将横纵坐标收集起来。遍历完成后，将横纵坐标分别排序，然后再一趟遍历计算各个位置到对应坐标中位数的差值，累加后即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minTotalDistance(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        x_list = []
        y_list = []
        
        m = len(grid)
        n = len(grid[0])
        for x in range(m):
            for y in range(n):
                if grid[x][y] == 1:
                    x_list.append(x)
                    y_list.append(y)
        
        def calc(arr):
            arr.sort()
            target = arr[len(arr) / 2]
            res = 0
            for v in arr:
                res += abs(v - target)
            return res

        return calc(x_list) + calc(y_list)
```
