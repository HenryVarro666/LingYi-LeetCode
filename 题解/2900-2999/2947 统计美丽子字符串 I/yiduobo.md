---
title: "2947. 统计美丽子字符串"
aliases: ["yiduobo的每日leetcode 2947.统计美丽子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/math", "leetcode/number-theory", "leetcode/prefix-sum"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/691820296"
zhihu_id: "691820296"
zhihu_title: "yiduobo的每日leetcode 2947.统计美丽子字符串"
question_id: "2947"
question: "统计美丽子字符串 I"
problem_url: "https://leetcode.cn/problems/count-beautiful-substrings-i/"
difficulty: "Medium"
created: "2024-04-11T02:02:28+08:00"
updated: "2024-04-11T02:02:28+08:00"
upvotes: 1
comments: 0
---

# 2947. 统计美丽子字符串

> **[yiduobo的每日leetcode 2947.统计美丽子字符串](https://zhuanlan.zhihu.com/p/691820296) · 知乎 · 2024-04-11 · 赞同 1**
> 力扣：[2947. 统计美丽子字符串 I](https://leetcode.cn/problems/count-beautiful-substrings-i/) · Medium · 灵茶山艾府：[O(n) 做法：分解质因子+前缀和+哈希表（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2947.统计美丽子字符串

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-beautiful-substrings-i/)

题目的数据规模不大，因此可以直接暴力计算。枚举子字符串的起点i，然后从i开始不断向后枚举子字符串的终点j，同时计算子字符串中元音和辅音的数量。若数量相同且二者的乘积是k的倍数，那么就更新答案。

最后附上python代码：

```python
class Solution(object):
    def beautifulSubstrings(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """

        vowel_set = set(['a', 'e', 'i', 'o', 'u'])

        res = 0
        for i in range(len(s)):
            vowel = consonants = 0
            for j in range(i, len(s)):
                if s[j] in vowel_set:
                    vowel += 1
                else:
                    consonants += 1

                if vowel == consonants and vowel * consonants % k == 0:
                    res += 1
        
        return res
```
