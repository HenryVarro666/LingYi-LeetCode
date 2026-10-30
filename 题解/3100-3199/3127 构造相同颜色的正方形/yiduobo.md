---
title: "3127. 构造相同颜色的正方形"
aliases: ["yiduobo的每日leetcode 3127.构造相同颜色的正方形"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/702084465"
zhihu_id: "702084465"
zhihu_title: "yiduobo的每日leetcode 3127.构造相同颜色的正方形"
question_id: "3127"
question: "构造相同颜色的正方形"
problem_url: "https://leetcode.cn/problems/make-a-square-with-the-same-color/"
difficulty: "Easy"
created: "2024-06-06T23:32:33+08:00"
updated: "2024-06-06T23:32:33+08:00"
upvotes: 0
comments: 0
---

# 3127. 构造相同颜色的正方形

> **[yiduobo的每日leetcode 3127.构造相同颜色的正方形](https://zhuanlan.zhihu.com/p/702084465) · 知乎 · 2024-06-06 · 赞同 0**
> 力扣：[3127. 构造相同颜色的正方形](https://leetcode.cn/problems/make-a-square-with-the-same-color/) · Easy · 灵茶山艾府：[遍历统计（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3127.构造相同颜色的正方形

[. - 力扣（LeetCode）](https://leetcode.cn/problems/make-a-square-with-the-same-color/description/)

题目给出一个大小为3\*3的黑白矩阵，可以修改其中至多一个格子的颜色，问能否得到一个2\*2的纯色正方形。

如果本来就存在2\*2的纯色正方形，那么答案显然为true。另外，如果存在有三个格子同色的2\*2正方形，只需修改不同色的那一个格子同样可以得到纯色正方形。于是只需遍历所有的2\*2正方形，计算其中黑色和白色单元格的数量，若任意色的格子数量大于等于3个，那么就返回true。

最后附上python代码：

```python
class Solution(object):
    def canMakeSquare(self, grid):
        """
        :type grid: List[List[str]]
        :rtype: bool
        """

        for i in range(2):
            for j in range(2):
                w = b = 0
                for x in range(2):
                    for y in range(2):
                        if grid[i + x][j + y] == 'W':
                            w += 1
                        else:
                            b += 1
                
                if w >= 3 or b >= 3:
                    return True
        
        return False
```
