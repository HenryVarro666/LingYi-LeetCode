---
title: "3517. 最小回文排列I"
aliases: ["yiduobo的每日leetcode 3517.最小回文排列I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/counting-sort", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1902542509688750100"
zhihu_id: "1902542509688750100"
zhihu_title: "yiduobo的每日leetcode 3517.最小回文排列I"
question_id: "3517"
question: "最小回文排列 I"
problem_url: "https://leetcode.cn/problems/smallest-palindromic-rearrangement-i/"
difficulty: "Medium"
rating: 1357
created: "2025-05-08T00:09:12+08:00"
updated: "2025-05-08T00:09:12+08:00"
upvotes: 2
comments: 0
---

# 3517. 最小回文排列I

> **[yiduobo的每日leetcode 3517.最小回文排列I](https://zhuanlan.zhihu.com/p/1902542509688750100) · 知乎 · 2025-05-08 · 赞同 2**
> 力扣：[3517. 最小回文排列 I](https://leetcode.cn/problems/smallest-palindromic-rearrangement-i/) · Medium · 灵茶山艾府：[排序左半部分 + 计数排序优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3517.最小回文排列I

<https://leetcode.cn/problems/smallest-palindromic-rearrangement-i>

题目给出一个回文字符串s，要求将s中的字符重新排列，得到字典序最小的回文串。

为了保证得到的字符串依然是回文串，那么s前半段和后半段各自的字符组成是不能改的。而为了使得字典序最小，那么就应该保证s前半段的字典序最小。于是只需对s的前半段字符进行排序，就可以得到答案字符串的前半部分。接下来将其翻转后作为后半部分，拼接起来即为最终答案。

需要特别注意的是，当s的长度为奇数时，还有一个落单的中间字符mid，在拼接答案时需要将mid也拼接进来。

最后附上python代码：

```python
class Solution(object):
    def smallestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """
        
        n = len(s)
        left = ''.join(sorted(s[:n // 2]))
        right = left[::-1]
        mid = ''
        if n % 2 == 1:
            mid = s[n // 2]
        return left + mid + right
```
