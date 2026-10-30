---
title: "3071. 在矩阵中写出字母Y所需的最少操作次数"
aliases: ["yiduobo的每日leetcode 3071.在矩阵中写出字母Y所需的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/697379285"
zhihu_id: "697379285"
zhihu_title: "yiduobo的每日leetcode 3071.在矩阵中写出字母Y所需的最少操作次数"
question_id: "3071"
question: "在矩阵上写出字母 Y 所需的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-write-the-letter-y-on-a-grid/"
difficulty: "Medium"
created: "2024-05-13T03:12:26+08:00"
updated: "2024-05-13T03:12:26+08:00"
upvotes: 1
comments: 0
---

# 3071. 在矩阵中写出字母Y所需的最少操作次数

> **[yiduobo的每日leetcode 3071.在矩阵中写出字母Y所需的最少操作次数](https://zhuanlan.zhihu.com/p/697379285) · 知乎 · 2024-05-13 · 赞同 1**
> 力扣：[3071. 在矩阵上写出字母 Y 所需的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-write-the-letter-y-on-a-grid/) · Medium · 灵茶山艾府：[一次遍历，以及更大值域怎么做（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3071.在矩阵中写出字母Y所需的最少操作次数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-write-the-letter-y-on-a-grid/description/)

一趟遍历，统计每种数字在Y上出现的次数以及在其他位置上出现的次数，接下来只需枚举最终构造的Y上的数字以及其他位置上的数字，然后分别计算填充Y和其他位置需要多少次操作即可。

具体来说，Y这个位置由上半部分的两条对角线以及下半部分的中线构成，也就是当坐标(i, j)中的i \<\= n / 2时，若i等于j或者i等于n - j - 1，那么就位于Y的上半部分；反过来，若i > n / 2时，若j位于n / 2时，那么就位于Y的下半部分。根据这个方法判断每个单元格是否位于Y上然后统计各种数子出现的次数即可。

接下来，Y上的单元格一共有n + n / 2个，其中前面的n来自上半部分两条对角线形成的v子形，因为每一列都有且仅有一个，因此一共是n个。而后面的n / 2则来自于下半部分的中线，其长度就相当于下半部分的长度n / 2。得到Y的单元格数量y_size后，使用n \* n减去y_size就可以得到其他位置上的单元格数量。

得到单元格数量后，分别枚举Y和其他位置上的数字，然后通过区域单元格总数减去区域现有数字的数量就得到了构造当前区域所需的操作数，两个区域所需的操作数相加后再更新答案。

最后附上python代码：

```python
class Solution(object):
    def minimumOperationsToWriteY(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        freq_y = [0] * 3
        freq_other = [0] * 3

        n = len(grid)
        for i in range(n):
            for j in range(n):
                if i <= n // 2:
                    if i == j or i == n - 1 - j:
                        freq_y[grid[i][j]] += 1
                    else:
                        freq_other[grid[i][j]] += 1
                else:
                    if j == n // 2:
                        freq_y[grid[i][j]] += 1
                    else:
                        freq_other[grid[i][j]] += 1
        
        res = n * n
        y_size = n + n // 2
        for y in range(3):
            for other in range(3):
                if y == other:
                    continue
                res = min(res, y_size - freq_y[y] + n * n - y_size - freq_other[other])
        
        return res
```
