---
title: "1727. 重新排列后的最大子矩阵"
aliases: ["yiduobo的每日leetcode 1727.重新排列后的最大子矩阵"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/enumeration", "leetcode/sorting", "题单/单调栈", "题单/贪心算法", "题单/单调栈/二-矩形", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/452018694"
zhihu_id: "452018694"
zhihu_title: "yiduobo的每日leetcode 1727.重新排列后的最大子矩阵"
question_id: "1727"
question: "重新排列后的最大子矩阵"
problem_url: "https://leetcode.cn/problems/largest-submatrix-with-rearrangements/"
difficulty: "Medium"
rating: 1927
created: "2021-12-31T12:52:33+08:00"
updated: "2021-12-31T12:52:34+08:00"
upvotes: 0
comments: 0
---

# 1727. 重新排列后的最大子矩阵

> **[yiduobo的每日leetcode 1727.重新排列后的最大子矩阵](https://zhuanlan.zhihu.com/p/452018694) · 知乎 · 2021-12-31 · 赞同 0**
> 力扣：[1727. 重新排列后的最大子矩阵](https://leetcode.cn/problems/largest-submatrix-with-rearrangements/) · Medium · 灵茶山艾府：[枚举子矩形的底边 + O(mn) 优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1727.重新排列后的最大子矩阵

[力扣](https://leetcode-cn.com/problems/largest-submatrix-with-rearrangements/)

本题与之前遇到过的85题非常像（传送门在这里[yiduobo：yiduobo的每日leetcode 85.最大矩形](https://zhuanlan.zhihu.com/p/134180401)），做法也类似，从上往下一次将当前的行加入，然后考察以当前行为下边的最大子矩阵的大小是多少。

对于新加入的第i行，首先需要计算每个位置可以向上延伸的最大高度height[i]。这个值可以根据上一行的最大延伸高度height[i - 1]以及当前位置上的值计算得到。

得到每个位置可以向上延伸的最大高度之后，就可以将所有位置按照向上可以延伸的高度从大到小进行排序，然后一趟扫描。对于当前位置j而言，显然是有height[i][0] >\= height[i][1] >\= ... >\= height[i][j]，因此以当前位置作为右下角的最大矩形面积就是(j + 1) \* height[i][j]。

由于这里每一行的height只与上一行有关，因此可以省去i这一维。

最后附上python代码：

```python
class Solution(object):
    def largestSubmatrix(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: int
        """

        m = len(matrix)
        n = len(matrix[0])
        height = [0] * n
        res = 0
        for i in range(m):
            for j in range(n):
                if matrix[i][j]:
                    height[j] += 1
                else:
                    height[j] = 0
            
            for j, h in enumerate(sorted(height, reverse=True)):
                res = max(res, (j + 1) * h)

        return res
```
