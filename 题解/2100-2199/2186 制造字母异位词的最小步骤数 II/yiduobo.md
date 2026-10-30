---
title: "2186. 使两字符串互为字母异位词的最少步骤数"
aliases: ["yiduobo的每日leetcode 2186.使两字符串互为字母异位词的最少步骤数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/536559802"
zhihu_id: "536559802"
zhihu_title: "yiduobo的每日leetcode 2186.使两字符串互为字母异位词的最少步骤数"
question_id: "2186"
question: "制造字母异位词的最小步骤数 II"
problem_url: "https://leetcode.cn/problems/minimum-number-of-steps-to-make-two-strings-anagram-ii/"
difficulty: "Medium"
created: "2022-07-02T01:07:18+08:00"
updated: "2022-07-02T01:07:18+08:00"
upvotes: 0
comments: 0
---

# 2186. 使两字符串互为字母异位词的最少步骤数

> **[yiduobo的每日leetcode 2186.使两字符串互为字母异位词的最少步骤数](https://zhuanlan.zhihu.com/p/536559802) · 知乎 · 2022-07-02 · 赞同 0**
> 力扣：[2186. 制造字母异位词的最小步骤数 II](https://leetcode.cn/problems/minimum-number-of-steps-to-make-two-strings-anagram-ii/) · Medium · 灵茶山艾府：[累加各个字母出现次数的差值](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2186.使两字符串互为字母异位词的最少步骤数

[力扣](https://leetcode.cn/problems/minimum-number-of-steps-to-make-two-strings-anagram-ii/)

题目规定每一步操作都只能添加一个字符，因此只需统计两个字符串中每种字符出现的次数，然后遍历每种字符，添加若干当前遍历到的字符直到两个字符串中该字符的数目相等，那么添加的次数就是两个字符串中该字符出现次数之差的绝对值。将这个次数累加起来就能得到最终答案。

最后附上python代码：

```python
class Solution(object):
    def minSteps(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: int
        """

        s_cnt = {}
        t_cnt = {}
        for char in s:
            s_cnt[char] = s_cnt.get(char, 0) + 1
        for char in t:
            t_cnt[char] = t_cnt.get(char, 0) + 1
        
        res = 0
        for index in range(26):
            char = chr(index + 97)
            res += abs(s_cnt.get(char, 0) - t_cnt.get(char, 0))
        
        return res
```
