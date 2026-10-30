---
title: "118. 杨辉三角 & 119. 杨辉三角II"
aliases: ["yiduobo的每日leetcode 118.杨辉三角 && 119.杨辉三角II", "118. 杨辉三角", "119. 杨辉三角II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/dynamic-programming", "leetcode/combinatorics", "题单/LeetCode-热题-100", "题单/LeetCode-热题-100/动态规划"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/139362699"
zhihu_id: "139362699"
zhihu_title: "yiduobo的每日leetcode 118.杨辉三角 && 119.杨辉三角II"
question_id: ["118", "119"]
question: ["杨辉三角", "杨辉三角 II"]
problem_url: ["https://leetcode.cn/problems/pascals-triangle/", "https://leetcode.cn/problems/pascals-triangle-ii/"]
difficulty: "Easy"
created: "2020-05-09T22:04:33+08:00"
updated: "2020-05-09T22:04:33+08:00"
upvotes: 0
comments: 0
---

# 118. 杨辉三角 & 119. 杨辉三角II

> **[yiduobo的每日leetcode 118.杨辉三角 && 119.杨辉三角II](https://zhuanlan.zhihu.com/p/139362699) · 知乎 · 2020-05-09 · 赞同 0**
> 力扣：[118. 杨辉三角](https://leetcode.cn/problems/pascals-triangle/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](../0118%20杨辉三角/灵茶山艾府.md)
> 力扣：[119. 杨辉三角 II](https://leetcode.cn/problems/pascals-triangle-ii/) · Easy · 灵茶山艾府：[如何理解这个式子？选或不选的角度（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

118.杨辉三角<https://leetcode-cn.com/problems/pascals-triangle/>

119.杨辉三角II<https://leetcode-cn.com/problems/pascals-triangle-ii/>

经典的数学题。

118题需要求出所有的数字，119题则是求出某一层的数字即可。

可以按照题目动画给出的动态规划方法来求，这里是118题的python代码：

```python
class Solution(object):
    def generate(self, numRows):
        """
        :type numRows: int
        :rtype: List[List[int]]
        """

        if numRows == 0:
            return []

        if numRows == 1:
            return [[1]]

        f = [[1], [1, 1]]
        for index in range(2, numRows):
            f.append([1] + [f[index - 1][i - 1] + f[index - 1][i] for i in range(1, len(f[index - 1]))] + [1])

        return f
```

另外，杨辉三角本质上就是二项式定理，即(x + 1)^k展开之后，x按次数排列之后的系数，于是也可以用组合数学来求解，第k行分别为C(k, 0), C(k, 1)...，C(k, k)。另外，由于C(m, n)与C(m, m - n)是等价的，因此这里只需要求出行中的一半数值，然后反过来复制一遍即可。这里是119题的python代码：

```python
class Solution(object):
    def getRow(self, rowIndex):
        """
        :type rowIndex: int
        :rtype: List[int]
        """

        res = [1]
        mid = rowIndex / 2
        for index in range(1, mid + 1):
            res.append(res[-1] * (rowIndex - index + 1) / index)
        
        res.extend([res[index] for index in range((rowIndex - 1) / 2, -1, -1)])
        return res
```
