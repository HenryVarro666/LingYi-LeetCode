---
title: "3239. 最少翻转次数使二进制矩阵回文I"
aliases: ["yiduobo的每日leetcode 3239.最少翻转次数使二进制矩阵回文I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/720795031"
zhihu_id: "720795031"
zhihu_title: "yiduobo的每日leetcode 3239.最少翻转次数使二进制矩阵回文I"
question_id: "3239"
question: "最少翻转次数使二进制矩阵回文 I"
problem_url: "https://leetcode.cn/problems/minimum-number-of-flips-to-make-binary-grid-palindromic-i/"
difficulty: "Medium"
created: "2024-09-19T00:46:46+08:00"
updated: "2024-09-19T00:46:46+08:00"
upvotes: 0
comments: 0
---

# 3239. 最少翻转次数使二进制矩阵回文I

> **[yiduobo的每日leetcode 3239.最少翻转次数使二进制矩阵回文I](https://zhuanlan.zhihu.com/p/720795031) · 知乎 · 2024-09-19 · 赞同 0**
> 力扣：[3239. 最少翻转次数使二进制矩阵回文 I](https://leetcode.cn/problems/minimum-number-of-flips-to-make-binary-grid-palindromic-i/) · Medium · 灵茶山艾府：[分别计算（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3239.最少翻转使二进制矩阵回文I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-number-of-flips-to-make-binary-grid-palindromic-i/description/)

题目给出一个大小m \* n的二进制矩阵grid，每次操作可以对grid中任意位置进行翻转。问至少进行多少次翻转才能使得矩阵所有行都是回文，或者所有列都是回文。

题目只需要所有行都是回文或者所有列都是回文，在这里就可以分别计算将所有行变成回文的最小代价以及将所有列变成回文的最小代价，取这两个代价中较小的即为最终答案。

对于将所有行变成回文需要的代价，可以遍历grid的每一行，对于当前行，从左右两侧向中间遍历，若对称位置上的值不相同，那么就需要进行一次修改。依照这个方法计算每一行所需的代价，累加起来就是总代价了。

同样的，对于将所有列变成回文需要的代价，则可以遍历grid的每一列，然后从上下两侧向中间遍历计算总代价。

最后附上python代码：

```python
class Solution(object):
    def minFlips(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        res = None
        m = len(grid)
        n = len(grid[0])

        cnt = 0
        for i in range(m):
            left, right = 0, n - 1
            while left < right:
                if grid[i][left] != grid[i][right]:
                    cnt += 1
                left += 1
                right -= 1
            
        res = cnt

        cnt = 0
        for j in range(n):
            top, bottom = 0, m - 1
            while top < bottom:
                if grid[top][j] != grid[bottom][j]:
                    cnt += 1
                top += 1
                bottom -= 1

        res = min(res, cnt)
        return res
```
