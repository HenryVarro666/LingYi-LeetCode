---
title: "3963. 构造恰好一条路径的网格"
aliases: ["yiduobo的每日leetcode 3963.构造恰好一条路径的网格"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "题单/贪心算法", "题单/贪心算法/六-构造题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2052122997507592401"
zhihu_id: "2052122997507592401"
zhihu_title: "yiduobo的每日leetcode 3963.构造恰好一条路径的网格"
question_id: "3963"
question: "构造恰好一条路径的网格"
problem_url: "https://leetcode.cn/problems/create-grid-with-exactly-one-path/"
difficulty: "Easy"
rating: 1311
created: "2026-06-22T22:43:36+08:00"
updated: "2026-06-22T22:43:39+08:00"
upvotes: 0
comments: 0
---

# 3963. 构造恰好一条路径的网格

> **[yiduobo的每日leetcode 3963.构造恰好一条路径的网格](https://zhuanlan.zhihu.com/p/2052122997507592401) · 知乎 · 2026-06-22 · 赞同 0**
> 力扣：[3963. 构造恰好一条路径的网格](https://leetcode.cn/problems/create-grid-with-exactly-one-path/) · Easy · 灵茶山艾府：[构造题，简单做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3963.构造恰好一条路径的网格

<https://leetcode.cn/problems/create-grid-with-exactly-one-path/description/>

题目给出两个整数m和n，分别表示网格的行数和列数。

现在要求构造一个只包含字符'.'以及'\#'的m \* n的网格，其中'.'表示空格，'\#'表示障碍物。这个网格中必须恰好只有一条从(0, 0)开始，仅通过向右或者向下移动且不经过任何障碍物，最终到达(m - 1, n - 1)的路径。

要求返回一个符合条件的网格。

题目要求构造一个仅包含一条符合条件的路径的网格，那么一个直观的想法就是为这条路径留出足够的空格，其他的地方全部填充障碍物。

对于这条路径，有多种方法可以构造，我在这里选择的是构造'L'形的路径，即从(0, 0)往下走到(m - 1, 0)，然后向右走到(m - 1, n - 1)。对应的构造方案则是前m - 1行的首字符为'.'，其他字符为'\#'，最后一行全都是'.'。

最后附上python代码：

```python
class Solution(object):
    def createGrid(self, m, n):
        """
        :type m: int
        :type n: int
        :rtype: List[str]
        """
        
        res = []
        for index in range(m - 1):
            res.append('.' + '#' * (n - 1))
        res.append('.' * n)
        return res
```
