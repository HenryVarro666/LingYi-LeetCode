---
title: "2133. 检查是否每一行每一列都包含全部整数"
aliases: ["yiduobo的每日leetcode 2133.检查是否每一行每一列都包含全部整数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/matrix"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/527530970"
zhihu_id: "527530970"
zhihu_title: "yiduobo的每日leetcode 2133.检查是否每一行每一列都包含全部整数"
question_id: "2133"
question: "检查是否每一行每一列都包含全部整数"
problem_url: "https://leetcode.cn/problems/check-if-every-row-and-column-contains-all-numbers/"
difficulty: "Easy"
created: "2022-06-11T21:10:55+08:00"
updated: "2022-06-11T21:10:55+08:00"
upvotes: 0
comments: 0
---

# 2133. 检查是否每一行每一列都包含全部整数

> **[yiduobo的每日leetcode 2133.检查是否每一行每一列都包含全部整数](https://zhuanlan.zhihu.com/p/527530970) · 知乎 · 2022-06-11 · 赞同 0**
> 力扣：[2133. 检查是否每一行每一列都包含全部整数](https://leetcode.cn/problems/check-if-every-row-and-column-contains-all-numbers/) · Easy · 灵茶山艾府：[高效写法，只需初始化一次统计数组](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2133.检查是否每一行每一列都包含全部整数

[力扣](https://leetcode.cn/problems/check-if-every-row-and-column-contains-all-numbers/)

由于题目保证了矩阵中的数都在1到n直接，那么对于任意行或者列，如果用哈希表来储存其中的数，只要出现了相同的数哈希表的大小就必然小于n，反之若哈希表的大小等于n，那么说明当前行或者列包含了1到n直接的所有数。于是可以遍历每一行和每一列，利用哈希表来判断是否包含了全部整数。

最后附上python代码：

```python
class Solution(object):
    def checkValid(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: bool
        """

        n = len(matrix)

        def check(x, y, dx, dy):
            num_set = set()
            for index in range(n):
                num_set.add(matrix[x][y])
                x += dx
                y += dy
            
            return len(num_set) == n
        
        for index in range(n):
            if not check(index, 0, 0, 1):
                return False

            if not check(0, index, 1, 0):
                return False
        
        return True
```
