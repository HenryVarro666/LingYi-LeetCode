---
title: "2906. 构造乘积矩阵"
aliases: ["yiduobo的每日leetcode 2906.构造乘积矩阵"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/动态规划", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/664007721"
zhihu_id: "664007721"
zhihu_title: "yiduobo的每日leetcode 2906.构造乘积矩阵"
question_id: "2906"
question: "构造乘积矩阵"
problem_url: "https://leetcode.cn/problems/construct-product-matrix/"
difficulty: "Medium"
rating: 2075
created: "2023-10-30T03:32:32+08:00"
updated: "2023-10-30T03:32:32+08:00"
upvotes: 0
comments: 0
---

# 2906. 构造乘积矩阵

> **[yiduobo的每日leetcode 2906.构造乘积矩阵](https://zhuanlan.zhihu.com/p/664007721) · 知乎 · 2023-10-30 · 赞同 0**
> 力扣：[2906. 构造乘积矩阵](https://leetcode.cn/problems/construct-product-matrix/) · Medium · 灵茶山艾府：[前后缀分解（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2906.构造乘积矩阵

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/construct-product-matrix/)

题目虽然给出的是矩阵，但是实际上对于每个位置的结果计算都要求其他位置的数参与进来，同时在计算时并没有涉及到矩阵横纵坐标相关的东西，因此在这里可以先将这个矩阵拉直，将其变为一个m \* n的一维数组然后求解。

接下来，只需正反两趟遍历，计算前缀乘积数组prefix和后缀乘积数组suffix，然后再一趟遍历，利用prefix[index - 1] \* suffix[index + 1]来计算index这个位置对应的答案，然后按照先行后列的方式将答案填充回矩阵中即可。

最后附上python代码：

```python
class Solution(object):
    def constructProductMatrix(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: List[List[int]]
        """

        nums = []
        m = len(grid)
        n = len(grid[0])
        for i in range(m):
            for j in range(n):
                nums.append(grid[i][j])
        
        mod = 12345
        prefix = [nums[0] % mod]
        for index in range(1, m * n):
            prefix.append(prefix[-1] * nums[index] % mod)
        
        suffix = [nums[-1] % mod]
        for index in range(m * n - 2, -1, -1):
            suffix.append(suffix[-1] * nums[index] % mod)
        suffix.reverse()

        res = []
        for index in range(m * n):
            if index % n == 0:
                res.append([])
            v = 1
            if index > 0:
                v = v * prefix[index - 1] % mod
            if index < m * n - 1:
                v = v * suffix[index + 1] % mod
            res[-1].append(v)
        
        return res
```
