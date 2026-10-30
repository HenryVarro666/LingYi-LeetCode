---
title: "3472. 至多K次操作后的最长回文子序列"
aliases: ["yiduobo的每日leetcode 3472.至多K次操作后的最长回文子序列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/八-区间-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1896750477657482188"
zhihu_id: "1896750477657482188"
zhihu_title: "yiduobo的每日leetcode 3472.至多K次操作后的最长回文子序列"
question_id: "3472"
question: "至多 K 次操作后的最长回文子序列"
problem_url: "https://leetcode.cn/problems/longest-palindromic-subsequence-after-at-most-k-operations/"
difficulty: "Medium"
rating: 1884
created: "2025-04-19T02:48:45+08:00"
updated: "2025-04-19T02:48:45+08:00"
upvotes: 2
comments: 0
---

# 3472. 至多K次操作后的最长回文子序列

> **[yiduobo的每日leetcode 3472.至多K次操作后的最长回文子序列](https://zhuanlan.zhihu.com/p/1896750477657482188) · 知乎 · 2025-04-19 · 赞同 2**
> 力扣：[3472. 至多 K 次操作后的最长回文子序列](https://leetcode.cn/problems/longest-palindromic-subsequence-after-at-most-k-operations/) · Medium · 灵茶山艾府：[区间 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3472.至多K次操作后的最长回文子序列

[3472. 至多 K 次操作后的最长回文子序列 - 力扣（LeetCode）](https://leetcode.cn/problems/longest-palindromic-subsequence-after-at-most-k-operations/description/)

题目给出一个字符串s以及一个整数k，s的长度以及k的大小都不超过200。

接下来可以对s执行至多k次操作，在每次操作中，都可以将s中任意位置的字符变为其在字母表中相邻的字符。需要注意本题中的字母表是循环的，字母'a'和'z'可以互相变换。

问最多k次操作后，s中的最长回文子序列的长度为多少。

对于回文子序列相关的问题，一种常见的思路是使用区间动态规划的方法，计算每个子区间可以得到的最长回文子序列的长度。而对于本题，则还需要额外携带上剩余操作数这一信息。考虑到本题的数据规模，完全可以直接令f[start][end][r]表示对于s中的区间[start, end]，在还剩下r次操作机会时可以得到的最长回文子序列长度。那么对于f[start][end][r]：

1、若start \= end：

这种情况下，区间中仅有唯一的一个字符，必然可以形成回文子序列，因此有f[start][end][r] \= 1

2、若start \< end：

这种情况下，针对区间的两侧s[start]以及s[end]，可以考虑通过操作使得二者变为相同的字符，从而将二者都保留下来，或者直接放弃掉其中的某一侧。

记ma为s[start]和s[end]中字典序较大的字符，mi为其中的另一个字符，那么要使得ma与mi变为相同字符，可以将ma变为前一个字符一共ord(ma) - ord(mi)次，使得ma变为mi；或者将ma不断变为后一个字符，套圈成为'a'，然后再将这个'a'不断变为后一个字符直到其变为mi，所需的操作次数为ord('z') - ord(ma) + 1 + ord(mi) - ord('a') \= ord(mi) + 26 - ord(ma)。记以上两种方案所需操作次数的较小值为dis，那么：

2-1）若start \= end - 1：

这种情况下，区间内仅有两个字符。若dis \<\= r，则可以通过操作将二者变为相同字符，从而得到一个长度为2的回文子序列，那么就有f[start][end][r] \= 2；反之，若dis > r，则必须放弃其中一个字符，那么就有f[start][end][r] \= 1

2-2）若start \< end - 1：

这种情况下，若放弃掉其中一侧的字符，就有f[start][end][r] \= max(f[start + 1][end][r], f[start][end - 1][r])。若想保留住两侧的字符，那么则必须要满足dis \<\= r，此时就可以用f[start + 1][end - 1][r - dis] + 2来更新f[start][end][r]。

在具体实现上，必须要先计算较短区间对应的f值再计算较长的，方便期间可以使用记忆化搜索。如果想要递推实现，则需要先枚举区间的长度，按区间长度从小到大进行计算。

最后附上python代码：

```python
class Solution(object):
    def longestPalindromicSubsequence(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """
        
        n = len(s)
        f = [[[None] * (k + 1) for _ in range(n)] for _ in range(n)]

        for length in range(1, n + 1):
            for start in range(n):
                end = start + length - 1
                if end >= n:
                    break
                for r in range(k + 1):
                    if length == 1:
                        f[start][end][r] = 1
                    else:
                        ma = max(s[start], s[end])
                        mi = min(s[start], s[end])
                        dis = min(ord(ma) - ord(mi), ord(mi) + 26 - ord(ma))

                        if length == 2:
                            if dis <= r:
                                f[start][end][r] = 2
                            else:
                                f[start][end][r] = 1
                        else:
                            f[start][end][r] = max(f[start + 1][end][r], f[start][end - 1][r])
                            if dis <= r:
                                f[start][end][r] = max(f[start][end][r], f[start + 1][end - 1][r - dis] + 2)

        return f[0][n - 1][k]
```
