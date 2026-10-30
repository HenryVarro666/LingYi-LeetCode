---
title: "378. 有序矩阵中第K小的元素"
aliases: ["yiduobo的每日leetcode 378.有序矩阵中第K小的元素"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/binary-search", "题单/二分算法", "题单/常用数据结构", "题单/二分算法/二-二分答案", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/166183062"
zhihu_id: "166183062"
zhihu_title: "yiduobo的每日leetcode 378.有序矩阵中第K小的元素"
question_id: "378"
question: "有序矩阵中第 K 小的元素"
problem_url: "https://leetcode.cn/problems/kth-smallest-element-in-a-sorted-matrix/"
difficulty: "Medium"
created: "2020-08-02T23:42:42+08:00"
updated: "2020-08-02T23:42:42+08:00"
upvotes: 0
comments: 0
---

# 378. 有序矩阵中第K小的元素

> **[yiduobo的每日leetcode 378.有序矩阵中第K小的元素](https://zhuanlan.zhihu.com/p/166183062) · 知乎 · 2020-08-02 · 赞同 0**
> 力扣：[378. 有序矩阵中第 K 小的元素](https://leetcode.cn/problems/kth-smallest-element-in-a-sorted-matrix/) · Medium · 灵茶山艾府：[【图解】第 k 小/大问题的通用转化方法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

378.有序矩阵中第K小的元素<https://leetcode-cn.com/problems/kth-smallest-element-in-a-sorted-matrix/>

这一题与之前某一题有些类似（找不到哪一题了），都是对于matrix[x][y]而言，

1、以matrix[0][0]为左上角，matrix[x][y]为右下角的矩阵中，matrix[x][y]一定是最大的

2、以matrix[x][y]为左上角，matrix[n - 1][n - 1]为右下角的矩阵中，matrix[x][y]一定是最小的

对于matrix[i][j]，若matrix[i][j]小于等于k，而matrix[i + 1][j]大于k，那么说明第j列中有i个数小于等于k，而对于第j + 1列，必然有

matrix[i + 1][j + 1] > matrix[i + 1][j] > k

因此可以直接从matrix[i][j + 1]开始检测第j + 1行中有多少个数小于等于k

那么这样一来，就从matrix[n - 1][0]开始，按上面的方法逐列检测当期列有多少个数小于等于k，于是在O(n + n)的时间内就可以找到matrix中小于等于k的数有多少个。

回到原问题，是需要找到第k小的数是多少，于是我们可以二分答案，每次检测matrix中小于等于mid的数有多少个。二分的边界自然是matrix[0][0]与matrix[n - 1][n - 1]。

最终的时间复杂度为O(nlog(max - min))，其中max为matrix[n - 1][n - 1]，min为matrix[0][0]。

最后附上python代码：

```python
class Solution(object):
    def kthSmallest(self, matrix, k):
        """
        :type matrix: List[List[int]]
        :type k: int
        :rtype: int
        """

        n = len(matrix)

        l = matrix[0][0]
        r = matrix[n - 1][n - 1]
        while l < r:
            mid = (l + r) / 2

            x = n - 1
            y = 0
            cnt = 0
            while x >= 0 and y < n:
                if matrix[x][y] <= mid:
                    cnt += x + 1
                    y += 1
                else:
                    x -= 1

            if cnt >= k:
                r = mid
            else:
                l = mid + 1

        return l
```
