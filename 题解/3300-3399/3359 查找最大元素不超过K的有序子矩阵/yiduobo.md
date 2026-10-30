---
title: "3359. 查找最大元素不超过K的有序子矩阵"
aliases: ["yiduobo的每日leetcode 3359.查找最大元素不超过K的有序子矩阵"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/27172472863"
zhihu_id: "27172472863"
zhihu_title: "yiduobo的每日leetcode 3359.查找最大元素不超过K的有序子矩阵"
question_id: "3359"
question: "查找最大元素不超过K的有序子矩阵"
problem_url: "https://leetcode.cn/problems/find-sorted-submatrices-with-maximum-element-at-most-k/"
created: "2025-03-01T00:25:34+08:00"
updated: "2025-03-01T00:25:56+08:00"
upvotes: 1
comments: 0
---

# 3359. 查找最大元素不超过K的有序子矩阵

> **[yiduobo的每日leetcode 3359.查找最大元素不超过K的有序子矩阵](https://zhuanlan.zhihu.com/p/27172472863) · 知乎 · 2025-03-01 · 赞同 1**
> 力扣：[3359. 查找最大元素不超过K的有序子矩阵](https://leetcode.cn/problems/find-sorted-submatrices-with-maximum-element-at-most-k/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3359.查找最大元素不超过K的有序子矩阵

[3359. 查找最大元素不超过 K 的有序子矩阵 - 力扣（LeetCode）](https://leetcode.cn/problems/find-sorted-submatrices-with-maximum-element-at-most-k/description/)

题目给出一个大小为m \* n的二维矩阵grid，同时给定一个非负整数k，要求找出满足一下条件的子矩阵数目：

1、子矩阵中的最大的元素小于等于k

2、子矩阵中的每一行都是非递增的

---

关于题目中的这两个条件，其中的非递增是与行有关的，因此在这里可以尝试先从行入手进行处理。

令f[i][j]表示以第i行，第j列为结尾，且所有元素都小于等于k的最长非递增子数组的长度，那么对于f[i][j]：

1、若grid[i][j] > k：

此时显然有f[i][j] \= 0

2、若grid[i][j] \<\= k，且j \= 0或者grid[i][j] > grid[i][j - 1]：

此时有f[i][j] \= 1，即grid[i][j]单独形成的子数组

3、若grid[i][j] \<\= k，且j > 0同时grid[i][j] \<\= grid[i][j - 1]：

此时grid[i][j]可以拼接在grid[i][j - 1]的后面，于是有f[i][j] \= f[i][j - 1] + 1

---

完成上面的预处理后，接下来就可以利用f来求解以每个位置为右下角的矩阵的数目。以样例举例，初始的grid为

| 4 | 3 | 2 | 1 |
| --- | --- | --- | --- |
| 8 | 7 | 6 | 1 |

k \= 3时计算得到的f为

| 0 | 1 | 2 | 3 |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 1 |

这样看上去不够直观，不妨设k \= 7，那么得到的f就是

| 1 | 2 | 3 | 4 |
| --- | --- | --- | --- |
| 0 | 1 | 2 | 3 |

可以发现，f[i][j]表示的就是对于j这一列，在i这一行上最多可以向左扩展的列数，因此以(i, j)为右下角的子矩阵数量实际上受限于j这一列中，前一个值小于f[i][j]的行p，那么：

1、从p + 1到i，这些行对应的f[p + 1][j]、f[p + 2][j]、...、f[i][j]都大于等于f[i][j]，也就是说以(i, j)为右下角的矩阵，且左上角在这些行中时，子矩阵可以向左扩展f[i][j]列，一共可以形成(i - p) \* f[i][j]个子矩阵。

2、另一方面，当子矩阵的左上角位于第0到第p行时，由于这些行对应的f[p + 1][j]、f[p + 2][j]、...、f[i][j]也都大于f[p][j]，因此肯定是无法向左扩展f[i][j]列的，不过在这里可以利用之前已经计算得到的结果。不妨设以f[p][j]为右下角可以形成的子矩阵数量为g[p][j]，由于从p + 1行到第i行可以向左扩展的列数都足够，那么对于g[p][j]中的每个子矩阵，都存在一个以(i, j)为右下角的对应子矩阵，因此一共有g[p][j]个子矩阵。由于g[p][j]也可以认为是一个软上限，因此也不存在遗漏的情况。

上面两种情况的结果累加起来，即为以(i, j)为右下角的合法子矩阵数目g[i][j]，将所有的g[i][j]累加起来即为最终答案。

对于同一列中上一个较小值行的这个问题，利用单调栈进行求解。于是可以遍历每一列，接下来对于每一列，在遍历每一行同时利用单调栈计算以当前位置为右下角的合法子矩阵数目即可。

最后附上python代码：

```python
class Solution(object):
    def countSubmatrices(self, grid, k):
        """
        :type grid: List[List[int]]
        :type k: int
        :rtype: int
        """
        
        m = len(grid)
        n = len(grid[0])

        f = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if grid[i][j] <= k:
                    if j > 0 and grid[i][j] <= grid[i][j - 1]:
                        f[i][j] = f[i][j - 1] + 1
                    else:
                        f[i][j] = 1
        
        g = [[0] * n for _ in range(m)]
        res = 0
        for j in range(n):
            stack = []
            for i in range(m):
                while stack and f[i][j] < f[stack[-1]][j]:
                    stack.pop()

                if stack:
                    g[i][j] = g[stack[-1]][j] + (i - stack[-1]) * f[i][j]
                else:
                    g[i][j] = (i + 1) * f[i][j]
                
                stack.append(i)
                res += g[i][j]
        
        return res
```
