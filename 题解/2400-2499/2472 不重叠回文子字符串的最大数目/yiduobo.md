---
title: "2472. 不重叠回文子字符串的最大数目"
aliases: ["yiduobo的每日leetcode 2472.不重叠回文子字符串的最大数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/string", "leetcode/dynamic-programming", "题单/动态规划", "题单/字符串", "题单/动态规划/五-划分型-DP", "题单/字符串/三-Manacher-算法-回文串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/588493187"
zhihu_id: "588493187"
zhihu_title: "yiduobo的每日leetcode 2472.不重叠回文子字符串的最大数目"
question_id: "2472"
question: "不重叠回文子字符串的最大数目"
problem_url: "https://leetcode.cn/problems/maximum-number-of-non-overlapping-palindrome-substrings/"
difficulty: "Hard"
rating: 2013
created: "2022-12-02T02:21:54+08:00"
updated: "2022-12-02T02:21:54+08:00"
upvotes: 0
comments: 0
---

# 2472. 不重叠回文子字符串的最大数目

> **[yiduobo的每日leetcode 2472.不重叠回文子字符串的最大数目](https://zhuanlan.zhihu.com/p/588493187) · 知乎 · 2022-12-02 · 赞同 0**
> 力扣：[2472. 不重叠回文子字符串的最大数目](https://leetcode.cn/problems/maximum-number-of-non-overlapping-palindrome-substrings/) · Hard · 灵茶山艾府：[三种方法：DP / 贪心 / Manacher 优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2472.不重叠回文子字符串的最大数目

[力扣](https://leetcode.cn/problems/maximum-number-of-non-overlapping-palindrome-substrings/)

常规的动态规划算法是很容易想到的。令g[i]表示前i个字符可以拆分出来的最多回文子字符串数目，那么对于g[i]，首先有边界情况g[0] \= 0，表示对于空字符的情况，接下来对于i > 0的情况：

1、不使用最后一个字符s[i - 1]，那么就有g[i] \= g[i - 1]

2、使用最后一个字符，那么此时就需要枚举最后这个回文子串的左边界j，那么就有g[i] \= g[j] + 1，其中j满足i - j >\= k，且s[j: i + 1]是一个回文字符串

如果做任何优化，上面这个算法的时间复杂度为O(n^3)，其中状态表示的复杂度为O(n)，枚举左边界j的复杂度为O(n)，判断s[j : i +1]是否为回文子串的复杂度也是O(n)。对于本题的数据规模而言，这个时间复杂度太高了。

由于判断是否为回文子串与动态规划本身无关，那么就可以先将s的所有子串是否为回文子串先预处理出来。如果同样使用暴力算法求解，这一步的时间复杂度也是O(n^2)，那么最终整体的时间复杂度就降到了O(n^2)，已经足够应付本题了。

对于上面的算法，还存在优化的空间。首先状态表示的O(n)是无法再优化的，那么优化的目标就是预处理的O(n^2)以及状态转移的O(n)。

对于预处理而言，在这里如果使用马拉车算法就可以在O(n)的时间内找出以每个字符作为回文中心的最长回文子串。具体细节可以参考

[yiduobo：yiduobo的每日leetcode 5.最长回文子串](https://zhuanlan.zhihu.com/p/113060786)

接下来则是考虑如何优化状态转移方程。

由于题目中对于每个回文子串的划分并没有权重这一说法，那么在满足长度大于等于k的前提下，划分出来的回文子串应该尽量的短，即对于一个长度为k + 2的回文子串而言，将其两侧的字符去掉之后依然能得到一个长度为k的回文子串，从而节省了两个字符提供给其他可能的回文子串使用。

根据这个结论，上面状态转移方程就不需要枚举左边界j了，而只需要考虑以s[i - 1]结尾，且长度为k以及k + 1的子串是否为回文串就行了。这样一来，状态转移的复杂度就从O(n)优化到了O(1)。

在具体实现上，由于马拉车算法在实现时一般会使用插入特殊字符的方法来处理回文串长度奇偶的问题，因此在动态规划时需要注意计算对应位置上的回文串。

最后附上python代码：

```python
class Solution(object):
    def maxPalindromes(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """

        n = len(s)

        if k == 1:
            return n

        s = '!' + '#'.join(list(s)) + '@'
        f = [0]
        mid = 0
        right = 0
        for index in range(1, len(s) - 1, 1):
            if index < right:
                f.append(min(f[2 * mid - index], right - index))
            else:
                f.append(1)
            while s[index - f[index]] == s[index + f[index]]:
                f[index] += 1
            if right < index + f[index]:
                right = index + f[index]
                mid = index
    
        g = [0]
        for index in range(1, n + 1):
            f_pos = index * 2 - 1
            if f_pos >= k - 1 and f[f_pos - (k - 1)] >= k:
                g.append(g[(f_pos - k - k + 2) / 2] + 1)
            elif f_pos >= k and f[f_pos - k] >= k + 1:
                g.append(g[(f_pos - k - k) / 2] + 1)
            else:
                g.append(g[-1])
        
        return g[-1]
```
