---
title: "2707. 字符串中的额外字符"
aliases: ["yiduobo的每日leetcode 2707.字符串中的额外字符"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/五-划分型-DP", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/650975332"
zhihu_id: "650975332"
zhihu_title: "yiduobo的每日leetcode 2707.字符串中的额外字符"
question_id: "2707"
question: "字符串中的额外字符"
problem_url: "https://leetcode.cn/problems/extra-characters-in-a-string/"
difficulty: "Medium"
rating: 1736
created: "2023-08-19T01:24:00+08:00"
updated: "2023-08-19T01:24:00+08:00"
upvotes: 1
comments: 0
---

# 2707. 字符串中的额外字符

> **[yiduobo的每日leetcode 2707.字符串中的额外字符](https://zhuanlan.zhihu.com/p/650975332) · 知乎 · 2023-08-19 · 赞同 1**
> 力扣：[2707. 字符串中的额外字符](https://leetcode.cn/problems/extra-characters-in-a-string/) · Medium · 灵茶山艾府：[动态规划：从记忆化搜索到递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2707.字符串中的额外字符

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/extra-characters-in-a-string/description/)

动态规划的题目。令f[i]表示前i个字符中最少有几个额外字符，初始情况下f[0] \= 0，也就是空串中没有额外字符。接下来一趟遍历，枚举s中的每个字符，根据该字符的处理方式更新f。

对于s[i]，其更新的位置应该是f[i + 1]，那么此时有两种处理方法：

1、放弃s[i]，认为这是一个额外字符，那么就有f[i + 1] \= f[i] + 1

2、尝试将s[i]归属到某个单词中，那么此时应该枚举这个单词的起点位置j，若s[j : i + 1]出现在dictionary中，那么就有f[i + 1] \= min(f[i + 1], f[j])

最后附上python代码：

```python
class Solution(object):
    def minExtraChar(self, s, dictionary):
        """
        :type s: str
        :type dictionary: List[str]
        :rtype: int
        """

        words = set(dictionary)
        n = len(s)
        f = [0]
        for i, char in enumerate(s):
            f.append(f[-1] + 1)
            for j in range(i + 1):
                if s[j : i + 1] in words:
                    f[-1] = min(f[-1], f[j])
        
        return f[-1]
```
