---
title: "2767. 将字符串分割为最少的美丽子字符串"
aliases: ["yiduobo的每日leetcode 2767.将字符串分割为最少的美丽子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/五-划分型-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/655201164"
zhihu_id: "655201164"
zhihu_title: "yiduobo的每日leetcode 2767.将字符串分割为最少的美丽子字符串"
question_id: "2767"
question: "将字符串分割为最少的美丽子字符串"
problem_url: "https://leetcode.cn/problems/partition-string-into-minimum-beautiful-substrings/"
difficulty: "Medium"
rating: 1865
created: "2023-09-09T03:19:16+08:00"
updated: "2023-09-09T03:19:16+08:00"
upvotes: 0
comments: 0
---

# 2767. 将字符串分割为最少的美丽子字符串

> **[yiduobo的每日leetcode 2767.将字符串分割为最少的美丽子字符串](https://zhuanlan.zhihu.com/p/655201164) · 知乎 · 2023-09-09 · 赞同 0**
> 力扣：[2767. 将字符串分割为最少的美丽子字符串](https://leetcode.cn/problems/partition-string-into-minimum-beautiful-substrings/) · Medium · 灵茶山艾府：[O(n^2) 记忆化搜索到递推](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2767.将字符串分割为最少的美丽子字符串

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/partition-string-into-minimum-beautiful-substrings/description/)

题目要求将字符切分成若干段二进制表示下的5的幂，那么就可以先将所有长度不超过s的5的幂的二进制表示先计算好，接下来就是常规的动态规划了。

令f[i]表示以i为结尾的前缀字符串可以被切分成的最少数目，那么对于f[i]，从0到i枚举最后这一段子串的起点j，若s[j : i + 1]这一段是5的幂的二进制表示，那么就有f[i] \= min(f[i], f[j] + 1)。

计算完成后，f[-1]即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minimumBeautifulSubstrings(self, s):
        """
        :type s: str
        :rtype: int
        """

        pow5_str = set(['1'])
        pow5 = 1
        while True:
            pow5 *= 5
            b = bin(pow5)[2:]
            if len(b) > len(s):
                break
            pow5_str.add(b)
        
        f = [0]
        for i in range(len(s)):
            f.append(-1)
            for j in range(i + 1):
                if s[j : i + 1] in pow5_str and f[j] != -1 and (f[-1] == -1 or f[-1] > f[j] + 1):
                    f[-1] = f[j] + 1

        return f[-1]
```
