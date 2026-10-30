---
title: "2842. 统计一个字符串的k子序列美丽值最大的数目"
aliases: ["yiduobo的每日leetcode 2842.统计一个字符串的k子序列美丽值最大的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/math", "leetcode/combinatorics", "leetcode/ordered-set", "题单/数学算法", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/659806783"
zhihu_id: "659806783"
zhihu_title: "yiduobo的每日leetcode 2842.统计一个字符串的k子序列美丽值最大的数目"
question_id: "2842"
question: "统计一个字符串的 k 子序列美丽值最大的数目"
problem_url: "https://leetcode.cn/problems/count-k-subsequences-of-a-string-with-maximum-beauty/"
difficulty: "Hard"
rating: 2092
created: "2023-10-07T04:36:52+08:00"
updated: "2023-10-07T04:36:52+08:00"
upvotes: 0
comments: 0
---

# 2842. 统计一个字符串的k子序列美丽值最大的数目

> **[yiduobo的每日leetcode 2842.统计一个字符串的k子序列美丽值最大的数目](https://zhuanlan.zhihu.com/p/659806783) · 知乎 · 2023-10-07 · 赞同 0**
> 力扣：[2842. 统计一个字符串的 k 子序列美丽值最大的数目](https://leetcode.cn/problems/count-k-subsequences-of-a-string-with-maximum-beauty/) · Hard · 灵茶山艾府：[组合数学（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2842.统计一个字符串的k子序列美丽值最大的数目

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/count-k-subsequences-of-a-string-with-maximum-beauty/)

题目中的k子序列值的是从字符串中选出k种不同的字符，而美丽值则是由这k种字符出现的频率之和想加得到。为了得到美丽值最大的子序列，就应该优先选择出现频率高的字符，于是在这里就应该先统计每种字符出现的频率，同时在这个过程中可以顺带解决一种边界情况，即不同字符的种数不足k种，此时的答案显然为0。

统计好每种字符出现的频率后，由于题目不关心子序列的具体内容，那么两种出现频率相同的不同字符实际上是等价的，于是可以进一步对这些频率进行统计，即统计每种频率出现了多少次。

接下来从大到小遍历出现频率，不妨设当前频率freq出现了cnt次，那么：

1、cnt \<\= k：

这cnt种字符就应该都加入到答案中。每种字符出现了freq次，一共有cnt种字符，根据乘法原理，这里就有freq^cnt种不同的子序列，将这个值累乘到答案中，然后将k减去cnt并继续遍历下一个freq

2、cnt > k：

此时就需要从这cnt种字符中选出k种，也就是C(cnt, k)。对于选好的k种字符，同样是每种字符出现了freq次，因此这里就需要将C(cnt, k) \* freq^k累乘到答案中，然后返回答案

另外由于本题中出现了组合数以及取模操作，如果不想使用乘法逆元那么就可以利用动态规划先预处理出这些组合数，也就是c[i][j] \= c[i - 1][j - 1] + c[i - 1][j]，同时在这个过程中完成取模。

最后附上python代码：

```python
class Solution(object):
    def countKSubsequencesWithMaxBeauty(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """

        char_freq = {}
        for char in s:
            char_freq[char] = char_freq.get(char, 0) + 1
        
        if len(char_freq) < k:
            return 0
        
        freq_cnt = {}
        for v in char_freq.values():
            freq_cnt[v] = freq_cnt.get(v, 0) + 1

        mod = 10 ** 9 + 7
        c = [[0] * 26 for _ in range(26)]
        for i in range(26):
            for j in range(i + 1):
                if j == 0 or j == i:
                    c[i][j] = 1
                else:
                    c[i][j] = c[i - 1][j] + c[i - 1][j - 1]
                    if c[i][j] >= mod:
                        c[i][j] -= mod

        res = 1
        for freq, cnt in sorted(freq_cnt.items(), reverse=True):
            if k >= cnt:
                for _ in range(cnt):
                    res *= freq
                    res %= mod
                k -= cnt
            else:
                res *= c[cnt][k]
                res %= mod
                for _ in range(k):
                    res *= freq
                    res %= mod
                break
        
        return res
```
