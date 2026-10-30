---
title: "3122. 使矩阵满足条件的最少操作次数"
aliases: ["yiduobo的每日leetcode 3122.使矩阵满足条件的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/di-tui", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/701661205"
zhihu_id: "701661205"
zhihu_title: "yiduobo的每日leetcode 3122.使矩阵满足条件的最少操作次数"
question_id: "3122"
question: "使矩阵满足条件的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-operations-to-satisfy-conditions/"
difficulty: "Medium"
rating: 1905
created: "2024-06-04T22:49:41+08:00"
updated: "2024-06-04T22:49:41+08:00"
upvotes: 1
comments: 0
---

# 3122. 使矩阵满足条件的最少操作次数

> **[yiduobo的每日leetcode 3122.使矩阵满足条件的最少操作次数](https://zhuanlan.zhihu.com/p/701661205) · 知乎 · 2024-06-04 · 赞同 1**
> 力扣：[3122. 使矩阵满足条件的最少操作次数](https://leetcode.cn/problems/minimum-number-of-operations-to-satisfy-conditions/) · Medium · 灵茶山艾府：[两种方法：记忆化搜索/递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3122.使矩阵满足条件的最少操作次数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-number-of-operations-to-satisfy-conditions/description/)

题目给出一个由0到9组成的，大小为m \* n的矩阵grid。每次操作可以将矩阵中任意位置的数修改成任意整数，问最少使用多少次操作，可以使得对于矩阵中的每个位置上的元素，其数值都与上下相邻的元素相等，但是与左右相邻的元素不同。

每个元素都与上下相邻的元素相等，就意味着最终矩阵中的同一列的值都相同，而矩阵中数值的取值范围在0到9之间，那么最终修改的目的也必然在0到9之间，于是可以使用f[i][j]表示修改好第0到第i列，其中第i列的值为j时需要的最小代价。

那么对于f[i][j]，可以从0到9枚举第i - 1列的取值p，就有

f[i][j] \= min(f[i - 1][p]) + m - freq[i][j]，其中p与j不同。

freq[i][j]则表示在原始矩阵中，第i列中j出现的次数，那么将第i列全部变为j需要m - freq[i][j]次操作。

注意到上面的状态转移过程总是从上一列中不等于j的位置中的最优值转移得到的，那么就可以维护上一列的最优值以及次优值，若当前的j等于上一列的最优值，就只能从上一列的次优值转移过来，否则就可以从上一列的最优值转移过来，因此在这里不需要j这一维，只需要保留最优和次有的两个数值以及这两数值对应的操作数就行了。

另一方面，由于每一轮的值仅与上一轮有关，因此也可以通过滚动省去i这一维。

最后附上python代码：

```python
class Solution(object):
    def minimumOperations(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])

        first_f = 0
        first_v = 0
        second_f = 0
        second_v = 1

        for j in range(n):
            pre_first_f, pre_first_v = first_f, first_v
            pre_second_f, pre_second_v = second_f, second_v
            first_f = second_f = -1

            freq = Counter()
            for i in range(m):
                freq[grid[i][j]] += 1
            
            for v in range(10):
                cost = m - freq[v]
                if v != pre_first_v:
                    f = pre_first_f + cost
                else:
                    f = pre_second_f + cost
                
                if first_f == -1 or f < first_f:
                    first_f, second_f = f, first_f
                    first_v, second_v = v, first_v
                elif second_f == -1 or f < second_f:
                    second_f = f
                    second_v = v
        
        return first_f
```
