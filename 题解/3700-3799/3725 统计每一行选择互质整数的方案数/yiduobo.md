---
title: "3725. 统计每一行选择互质整数的方案数"
aliases: ["yiduobo的每日leetcode 3725.统计每一行选择互质整数的方案数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/dynamic-programming", "leetcode/combinatorics", "leetcode/number-theory", "题单/动态规划", "题单/数学算法", "题单/动态规划/七-其他线性-DP", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1965855700652659805"
zhihu_id: "1965855700652659805"
zhihu_title: "yiduobo的每日leetcode 3725.统计每一行选择互质整数的方案数"
question_id: "3725"
question: "统计每一行选择互质整数的方案数"
problem_url: "https://leetcode.cn/problems/count-ways-to-choose-coprime-integers-from-rows/"
difficulty: "Hard"
rating: 1982
created: "2025-10-27T19:52:18+08:00"
updated: "2025-10-27T19:52:23+08:00"
upvotes: 0
comments: 0
---

# 3725. 统计每一行选择互质整数的方案数

> **[yiduobo的每日leetcode 3725.统计每一行选择互质整数的方案数](https://zhuanlan.zhihu.com/p/1965855700652659805) · 知乎 · 2025-10-27 · 赞同 0**
> 力扣：[3725. 统计每一行选择互质整数的方案数](https://leetcode.cn/problems/count-ways-to-choose-coprime-integers-from-rows/) · Hard · 灵茶山艾府：[两种方法：动态规划 / 倍数容斥（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3725.统计每一行选择互质整数的方案数

[3725. 统计每一行选择互质整数的方案数 - 力扣（LeetCode）](https://leetcode.cn/problems/count-ways-to-choose-coprime-integers-from-rows/description/)

题目给出一个由正整数组成的m \* n的矩阵mat，其中m、n以及mat中的元素都在1到150之间。

现在要求返回一个整数，表示从mat中每一行中恰好选择一个整数，使得所有被选择的整数的最大公约数为1的选择方案数。

由于mat中元素的大小不超过150，而最大公约数只会越算越小，因此无论如何选择元素，这些元素的最大公约数都将落在1到150之间，因此可以直接将最大公约数表示在状态中，利用动态规划进行求解。

令f[index][v]表示第0到第index行中每行选择一个元素，这些元素的最大公约数为v的选择方案数是多少，那么对于index \= 0的情况，可以遍历mat[0]中的所有元素v，对于每个v，将f[0][v]加上1。接下来对于index > 0的情况，可以先枚举f[index - 1]中的所有值pre，然后枚举mat[index]这一行的所有值v，计算二者的最大公约数g，那么就可以将f[index - 1][pre]累加到f[index][g]中。

全部计算完成后，f[-1][1]即为最终答案。

由于f每一轮的值只与上一轮有关，因此可以使用数组迭代省去index这一维。另外，由于gcd可能触及到的元素有限，因此在这里使用哈希表而不是数组下标来储存状态是更好的做法。

最后附上python代码：

```python
class Solution(object):
    def countCoprime(self, mat):
        """
        :type mat: List[List[int]]
        :rtype: int
        """
        
        f = {}
        for v in mat[0]:
            f[v] = f.get(v, 0) + 1
        
        def gcd(x, y):
            while y != 0:
                x, y = y, x % y
            return x

        mod = 10 ** 9 + 7
        for line in mat[1:]:
            h = copy.deepcopy(f)
            f = {}
            for v in line:
                for pre in h:
                    g = gcd(pre, v)
                    f[g] = f.get(g, 0) + h[pre]
                    if f[g] >= mod:
                        f[g] -= mod
        
        return f.get(1, 0)
```
