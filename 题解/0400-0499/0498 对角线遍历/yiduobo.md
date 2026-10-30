---
title: "498. 对角线遍历"
aliases: ["yiduobo的每日leetcode 498.对角线遍历"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bian-li", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/258102606"
zhihu_id: "258102606"
zhihu_title: "yiduobo的每日leetcode 498.对角线遍历"
question_id: "498"
question: "对角线遍历"
problem_url: "https://leetcode.cn/problems/diagonal-traverse/"
difficulty: "Medium"
created: "2020-09-22T21:10:00+08:00"
updated: "2020-09-22T21:10:00+08:00"
upvotes: 0
comments: 0
---

# 498. 对角线遍历

> **[yiduobo的每日leetcode 498.对角线遍历](https://zhuanlan.zhihu.com/p/258102606) · 知乎 · 2020-09-22 · 赞同 0**
> 力扣：[498. 对角线遍历](https://leetcode.cn/problems/diagonal-traverse/) · Medium · 灵茶山艾府：[【模板】遍历对角线（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

498.对角线遍历<https://leetcode-cn.com/problems/diagonal-traverse/>

经典的题目，有各式各样的做法，例如一步一步模拟，或者计算每个数字变换之后的位置。我在这里使用的是计算每一条对角线上有哪些数字，然后按奇偶性进行翻转。

如果将左上角视为第0条对角线，那么对于第i行第j个元素，其所在的对角线编号为i + j，于是可以先通过一次遍历计算出每条对角线上有哪些元素。接下来，对于编号为偶数的对角线，我们应当将其反转。最后将所有对角线拼起来即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def findDiagonalOrder(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: List[int]
        """

        if not matrix:
            return []

        m = len(matrix)
        n = len(matrix[0])
        res_list = [[] for _ in range(m + n + 1)]
        for i in range(m):
            for j in range(n):
                res_list[i + j].append(matrix[i][j])

        res = []
        for index in range(m + n + 1):
            if index % 2 == 0:
                res_list[index].reverse()
            res.extend(res_list[index])

        return res
```
