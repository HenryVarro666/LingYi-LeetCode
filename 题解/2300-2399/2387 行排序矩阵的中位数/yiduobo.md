---
title: "2387. 行排序矩阵的中位数"
aliases: ["yiduobo的每日leetcode 2387.行排序矩阵的中位数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/630788428"
zhihu_id: "630788428"
zhihu_title: "yiduobo的每日leetcode 2387.行排序矩阵的中位数"
question_id: "2387"
question: "行排序矩阵的中位数"
problem_url: "https://leetcode.cn/problems/median-of-a-row-wise-sorted-matrix/"
created: "2023-05-20T04:54:31+08:00"
updated: "2023-05-20T04:54:31+08:00"
upvotes: 1
comments: 0
---

# 2387. 行排序矩阵的中位数

> **[yiduobo的每日leetcode 2387.行排序矩阵的中位数](https://zhuanlan.zhihu.com/p/630788428) · 知乎 · 2023-05-20 · 赞同 1**
> 力扣：[2387. 行排序矩阵的中位数](https://leetcode.cn/problems/median-of-a-row-wise-sorted-matrix/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2387.行排序矩阵的中位数

[力扣](https://leetcode.cn/problems/median-of-a-row-wise-sorted-matrix/)

题目给出m个长度为n且单调不减的数组，要求找出这m \* n个数的中位数。

对于这个问题，O(mlog(n)log(C))的算法是很容易想到的。首先二分答案res，接下来遍历每一行，在当前行中通过二分找出当前行中有多少个数小于等于res。将每一行小于等于res的数的数量累加起来，然后通过这个值与m \* n / 2的大小来调整二分的上下界即可。

另外题目想要一种O(mlog(n))的算法，但是目前还没有什么思路，所以最后还是采用了上面这种算法。

最后附上python代码：

```python
class Solution(object):
    def matrixMedian(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])

        def check(v):
            cnt = 0
            for i in range(m):
                if v < grid[i][0]:
                    continue
                left = 0
                right = n - 1
                while left < right:
                    mid = (left + right + 1) / 2
                    if grid[i][mid] <= v:
                        left = mid
                    else:
                        right = mid - 1
                
                cnt += left + 1

            return cnt > m * n / 2

        left = 1
        right = 10 ** 6
        while left < right:
            mid = (left + right) / 2
            if check(mid):
                right = mid
            else:
                left = mid + 1
        
        return left
```
