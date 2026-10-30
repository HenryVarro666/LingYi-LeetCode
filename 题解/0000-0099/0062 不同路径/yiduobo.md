---
title: "62. 不同路径"
aliases: ["yiduobo的每日leetcode 62.不同路径"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "leetcode/combinatorics", "题单/动态规划", "题单/数学算法", "题单/LeetCode-热题-100", "题单/动态规划/二-网格图-DP", "题单/数学算法/二-组合数学", "题单/LeetCode-热题-100/多维动态规划"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/129366399"
zhihu_id: "129366399"
zhihu_title: "yiduobo的每日leetcode 62.不同路径"
question_id: "62"
question: "不同路径"
problem_url: "https://leetcode.cn/problems/unique-paths/"
difficulty: "Medium"
created: "2020-04-12T22:56:16+08:00"
updated: "2020-04-12T22:56:16+08:00"
upvotes: 0
comments: 0
---

# 62. 不同路径

> **[yiduobo的每日leetcode 62.不同路径](https://zhuanlan.zhihu.com/p/129366399) · 知乎 · 2020-04-12 · 赞同 0**
> 力扣：[62. 不同路径](https://leetcode.cn/problems/unique-paths/) · Medium · 灵茶山艾府：[两种方法：动态规划 / 组合数学（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

62.不同路径<https://leetcode-cn.com/problems/unique-paths/>

经典的动态规划问题，当然也可以通过排列组合的方式，用二项式定理解决问题。

这里用的是排列组合的方法。注意到这里从左上角走到右下角，一定是往右走了m - 1步，往下走了n - 1步，其中m和n分别为矩形的列数和行数。

于是可以看成，一共m + n - 2个球中，有m - 1个白球，n - 1个黑球，问有多少种排列的情况，因此最终的答案就是C(m + n - 2，m - 1)。

最后附上python代码：

```python
class Solution(object):
    def uniquePaths(self, m, n):
        """
        :type m: int
        :type n: int
        :rtype: int
        """

        if m == 0 or n == 0:
            return 0

        m = m + n - 2
        n -= 1
        res = 1
        for index in range(1, n + 1):
            now = m - n + index
            res = res * now / index

        return res
```
