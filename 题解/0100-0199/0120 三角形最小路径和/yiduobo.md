---
title: "120. 三角形最小路径和"
aliases: ["yiduobo的每日leetcode 120.三角形最小路径和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/面试经典-150-题", "题单/动态规划/二-网格图-DP", "题单/面试经典-150-题/多维动态规划"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/139524249"
zhihu_id: "139524249"
zhihu_title: "yiduobo的每日leetcode 120.三角形最小路径和"
question_id: "120"
question: "三角形最小路径和"
problem_url: "https://leetcode.cn/problems/triangle/"
difficulty: "Medium"
created: "2020-05-10T22:12:34+08:00"
updated: "2020-05-10T22:12:34+08:00"
upvotes: 0
comments: 0
---

# 120. 三角形最小路径和

> **[yiduobo的每日leetcode 120.三角形最小路径和](https://zhuanlan.zhihu.com/p/139524249) · 知乎 · 2020-05-10 · 赞同 0**
> 力扣：[120. 三角形最小路径和](https://leetcode.cn/problems/triangle/) · Medium · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推到空间优化！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

120.三角形最小路径和<https://leetcode-cn.com/problems/triangle/>

经典的动态规划题。

首先我们调整一下三角形的样式变成左对齐便于观察，比如说样例我们将其调整如下：

2

3 4

6 5 7

4 1 8 3

考察以第i行第j个数为结尾的路径：

1、当j为0时，只能从上一层的最左侧下来，即从第i - 1行的第0个数走下来。

2、当j等于i时，只能从上一层的最右侧下来，即从第i - 1行的第j - 1个数走下来。

3、其他情况，都可能从上一层的第j - 1个数或者上一层的第j个数走下来。

于是可以设置状态f[i][j]表示从三角形顶部到第i层第j个数形成的路径中最小路径和是多少，那么：

1、当j为0时，f[i][j] \= f[i - 1][j] + triangle[i][j]

2、当j等于i时，f[i][j] \= f[i - 1][j - 1] + triangle[i][j]

3、其他情况，f[i][j] \= min(f[i - 1][j - 1]，f[i - 1][j]) + triangle[i][j]

可以发现状态转移过程中只与上一层的结果有关，于是可以使用滚动数组来优化空间。

另外，我在这里使用了一个省事但是不优美的写法，即在计算完每一层的f之后，在最后添加上一个maxint。

这样一来，对于j \= 0的情况，f[i - 1][j - 1]对应到的是f[i - 1][-1]即最后添加的maxint，而对于j \= i - 1的情况，f[i - 1][j]同样是对应到这个最后添加的maxint。于是，上面的三种情况都可以通过情况3的状态转移方程覆盖住了。

最后附上python代码：

```python
class Solution(object):
    def minimumTotal(self, triangle):
        """
        :type triangle: List[List[int]]
        :rtype: int
        """

        if not triangle:
            return 0

        f = [triangle[0][0], 2147483647]

        for i in range(1, len(triangle)):
            f = [min(f[j - 1], f[j]) + triangle[i][j] for j in range(i + 1)] + [2147483647]
        return min(f)
```
