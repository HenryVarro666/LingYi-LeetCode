---
title: "3529. 统计水平子串和垂直子串重叠格子的数目"
aliases: ["yiduobo的每日leetcode 3529.统计水平子串和垂直子串重叠格子的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "leetcode/prefix-sum", "leetcode/string-matching", "题单/常用数据结构", "题单/字符串", "题单/常用数据结构/二-差分", "题单/字符串/一-KMP-前缀的后缀"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1904704330398930155"
zhihu_id: "1904704330398930155"
zhihu_title: "yiduobo的每日leetcode 3529.统计水平子串和垂直子串重叠格子的数目"
question_id: "3529"
question: "统计水平子串和垂直子串重叠格子的数目"
problem_url: "https://leetcode.cn/problems/count-cells-in-overlapping-horizontal-and-vertical-substrings/"
difficulty: "Medium"
rating: 2105
created: "2025-05-13T23:00:15+08:00"
updated: "2025-05-13T23:00:15+08:00"
upvotes: 0
comments: 0
---

# 3529. 统计水平子串和垂直子串重叠格子的数目

> **[yiduobo的每日leetcode 3529.统计水平子串和垂直子串重叠格子的数目](https://zhuanlan.zhihu.com/p/1904704330398930155) · 知乎 · 2025-05-13 · 赞同 0**
> 力扣：[3529. 统计水平子串和垂直子串重叠格子的数目](https://leetcode.cn/problems/count-cells-in-overlapping-horizontal-and-vertical-substrings/) · Medium · 灵茶山艾府：[KMP + 差分数组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3529.统计水平子串和垂直子串重叠格子的数目

[3529. 统计水平子串和垂直子串重叠格子的数目 - 力扣（LeetCode）](https://leetcode.cn/problems/count-cells-in-overlapping-horizontal-and-vertical-substrings/description/)

题目给出一个由字符组成的m \* n的矩阵grid，以及一个字符串pattern，其中m \* n的规模可达10^5，pattern的长度小于等于m \* n。

水平子串指的是从左到右的一段连续字符序列。如果子串到达了某行的末尾，它将换行并从下一行的第一个字符继续。不能从最后一行回到第一行。

垂直子串的定义与水平子串类似，顺序是从上往下，如果子串到达了某列的末尾，将从下一列的第一个字符继续。同样不能从最后一列回到第一列。

现在要求计算矩阵中符合条件的单元格数量，这些单元格必须属于至少一个等于pattern的水平子串，以及至少一个等于parttern的垂直子串。

可以发现，题目中的水平子串实际上就是将grid按行拉直后得到的字符串中的子串，而垂直子串则是将grid按列拉直后得到的字符串中的子串，那么在这里就可以先用kmp找出所有等于pattern的水平子串以及竖直子串，使用两个集合hit_row和hit_col分别记录这些子串在拉直后的水平字符串以及垂直字符串中的下标。需要特别注意的是，这些子串可能互相重叠，因此在记录时需要使用一个变量start记录下一次记录的起点，接下来的记录将从start和下一个等于pattern的子串的起点这二者中的较大值开始，而在完成一次记录后，还需要将start更新为当前这个子串的终点加1。

计算完成后，再遍历grid中的每个单元格，分别计算其在拉直后的水平字符串中的下标以及其在拉直后的垂直字符串中的下标，若这两个下标分别出现在hit_row和hit_col中，说明这个单元格符合条件，将答案加上1即可。

在具体实现上，并不需要真的将矩阵拉直得到字符串，而是分别按照行和列的顺序在矩阵中执行与pattern的匹配即可。另外对于下标的计算，位于矩阵中(i, j)的字符在水平字符串和垂直字符串中的下标分别是i \* n + j以及j \* m + i。

最后附上python代码：

```python
class Solution(object):
    def countCells(self, grid, pattern):
        """
        :type grid: List[List[str]]
        :type pattern: str
        :rtype: int
        """

        f = [0]
        p = 0
        for index in range(1, len(pattern)):
            while p and pattern[p] != pattern[index]:
                p = f[p - 1]
            
            if pattern[p] == pattern[index]:
                p += 1
            f.append(p)
        
        m = len(grid)
        n = len(grid[0])
        
        hit_row = set()
        p = 0
        start = 0
        for i in range(m):
            for j in range(n):
                while p and pattern[p] != grid[i][j]:
                    p = f[p - 1]
                
                if pattern[p] == grid[i][j]:
                    p += 1
                    if p == len(pattern):
                        now = i * n + j
                        for index in range(max(start, now - len(pattern) + 1), now + 1):
                            hit_row.add(index)
                        start = now + 1
                        p = f[p - 1]
        
        hit_col = set()
        p = 0
        start = 0
        for j in range(n):
            for i in range(m):
                while p and pattern[p] != grid[i][j]:
                    p = f[p - 1]
                
                if pattern[p] == grid[i][j]:
                    p += 1
                    if p == len(pattern):
                        now = j * m + i
                        for index in range(max(start, now - len(pattern) + 1), now + 1):
                            hit_col.add(index)
                        start = now + 1
                        p = f[p - 1]
        
        res = 0
        for i in range(m):
            for j in range(n):
                if i * n + j in hit_row and j * m + i in hit_col:
                    res += 1
        
        return res
```
