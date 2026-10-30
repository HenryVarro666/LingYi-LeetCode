---
title: "1216. 验证回文字符串III"
aliases: ["yiduobo的每日leetcode 1216.验证回文字符串III"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/613444066"
zhihu_id: "613444066"
zhihu_title: "yiduobo的每日leetcode 1216.验证回文字符串III"
question_id: "1216"
question: "验证回文字符串III"
problem_url: "https://leetcode.cn/problems/valid-palindrome-iii/"
created: "2023-03-12T23:16:06+08:00"
updated: "2023-03-12T23:16:06+08:00"
upvotes: 0
comments: 0
---

# 1216. 验证回文字符串III

> **[yiduobo的每日leetcode 1216.验证回文字符串III](https://zhuanlan.zhihu.com/p/613444066) · 知乎 · 2023-03-12 · 赞同 0**
> 力扣：[1216. 验证回文字符串III](https://leetcode.cn/problems/valid-palindrome-iii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1216.验证回文字符串III

[力扣](https://leetcode.cn/problems/valid-palindrome-iii/)

经典的动态规划问题。令f[left][right]表示将字符串中left到right修正成回文串所需的最少操作次数，那么对于f[left][right]：

1、若left \= right：

此时只有一个字符，因此f[left][right] \= 0

2、若left \= right - 1：

此时只有两个字符。若s[left] \= s[right]，那么就有f[left][right] \= 0，否则就需要移除s[left]和s[right]中的一个字符，因此有f[left][right] \= 1

3、其他一般情况：

此时可以同样是检测s[left]是否等于s[right]。若相等，那么就有f[left][right] \= f[left + 1][right - 1]，否则必须移除s[left]和s[right]中的一个字符，因此有f[left][right] \= min(f[left + 1][right], f[left][right - 1]) + 1

全部计算完成后，只需检测f[0][n - 1]是否小于等于k即可。

具体实现上，使用记忆化搜索是比较直观的，如果想使用常规的递推，则需要优先计算出长度较小的子串对应的f，因此需要先从小到大枚举子串的长度，然后枚举left，并通过left和长度计算出对应的right。

最后附上python代码：

```python
class Solution(object):
    def isValidPalindrome(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: bool
        """

        n = len(s)

        f = [[None] * n for _ in range(n)]
        for length in range(1, n + 1):
            for left in range(n):
                right = left + length - 1
                if right >= n:
                    break
                if left == right:
                    f[left][right] = 0
                elif left == right - 1:
                    if s[left] == s[right]:
                        f[left][right] = 0
                    else:
                        f[left][right] = 1
                else:
                    if s[left] == s[right]:
                        f[left][right] = f[left + 1][right - 1]
                    else:
                        f[left][right] = min(f[left + 1][right], f[left][right - 1]) + 1
        
        return f[0][n - 1] <= k
```
