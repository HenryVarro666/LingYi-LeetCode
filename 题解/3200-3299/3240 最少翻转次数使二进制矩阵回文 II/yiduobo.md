---
title: "3240. 最少翻转次数使二进制矩阵回文II"
aliases: ["yiduobo的每日leetcode 3240.最少翻转次数使二进制矩阵回文II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/bian-li", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/720795521"
zhihu_id: "720795521"
zhihu_title: "yiduobo的每日leetcode 3240.最少翻转次数使二进制矩阵回文II"
question_id: "3240"
question: "最少翻转次数使二进制矩阵回文 II"
problem_url: "https://leetcode.cn/problems/minimum-number-of-flips-to-make-binary-grid-palindromic-ii/"
difficulty: "Medium"
rating: 2080
created: "2024-09-19T01:13:13+08:00"
updated: "2024-09-19T01:13:13+08:00"
upvotes: 0
comments: 0
---

# 3240. 最少翻转次数使二进制矩阵回文II

> **[yiduobo的每日leetcode 3240.最少翻转次数使二进制矩阵回文II](https://zhuanlan.zhihu.com/p/720795521) · 知乎 · 2024-09-19 · 赞同 0**
> 力扣：[3240. 最少翻转次数使二进制矩阵回文 II](https://leetcode.cn/problems/minimum-number-of-flips-to-make-binary-grid-palindromic-ii/) · Medium · 灵茶山艾府：[分类讨论（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3240.最少翻转次数使二进制矩阵回文II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-number-of-flips-to-make-binary-grid-palindromic-ii/)

上一题的加强版。本题给出一个大小为m \* n的二进制矩阵grid，每次操作同样可以翻转grid中的任意单元格，要求计算最少的翻转次数，使得矩阵中所有行和列都是回文的，同时矩阵中1的数量是4的倍数。

题目要求矩阵所有行和列都是回文的，那么对于矩阵中的单元格，有三种情况：

1、矩阵正中心的单元格：

只有当m和n都是奇数时才有唯一的中心单元格。这个单元格不会对行和列的回文性质产生任何影响，但是由于其他位置上的回文性质决定了矩阵中1的数量一定是2的倍数，因此这个中心单元格必须为0，否则矩阵中1的数量将会是奇数，不符合4的倍数的性质。

也就是说，当m和n都为奇数，且中心单元格grid[m // 2][n // 2]为1时，需要进行一次操作将其修改为0。

2、不是矩阵正中心，但是位于矩阵中心行或者矩阵中心列上的单元格：

只有m为奇数时矩阵才有中心行，这些行的单元格不会对矩阵列的回文性质产生影响，所以只需要保证中心行本身是回文的。与上一题相同，依然可以通过从左右两侧向中间遍历的方法，计算出将中心行变为回文所需的最小操作次数。需要注意的是，这是修改次数的下限，但是由于有1的数量必须是4的倍数的限制，这个下限不一定可以达到。

同样的，只有n为奇数时矩阵才有中心列，而要使得中心列时回文所需的最小操作次数同样可以通过从上下两侧向中间遍历的方法计算得到。

关于行和列中1的数量的调配放在最后再详细说明，在这里先计算中心行以及中心列上原始就对称的1的数量one，以及是否进行过至少一次操作。

3、不处于矩阵的中心行和中心列上的单元格：

对于这类单元格，不妨设其坐标为(x, y)，那么其所在行上存在一个对称的单元格(x, y')，同时其所在列上也存在一个对称的单元格(x', y)，同时这两个单元格都与(x', y')对称。

也就是说，这四个单元格的值必须是一样的，要么全0要么全1。好消息是，只要保持了矩阵的回文性质，这部分的1的数量一定是4的倍数，因此只需要考虑使用最少的操作次数使得这些单元格满足回文性质就行了。

枚举左上部分所有的(x, y)，也就是对于所有x在0到m // 2 - 1之间，y在0到n // 2 - 1之间的单元格，这些单元格对称的(x, y') \= (x, n - 1- y)，(x', y) \= (m - 1 - x, y)，(x', y') \= (m - 1 - x, n - 1- y)。只需这四个单元格中1的数量k，那么将这四个单元格都变为0的操作次数为k，而将这些单元格都变为1的操作次数则为4 - k，取二者的较小值执行操作将四个单元格的值变为相同即可。

到了这里，就只需要考虑中心行和中心列上1应该如何调配的问题。不妨设中心行和中心列上原始就对称的1的数量为one，那么：

1、当one为4的倍数时：

只需将中心行和中心列上所有的操作都变为对称的0，这样一来既可以达到操作次数的下限，也可以满足1的数量是4的倍数。

2、如果one不是4的倍数时：

此时的one一定是2的倍数。如果中心行或者中心列上执行过至少一次操作，那么就可以将某一次操作的目标变为两个1，这样一来就可以使得1的数量是4的倍数，同时依然可以达到操作次数的下限。

反之，如果中心行和中心列上一次操作都没有执行过，那么在这里就需要两次额外操作，将中心行或者中心列上的两个对称的1都变为0，也就是说这里在操作次数下限的基础上还需要额外加上2。

最后附上python代码：

```python
class Solution(object):
    def minFlips(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        m = len(grid)
        n = len(grid[0])

        res = 0
        for i in range(m // 2):
            for j in range(n // 2):
                one = 0
                if grid[i][j] == 1:
                    one += 1
                if grid[i][n - 1 - j] == 1:
                    one += 1
                if grid[m - 1 - i][j] == 1:
                    one += 1
                if grid[m - 1 - i][n - 1 - j] == 1:
                    one += 1
                
                res += min(one, 4 - one)
        
        if m % 2 == 1 and n % 2 == 1 and grid[m // 2][n // 2] == 1:
            res += 1
        
        changed = False
        one = 0
        if m % 2 == 1:
            x = m // 2
            left, right = 0, n - 1
            while left < right:
                if grid[x][left] != grid[x][right]:
                    changed = True
                    res += 1
                elif grid[x][left] == 1:
                    one += 2
                
                left += 1
                right -= 1
        
        if n % 2 == 1:
            y = n // 2
            top, bottom = 0, m - 1
            while top < bottom:
                if grid[top][y] != grid[bottom][y]:
                    changed = True
                    res += 1
                elif grid[top][y] == 1:
                    one += 2
                
                top += 1
                bottom -= 1
        
        if one % 4 == 2 and not changed:
            res += 2
        
        return res
```
