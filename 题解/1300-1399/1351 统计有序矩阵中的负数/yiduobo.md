---
title: "1351. 统计有序矩阵中的负数"
aliases: ["yiduobo的每日leetcode 1351.统计有序矩阵中的负数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/397620331"
zhihu_id: "397620331"
zhihu_title: "yiduobo的每日leetcode 1351.统计有序矩阵中的负数"
question_id: "1351"
question: "统计有序矩阵中的负数"
problem_url: "https://leetcode.cn/problems/count-negative-numbers-in-a-sorted-matrix/"
difficulty: "Easy"
created: "2021-08-08T17:54:42+08:00"
updated: "2021-08-08T17:54:42+08:00"
upvotes: 0
comments: 0
---

# 1351. 统计有序矩阵中的负数

> **[yiduobo的每日leetcode 1351.统计有序矩阵中的负数](https://zhuanlan.zhihu.com/p/397620331) · 知乎 · 2021-08-08 · 赞同 0**
> 力扣：[1351. 统计有序矩阵中的负数](https://leetcode.cn/problems/count-negative-numbers-in-a-sorted-matrix/) · Easy · 灵茶山艾府：[【图解】疯狂撕数字，一图秒懂（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1351.统计有序矩阵中的负数

[力扣](https://leetcode-cn.com/problems/count-negative-numbers-in-a-sorted-matrix/)

之前也遇到过类似的题目，但是忘记题目号码了，这里再复习一遍。

题目要求矩阵中负数的数目，那么我们可以反过来求矩阵中非负数的数目，再用总数减去这个数目。

具体求解方法需要利用到单调性。

我们逐行求解，设now为当前行最小的非负数的下标，那么我们先初始化now为n - 1，然后向前扫描，直到非负数出现。

那么可以明确的是，对于当前行，第0到第now这些数必然都是非负数，于是应该将答案减去now + 1。

另外，由于行之间也满足单调性，设当前行为第i行，那么就有

grid[i][now + 1] \< 0

而由于

grid[i][now + 1] >\= grid[i + 1][now + 1]

也就是说

grid[i + 1][now + 1] \< 0

于是在求解第i + 1行最小非负数的位置时，我们可以直接从第i + 1行的now这个位置开始向前遍历，于是这样就得到了一种O(m + n)的做法了

最后附上python代码：

```python
class Solution(object):
    def countNegatives(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])
        res = m * n
        now = n - 1
        for index in range(m):
            while now >= 0 and grid[index][now] < 0:
                now -= 1
            
            if now == -1:
                break
            
            res = res - now - 1

        return res
```
