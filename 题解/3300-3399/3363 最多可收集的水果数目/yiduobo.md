---
title: "3363. 最多可收集的水果数目"
aliases: ["yiduobo的每日leetcode 3363.最多可收集的水果数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/brainteaser", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/二-网格图-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/27492648883"
zhihu_id: "27492648883"
zhihu_title: "yiduobo的每日leetcode 3363.最多可收集的水果数目"
question_id: "3363"
question: "最多可收集的水果数目"
problem_url: "https://leetcode.cn/problems/find-the-maximum-number-of-fruits-collected/"
difficulty: "Hard"
rating: 2200
created: "2025-03-03T01:00:17+08:00"
updated: "2025-03-03T01:00:17+08:00"
upvotes: 2
comments: 0
---

# 3363. 最多可收集的水果数目

> **[yiduobo的每日leetcode 3363.最多可收集的水果数目](https://zhuanlan.zhihu.com/p/27492648883) · 知乎 · 2025-03-03 · 赞同 2**
> 力扣：[3363. 最多可收集的水果数目](https://leetcode.cn/problems/find-the-maximum-number-of-fruits-collected/) · Hard · 灵茶山艾府：[脑筋急转弯 + 网格图 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3363.最多可收集的水果数目

[3363. 最多可收集的水果数目 - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-maximum-number-of-fruits-collected/description/)

题目给出一个n \* n的二维矩阵fruits，其中fruits[i][j]表示单元格(i, j)内有fruits[i][j]个水果。有三个小朋友分别从矩阵的左上角(0, 0)，右上角(0, n - 1)以及右下角(n - 1, 0)开始移动，每个人都会移动n - 1步，且最终都会到达右下角(n - 1, n - 1)。

其中

从(0, 0)出发的小朋友每次只能从(i, j)移动到(i + 1, j + 1), (i, j + 1), (i + 1, j)三个单元格中的一个

从(0, n - 1)出发的小朋友每次只能从(i, j)移动到(i + 1, j - 1), (i + 1, j), (i + 1, j + 1)三个单元格中的一个

从(n - 1, 0)出发的小朋友每次只能从(i, j)移动到(i - 1, j + 1), (i, j + 1), (i + 1, j + 1)三个单元格中的一个

另外在整个移动过程中都不能超出矩阵边界。

当某个小朋友来到某个单元格时，单元格内的水果将被全部收集起来，但是多个小朋友访问同一个单元格也只能将其中的水果收集一次。问这三个小朋友最多可以收集的水果数目是多少。

看题目描述应该是经典的动态规划问题，但是本题中需要找出三条路径，且这三条路径相交的单元格只能被计算一次，那么在这里需要想办法去重。

注意到题目中有每个人将会移动n - 1步，且都会到达右下角(n - 1, n - 1)，那么对于从(0, 0)出发的小朋友而言，其只能沿着对角线从左上角一路走到右下角。

另一方面，对于从左上角(0, n - 1)出发的小朋友以及从右下角(n - 1, 0)出发的小朋友而言，他们行走的路线最多只能到达对角线，但是不能超过对角线，否则就不可能走回到(n - 1, n - 1)了。换言之，这两个小朋友的所有可行路径只可能与走对角线的小朋友相交，不可能与另一个小朋友相交。

那么在这里，如果让从左上角出发的小朋友收集掉对角线上的水果，就可以将矩阵的对角线全部置为0，然后利用动态规划计算从右上角和从左下角出发的小朋友的最佳路线就行了。

具体实现上，就是经典的f[i][j]表示这个小朋友走到第i行第j列时可以收集的最多水果，从上一轮的三个可行单元格转移过来就行了。另外对于右上角出发的小朋友，可以通过滚动数组优化掉i这一维，而从左下角出发的小朋友则可以通过滚动数组优化掉j这一维。

最后附上python代码：

```python
class Solution(object):
    def maxCollectedFruits(self, fruits):
        """
        :type fruits: List[List[int]]
        :rtype: int
        """

        n = len(fruits)
        
        f = [-1] * n
        f[n - 1] = fruits[n - 1][0]
        for j in range(1, n):
            g = f[:]
            f = [-1] * n
            for i in range(max(n - 1 - j, j), n):
                pre = -1
                if i - 1 >= 0 and g[i - 1] != -1:
                    pre = max(pre, g[i - 1])
                if g[i] != -1:
                    pre = max(pre, g[i])
                if i + 1 < n and g[i + 1] != -1:
                    pre = max(pre, g[i + 1])
                
                if pre == -1:
                    continue
                
                if i == j:
                    f[i] = pre
                else:
                    f[i] = pre + fruits[i][j]
        
        res = f[-1]

        f = [-1] * n
        f[n - 1] = fruits[0][n - 1]
        for i in range(1, n):
            g = f[:]
            f = [-1] * n
            for j in range(max(n - 1 - i, i), n):
                pre = -1
                if j - 1 >= 0 and g[j - 1] != -1:
                    pre = max(pre, g[j - 1])
                if g[j] != -1:
                    pre = max(pre, g[j])
                if j + 1 < n and g[j + 1] != -1:
                    pre = max(pre, g[j + 1])
                
                if pre == -1:
                    continue
                
                if i == j:
                    f[j] = pre
                else:
                    f[j] = pre + fruits[i][j]

        res += f[-1]

        
        for i in range(n):
            res += fruits[i][i]
        
        return res
```
