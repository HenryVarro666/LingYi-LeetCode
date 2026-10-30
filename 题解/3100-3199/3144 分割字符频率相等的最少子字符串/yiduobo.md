---
title: "3144. 分割字符串频率相等的最少子字符串"
aliases: ["yiduobo的每日leetcode 3144.分割字符串频率相等的最少子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/string", "leetcode/dynamic-programming", "leetcode/di-tui", "题单/动态规划", "题单/动态规划/五-划分型-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/703288359"
zhihu_id: "703288359"
zhihu_title: "yiduobo的每日leetcode 3144.分割字符串频率相等的最少子字符串"
question_id: "3144"
question: "分割字符频率相等的最少子字符串"
problem_url: "https://leetcode.cn/problems/minimum-substring-partition-of-equal-character-frequency/"
difficulty: "Medium"
rating: 1917
created: "2024-06-14T01:35:27+08:00"
updated: "2024-06-14T01:35:27+08:00"
upvotes: 0
comments: 0
---

# 3144. 分割字符串频率相等的最少子字符串

> **[yiduobo的每日leetcode 3144.分割字符串频率相等的最少子字符串](https://zhuanlan.zhihu.com/p/703288359) · 知乎 · 2024-06-14 · 赞同 0**
> 力扣：[3144. 分割字符频率相等的最少子字符串](https://leetcode.cn/problems/minimum-substring-partition-of-equal-character-frequency/) · Medium · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3144.分割字符串频率相等的最少子字符串

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-substring-partition-of-equal-character-frequency/description/)

题目给出一个字符串c，要求将其分割成若干个子串，要求每个子串中每种字符出现的次数都相同，问最少可以分割出多少个子串。

这是经典的字符串分割问题，可以使用动态规划求解。令f[i]表示字符串的前i个字符可以分割出最少多少个子串，那么对于f[i]，只需从0到i - 1枚举上一次的分割点pre，若c[pre + 1: i + 1]这个子串中每种字符出现的次数都相等，那么就有f[i] \= min(f[i], f[pre] + 1)，表示将c[pre + 1 : i + 1]这个子串划分出去。

而对于判断子串中每种字符出现的次数是否都相等这个问题，则可以利用哈希表求解。使用哈希表储存当前子串中每个字符出现的次数，那么只有当哈希表中的最大次数乘以其中字符种类的数目恰好等于子串的长度时，子串中每种字符出现的次数才相等。

最后附上python代码：

```python
class Solution(object):
    def minimumSubstringsInPartition(self, s):
        """
        :type s: str
        :rtype: int
        """

        n = len(s)
        f = [0] * (n + 1)

        for index in range(1, n + 1):
            f[index] = f[index - 1] + 1
            freq = Counter()
            ma = 0

            for pre in range(index - 1, -1, -1):
                char = s[pre]
                freq[char] += 1
                ma = max(ma, freq[char])
                
                if ma * len(freq) == index - pre:
                    f[index] = min(f[index], f[pre] + 1)
        
        return f[-1]
```
