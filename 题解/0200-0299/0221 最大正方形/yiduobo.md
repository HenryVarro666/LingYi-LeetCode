---
title: "221. 最大正方形"
aliases: ["yiduobo的每日leetcode 221.最大正方形"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/monotonic-stack", "题单/动态规划", "题单/单调栈", "题单/面试经典-150-题", "题单/动态规划/七-其他线性-DP", "题单/单调栈/二-矩形", "题单/面试经典-150-题/多维动态规划"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/148809978"
zhihu_id: "148809978"
zhihu_title: "yiduobo的每日leetcode 221.最大正方形"
question_id: "221"
question: "最大正方形"
problem_url: "https://leetcode.cn/problems/maximal-square/"
difficulty: "Medium"
created: "2020-06-16T23:42:21+08:00"
updated: "2020-06-16T23:42:21+08:00"
upvotes: 0
comments: 0
---

# 221. 最大正方形

> **[yiduobo的每日leetcode 221.最大正方形](https://zhuanlan.zhihu.com/p/148809978) · 知乎 · 2020-06-16 · 赞同 0**
> 力扣：[221. 最大正方形](https://leetcode.cn/problems/maximal-square/) · Medium · 灵茶山艾府：[【图解】两种方法：动态规划/单调栈（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

221.最大正方形<https://leetcode-cn.com/problems/maximal-square/>

经典的动态规划问题。

设f[i][j]表示以坐标(i, j)为右下角的最大正方形的边长，那么有：

1、若matrix[i][j] \= 0，那么f[i][j]就只能为0

2、若matrix[i][j] \= 1，且i为0或者j为0，说明此时位于边界上，那么f[i][j]\=1，表示matrix[i][j]这个边长为1的小正方形

3、若matrix[i][j] \= 1，且i和j都大于0，那么需要考察以(i - k，j - k)为左上角，(i, j)为右下角的正方形里面是不是都是1，这里可以通过考察f[i - 1][j]，f[i][j - 1]以及f[i - 1][j - 1]是否达到了k来判断，换言之，就可以通过min(f[i - 1][j]，f[i][j - 1]，f[i - 1][j - 1])来判断当前以matrix[i][j]为右下角的正方形能到达多远，那么就有f[i][j] \= min(f[i - 1][j]，f[i][j - 1]，f[i - 1][j - 1]) + 1

二重循环扫描下来，最后的时间复杂度为O(mn)。空间方面可以利用滚动数组，方便起见这里就直接用二维数组来实现了。

最后附上python代码：

```python
class Solution(object):
    def maximalSquare(self, matrix):
        """
        :type matrix: List[List[str]]
        :rtype: int
        """

        if not matrix:
            return 0

        m = len(matrix)
        n = len(matrix[0])

        f = [[0] * n for _ in range(m)]
        res = 0

        for i in range(m):
            for j in range(n):
                if matrix[i][j] == '1':
                    if i == 0 or j == 0:
                        f[i][j] = 1
                    else:
                        f[i][j] = min(f[i][j - 1], f[i - 1][j], f[i - 1][j - 1]) + 1
                    res = max(res, f[i][j])

        return res * res
```
