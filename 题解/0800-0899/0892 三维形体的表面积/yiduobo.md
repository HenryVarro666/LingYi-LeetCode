---
title: "892. 三维形体的表面积"
aliases: ["yiduobo的每日leetcode 892.三维形体的表面积"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/352445118"
zhihu_id: "352445118"
zhihu_title: "yiduobo的每日leetcode 892.三维形体的表面积"
question_id: "892"
question: "三维形体的表面积"
problem_url: "https://leetcode.cn/problems/surface-area-of-3d-shapes/"
created: "2021-02-23T21:58:15+08:00"
updated: "2021-02-23T21:58:15+08:00"
upvotes: 0
comments: 0
---

# 892. 三维形体的表面积

> **[yiduobo的每日leetcode 892.三维形体的表面积](https://zhuanlan.zhihu.com/p/352445118) · 知乎 · 2021-02-23 · 赞同 0**
> 力扣：[892. 三维形体的表面积](https://leetcode.cn/problems/surface-area-of-3d-shapes/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

892.三维形体的表面积

[力扣](https://leetcode-cn.com/problems/surface-area-of-3d-shapes/)

与之前做过的三维形体视图面积类似，不过需要注意的是，这里是表面积，因此对于诸如“回”这种性质的构造而言，中间镂空的部分也是会提供表面积的。在这里我们依然是采用从上、下、左、右、前、后六个方向来看的方法来计算整个三维形体的表面积，不过这次是判断每个格子的每个方向是否会提供表面积。

对于上方和下方，若当前格子上高度不为0，那么从上方和下方将分别提供1的表面积，否则不能提供表面积。

由于前后左右的计算规则肯定是一样的，那么不妨挑选左侧来进行分析。对于grid[i][j]而言：

1、若满足j \= 0，那么说明这个格子位于左边界上，那么此时从左边来看的话，这个格子将提供其对应高度的表面积

2、若满足j !\= 0，那么其左边必然存在格子grid[i][j - 1]。当grid[i][j] \<\= grid[i][j - 1]时，grid[i][j]这个格子的左侧不能提供表面积的，否则将提供grid[i][j] - grid][i][j - 1]的表面积

我们可以对所有的格子进行上面的判断，从而得知从左侧看的表面积是多少。同理，也可以按同样的方式计算出从前、后、右侧看的表面积。

最后附上python代码：

```python
class Solution(object):
    def surfaceArea(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        res = 0
        m = len(grid)
        n = len(grid[0])

        for i in range(m):
            for j in range(n):
                if grid[i][j] > 0:
                    res += 2

                if i == 0:
                    res += grid[i][j]
                elif grid[i][j] > grid[i - 1][j]:
                    res += grid[i][j] - grid[i - 1][j]
                
                if i == m - 1:
                    res += grid[i][j]
                elif grid[i][j] > grid[i + 1][j]:
                    res += grid[i][j] - grid[i + 1][j]
                
                if j == 0:
                    res += grid[i][j]
                elif grid[i][j] > grid[i][j - 1]:
                    res += grid[i][j] - grid[i][j - 1]
                
                if j == n - 1:
                    res += grid[i][j]
                elif grid[i][j] > grid[i][j + 1]:
                    res += grid[i][j] - grid[i][j + 1]
        
        return res
```
