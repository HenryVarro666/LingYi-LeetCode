---
title: "2478. 完美分割的方案数"
aliases: ["yiduobo的每日leetcode 2478.完美分割的方案数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/五-划分型-DP", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/589004282"
zhihu_id: "589004282"
zhihu_title: "yiduobo的每日leetcode 2478.完美分割的方案数"
question_id: "2478"
question: "完美分割的方案数"
problem_url: "https://leetcode.cn/problems/number-of-beautiful-partitions/"
difficulty: "Hard"
rating: 2344
created: "2022-12-04T04:03:04+08:00"
updated: "2022-12-04T04:03:04+08:00"
upvotes: 0
comments: 0
---

# 2478. 完美分割的方案数

> **[yiduobo的每日leetcode 2478.完美分割的方案数](https://zhuanlan.zhihu.com/p/589004282) · 知乎 · 2022-12-04 · 赞同 0**
> 力扣：[2478. 完美分割的方案数](https://leetcode.cn/problems/number-of-beautiful-partitions/) · Hard · 灵茶山艾府：[动态规划 + 简洁写法 + 循环优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2478.完美分割的方案数

[力扣](https://leetcode.cn/problems/number-of-beautiful-partitions/)

二维的动态规划算法是很容想到的。令h[i][j]表示前i个字符分割成j份的方案数，那么对于h[i][j]：

1、首先是边界情况。当j \= 0时，若i \= 0，那么有h[i][j] \= 1，即对于空串不进行分割是一种合法的情况，若i > 0，那么有h[i][j] \= 0，因为每个字符都必须参与分割

2、接下来是不合法的情况：

2-1）若j \* minLength > i，那么这i个字符是不足以分割成j份的，那么h[i][j] \= 0

2-2）若s[i - 1]是质数，那么h[i][j] \= 0，因为前i个字符分割的最后一份必然是以s[i - 1]结尾的，题目要求每个分割结尾的字符都不是质数

2-3）若i + 1 \<\= n，且s[i]不是质数，那么h[i][j]同样等于0。因为后续状态的分割如果要基于h[i][j]进行，那么必然存在一个分割是以s[i]开头的，但是题目要求每个分割开头的字符是质数

3、最后则是可用的状态。此时就有

h[i][j] \= h[i - min_length - 1][j - 1] + h[i - min_length - 2][j - 1] + ... + h[0][j - 1]

在这里无需判断分割的上一段是否合法，因为在步骤2中已经自动将不合法状态置为0了，即使累加进来也不会影响最终的答案

到了这里，就得到了一个时间复杂度为O(n^2 \* k)的算法，其中状态表示为O(nk)，转移的复杂度为O(n)，需要进行优化。

注意到转移的复杂度主要集中在情况3，且这是一个非常典型的前缀和的式子，那么可以令f[i][j]表示h[0][j] + h[1][j] + ... + h[i][j]，那么只需在h[i][j]更新后立即使用h[i][j]来更新f[i][j]就行了。这样一来时间复杂度就降到了O(nk)。

加入f数组之后可以发现，时间上h数组就是用来倒腾了一下数据，那么完全可以舍去h数组，只留下f数组。

此时对于f[i][j]的处理，首先就有f[i][j] \= f[i - 1][j]，这是由于f自身的定义是一个前缀累加和。接下来对于原来h[i][j]对应的情况而言，边界情况和不合法情况的处理方法不变，而对于可用状态的转移，则有f[i][j] +\= f[i - min_length][j - 1]。

最后，注意到f数组每一轮只与上一轮有关，因此可以使用滚动数据优化掉j这一维。不过需要注意的是，在这里需要调换i和j枚举的顺序方便进行滚动。

另外需要特别注意的，在这里f的定义变成了累加，因此最后返回的结果应该是f[n - min_length]而不是f[n]。

最后附上python代码：

```python
class Solution(object):
    def beautifulPartitions(self, s, k, minLength):
        """
        :type s: str
        :type k: int
        :type minLength: int
        :rtype: int
        """

        prime_set = set(['2', '3', '5', '7'])
        if s[0] not in prime_set or s[-1] in prime_set:
            return 0
        
        mod = 10 ** 9 + 7
        n = len(s)
        if minLength * k > n:
            return 0
        
        f = [1] * (n + 1)

        for j in range(1, k + 1):
            g = f[:]
            f = [0]
            for i in range(1, n + 1):
                f.append(f[-1])
                if i >= minLength * j and s[i - 1] not in prime_set and i + 1 <= n and s[i] in prime_set:
                    f[i] += g[i - minLength]
                    if f[i] >= mod:
                        f[i] -= mod

        return g[n - minLength]
```
