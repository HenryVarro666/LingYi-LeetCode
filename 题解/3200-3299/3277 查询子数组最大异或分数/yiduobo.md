---
title: "3277. 查询子数组最大异或值"
aliases: ["yiduobo的每日leetcode 3277.查询子数组最大异或值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/八-区间-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/794254810"
zhihu_id: "794254810"
zhihu_title: "yiduobo的每日leetcode 3277.查询子数组最大异或值"
question_id: "3277"
question: "查询子数组最大异或分数"
problem_url: "https://leetcode.cn/problems/maximum-xor-score-subarray-queries/"
difficulty: "Hard"
rating: 2693
created: "2024-10-04T01:36:29+08:00"
updated: "2024-10-04T01:36:29+08:00"
upvotes: 0
comments: 0
---

# 3277. 查询子数组最大异或值

> **[yiduobo的每日leetcode 3277.查询子数组最大异或值](https://zhuanlan.zhihu.com/p/794254810) · 知乎 · 2024-10-04 · 赞同 0**
> 力扣：[3277. 查询子数组最大异或分数](https://leetcode.cn/problems/maximum-xor-score-subarray-queries/) · Hard · 灵茶山艾府：[区间 DP 套区间 DP（Python/Java/C++/Go）](灵茶山艾府.md)

9祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3277.查询子数组最大异或值

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-xor-score-subarray-queries/)

定义数组的异或值为对于数组a，若a的长度大于1，那么就对除最后一个元素之外的每个a[i]都执行a[i] ^\= a[i + 1]，然后将最后这个元素从数组a中删去，重复这个过程直到a中只剩下一个元素，此时这个元素就是a的异或值。

接下来给出一个长度为n的自然数数组nums，以及一个询问数组queries，对于queries\[i\] \= \[l\[i\], r\[i\]\]，问对于nums\[l\[i\] : r\[i\] + 1\]这个子数组，其中任意子数组的异或值的最大值是多少。

题目中的n \<\= 2000。

从数据规模来看，O(n^2)的区间动态规划应该是比较合适的，而状态的定义也十分明确，首先需要f[i][j]表示数组从i到j这一段的异或值，然后需要g[i][j]表示i到j这一段子数组中任意子数组的异或值的最大值。

对于g[i][j]的求解是比较直观的，即g[i][j] \= max(f[i][j], g[i + 1][j], g[i][j - 1])，即异或值最大值的子数组，要么起点为i终点为j，要么就是所有起点大于i且终点小于等于j的子数组之一，要么是起点大于等于i终点小于j的子数组之一。

而对于f[i][j]的求解，则可以尽量往这上面去靠拢，即尝试通过f[i + 1][j]以及f[i][j - 1]来处理。

不妨先看看f[i][j]以及f[i][j - 1]之间的关系，从状态表示上可以理解成在抛开了nums[j]后，nums[i : j + 1]这一段的异或值将会变成什么样。

由于f[i][j]按题目给出的计算方法一共需要计算j - i轮，而在最后一轮之前，都可以改成认为是a[-1] ^ a[-2]，然后占据了a[-2]的位置并删掉了a[-2]，而不是a[-2]^a[-1]然后删掉了a[-1]，也就是说实际上在最后一轮之前，完全可以认为是数组除nums[j]之外的元素在做上面的操作，刚好就对应上f[i][j - 1]的定义。

那么对于nums[j]参与的运算又应该如何理解呢？答案很简单，因为i和j在计算nums[i : j + 1]的异或值时处于完全对称的地位，而nums[i]参与的运算结果刚好就是f[i][j - 1]，因此nums[j]参与的运算结果一定是f[i + 1][j]。

也就是说，在这里就有f[i][j] \= f[i][j - 1] ^ f[i + 1][j]。

到了这里，就得到了一种可行的算法。

先从1到n枚举子数组的长度length，接下来枚举子数组的起点i，通过i + length - 1计算子数组的终点j。若i \= j，那么f[i][j]和g[i][j]都等于nums[i]，否则就使用上面得到的结论，先计算f[i][j]，然后计算g[i][j]。

计算完成后，遍历queries，对于当前询问的区间[x, y]，g[x][y]就是对应的答案。

最后附上python代码：

```python
class Solution(object):
    def maximumSubarrayXor(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        n = len(nums)
        f = [[0] * n for _ in range(n)]
        g = [[0] * n for _ in range(n)]
        for length in range(1, n + 1):
            for i in range(n):
                j = i + length - 1
                if j >= n:
                    break
                if i == j:
                    f[i][j] = nums[i]
                    g[i][j] = nums[i]
                else:
                    f[i][j] = f[i + 1][j] ^ f[i][j - 1]
                    g[i][j] = max(f[i][j], g[i + 1][j], g[i][j - 1])

        res = []
        for x, y in queries:
            res.append(g[x][y])
        
        return res
```
