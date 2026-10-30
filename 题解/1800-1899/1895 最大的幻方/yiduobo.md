---
title: "1895. 最大的幻方"
aliases: ["yiduobo的每日leetcode 1895.最大的幻方"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/479612986"
zhihu_id: "479612986"
zhihu_title: "yiduobo的每日leetcode 1895.最大的幻方"
question_id: "1895"
question: "最大的幻方"
problem_url: "https://leetcode.cn/problems/largest-magic-square/"
difficulty: "Medium"
rating: 1781
created: "2022-03-12T00:40:00+08:00"
updated: "2022-03-12T00:40:00+08:00"
upvotes: 1
comments: 0
---

# 1895. 最大的幻方

> **[yiduobo的每日leetcode 1895.最大的幻方](https://zhuanlan.zhihu.com/p/479612986) · 知乎 · 2022-03-12 · 赞同 1**
> 力扣：[1895. 最大的幻方](https://leetcode.cn/problems/largest-magic-square/) · Medium · 灵茶山艾府：[从 O(N^4) 优化到 O(N^3)（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1895.最大的幻方

[力扣](https://leetcode-cn.com/problems/largest-magic-square/)

没有什么特别好的想法，不过由于题目的数据规模并不大，因此可以选择枚举幻方的左上角(lx, ly)以及边长l，然后通过(lx, ly)以及l计算出(rx, ry)。接下来记lx这一行从rx到ry的和为s，那么后续需要验证的是lx + 1到rx这些行中从rx到ry的和是否等于s，以及ly到ry这些列中从lx到rx的和是否等于s。另外，还有两条对角线的和也需要验证。

对于行和列上的和，可以对每一行和每一列都维护一个前缀和，然后通过这个前缀和来求区间和。而对于对角线上的和，则可以在枚举每一行的过程中顺便计算。

这样一来，枚举(lx, ly)的复杂度位O(mn)，枚举l的复杂度为O(min(m, n))，而枚举每一行每一列的复杂度与枚举l的复杂度取决于l，那么在这里就有了一种四次方的算法，在数据规模在50的情况下是完全够用的。

最后附上python代码：

```python
class Solution(object):
    def largestMagicSquare(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])

        h_prefix = [[] for _ in range(m)]
        v_prefix = [[] for _ in range(n)]

        for i in range(m):
            for j in range(n):
                h_prefix[i].append(grid[i][j])
                if j > 0:
                    h_prefix[i][-1] += h_prefix[i][-2]
                
                v_prefix[j].append(grid[i][j])
                if i > 0:
                    v_prefix[j][-1] += v_prefix[j][-2]
        
        res = 1
        for lx in range(m):
            for ly in range(n):
                for l in range(2, min(m - lx, n - ly) + 1):
                    rx = lx + l - 1
                    ry = ly + l - 1
                    l_cross = grid[lx][ly]
                    r_cross = grid[lx][ry]

                    s = self.get_s(h_prefix, lx, ly, ry)

                    flag = True
                    for index in range(lx + 1, rx + 1):
                        if s != self.get_s(h_prefix, index, ly, ry):
                            flag = False
                            break
                        
                        l_cross += grid[index][ly + index - lx]
                        r_cross += grid[index][ry - index + lx]

                    if not flag:
                        continue

                    if l_cross != s or r_cross != s:
                        continue
                    
                    flag = True
                    for index in range(ly, ry + 1):
                        if s != self.get_s(v_prefix, index, lx, rx):
                            flag = False
                            break
                    
                    if flag:
                        res = max(res, l)
        
        return res

    def get_s(self, prefix, pos, l, r):
        res = prefix[pos][r]
        if l > 0:
            res -= prefix[pos][l - 1]
        
        return res
```
