---
title: "3643. 垂直翻转子矩阵"
aliases: ["yiduobo的每日leetcode 3643.垂直翻转子矩阵"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/two-pointers", "leetcode/simulation", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1948041102889293331"
zhihu_id: "1948041102889293331"
zhihu_title: "yiduobo的每日leetcode 3643.垂直翻转子矩阵"
question_id: "3643"
question: "垂直翻转子矩阵"
problem_url: "https://leetcode.cn/problems/flip-square-submatrix-vertically/"
difficulty: "Easy"
rating: 1235
created: "2025-09-07T15:19:03+08:00"
updated: "2025-09-07T15:19:04+08:00"
upvotes: 0
comments: 0
---

# 3643. 垂直翻转子矩阵

> **[yiduobo的每日leetcode 3643.垂直翻转子矩阵](https://zhuanlan.zhihu.com/p/1948041102889293331) · 知乎 · 2025-09-07 · 赞同 0**
> 力扣：[3643. 垂直翻转子矩阵](https://leetcode.cn/problems/flip-square-submatrix-vertically/) · Easy · 灵茶山艾府：[双指针（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3643.垂直翻转子矩阵

<https://leetcode.cn/problems/flip-square-submatrix-vertically/description/>

题目给出一个m \* n的整数矩阵grid，以及三个整数x、y和k。整数x和y表示一个正方形子矩阵的左上角下标，整数k表示该正方形子矩阵的边长。现在要求垂直翻转子矩阵的行顺序，返回更新后的矩阵。

子矩阵的左上角为(x, y)，那么矩阵最上面的行是x，最下面的行则为x + k - 1，于是可以设置两个变量top和bottom，从上下两侧向中靠拢。若top和bottom不同，则交换这两行中y到y + k - 1这一段元素，然后top向下移动，bottom向上移动，直到top大于等于bottom为止。

最后附上python代码：

```python
class Solution(object):
    def reverseSubmatrix(self, grid, x, y, k):
        """
        :type grid: List[List[int]]
        :type x: int
        :type y: int
        :type k: int
        :rtype: List[List[int]]
        """
        
        top = x
        bottom = x + k - 1
        while top < bottom:
            for index in range(y, y + k):
                grid[top][index], grid[bottom][index] = grid[bottom][index], grid[top][index]
            top += 1
            bottom -= 1
        
        return grid
```
