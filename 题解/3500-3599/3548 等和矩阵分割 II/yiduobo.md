---
title: "3548. 等和矩阵分割II"
aliases: ["yiduobo的每日leetcode 3548.等和矩阵分割II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/零-常用枚举技巧", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1907614923212722301"
zhihu_id: "1907614923212722301"
zhihu_title: "yiduobo的每日leetcode 3548.等和矩阵分割II"
question_id: "3548"
question: "等和矩阵分割 II"
problem_url: "https://leetcode.cn/problems/equal-sum-grid-partition-ii/"
difficulty: "Hard"
rating: 2245
created: "2025-05-22T22:58:08+08:00"
updated: "2025-05-22T22:58:08+08:00"
upvotes: 1
comments: 0
---

# 3548. 等和矩阵分割II

> **[yiduobo的每日leetcode 3548.等和矩阵分割II](https://zhuanlan.zhihu.com/p/1907614923212722301) · 知乎 · 2025-05-22 · 赞同 1**
> 力扣：[3548. 等和矩阵分割 II](https://leetcode.cn/problems/equal-sum-grid-partition-ii/) · Hard · 灵茶山艾府：[式子变形 + 分类讨论 + 复用代码（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3548.等和矩阵分割II

[3548. 等和矩阵分割 II - 力扣（LeetCode）](https://leetcode.cn/problems/equal-sum-grid-partition-ii/description/)

题目给出一个由正整数组成的大小为m \* n的矩阵grid，现在要求找出一条水平或者垂直的分割线，将其分为两个非空的矩阵，且这两个矩阵在移除掉至多一个元素后元素之和相同。如果要执行移除操作，矩阵剩下的部分必须是连通的。问能否找出这样的分割。

之前3546题的加强版，本题中多了一次可用的移除操作，那么就可以想办法沿用之前的做法，分别枚举水平和竖直方向的分割方法。首先依然是检测不移除时是否存在可行的划分，然后检测数值和较大的那个部分减去较小的按个部分的差值，是否存在于较大的部分中，同时这个差值也可以被移除。

关于可以被移除这一点，只有当矩阵长或者宽为1时，移除中间的某个元素才会将矩阵分割成不连通的两个部分，以从上往下枚举水平分割为例：

首先对于i \= 0这一行，在一开始只能移除掉j \= 0或者j \= n - 1这两个位置上的元素，因为一开始这个矩阵只有i \= 0这一行，如果移除掉中间的元素就会将矩阵切分成两个部分。但是需要注意的是，当继续向下枚举，也就是i \= 1时，i \= 0这一行中的其他元素也可以被移除了，因为连通性已经被i \= 1这一行不足了，因此需要将i \= 0这一行中的其他元素补充到可以被移除的元素当中。

接下来对于i > 0的这些行，如果矩阵的宽n > 1，那么行中所有元素都可以被移除，同时移除掉这些元素也不会影响到后续的枚举；而当n \= 1时，这一行唯一的元素grid[i][0]只有在当前这种划分时才可以被移除，因为此时的grid[i][0]相当于某个长条矩阵的下端点，而i继续向下遍历时，grid[i][0]就不能被移除了，否则会将这个长条矩阵切割成两个部分。

基于这一点，就可以使用一个哈希表removeable记录可以移除的元素值，然后对于上半部分元素之和now减去下半部分的元素之和s - now，也就是now - (s - now)，出现在removeable，那么说明这个划分可行。

这样一来，只需从上到下，从下到上，从左到右，从右到左分别进行扫描划分，并计算已经扫过部分的removeable，就可以通过扫过部分的元素之和now以及removeable来判断当前划分是否可行了。

最后附上python代码：

```python
class Solution(object):
    def canPartitionGrid(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: bool
        """
        
        m = len(grid)
        n = len(grid[0])
        s = 0

        for i in range(m):
            for j in range(n):
                s += grid[i][j]
        
        removeable = set()
        now = 0
        for i in range(m - 1):
            for j in range(n):
                now += grid[i][j]
                if i == 0:
                    if j == 0 or j == n - 1:
                        removeable.add(grid[i][j])
                elif n > 1:
                    removeable.add(grid[i][j])
                elif now - grid[i][j] == s - now:
                    return True
            
            if i == 1:
                for j in range(1, n - 1):
                    removeable.add(grid[i - 1][j])

            if now + now == s:
                return True
            if now - (s - now) in removeable:
                return True
        
        removeable = set()
        now = 0
        for i in range(m - 1, 0, -1):
            for j in range(n):
                now += grid[i][j]
                if i == m - 1:
                    if j == 0 or j == n - 1:
                        removeable.add(grid[i][j])
                elif n > 1:
                    removeable.add(grid[i][j])
                elif now - grid[i][j] == s - now:
                    return True
            
            if i == m - 2:
                for j in range(1, n - 1):
                    removeable.add(grid[i + 1][j])
            
            if now + now == s:
                return True
            if now - (s - now) in removeable:
                return True
        
        removeable = set()
        now = 0
        for j in range(n - 1):
            for i in range(m):
                now += grid[i][j]
                if j == 0:
                    if i == 0 or i == m - 1:
                        removeable.add(grid[i][j])
                elif m > 1:
                    removeable.add(grid[i][j])
                elif now - grid[i][j] == s - now:
                    return True
            
            if j == 1:
                for i in range(1, m - 1):
                    removeable.add(grid[i][j - 1])
            
            if now + now == s:
                return True
            if now - (s - now) in removeable:
                return True
        
        removeable = set()
        now = 0
        for j in range(n - 1, 0, -1):
            for i in range(m):
                now += grid[i][j]
                if j == n - 1:
                    if i == 0 or i == m - 1:
                        removeable.add(grid[i][j])
                elif m > 1:
                    removeable.add(grid[i][j])
                elif now - grid[i][j] == s - now:
                    return True
            
            if j == n - 2:
                for i in range(1, m - 1):
                    removeable.add(grid[i][j + 1])
            
            if now + now == s:
                return True
            if now - (s - now) in removeable:
                return True
        
        return False
```
