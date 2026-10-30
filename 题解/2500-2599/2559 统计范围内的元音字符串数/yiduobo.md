---
title: "2559. 统计范围内的元音字符串数"
aliases: ["yiduobo的每日leetcode 2559.统计范围内的元音字符串数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/640273654"
zhihu_id: "640273654"
zhihu_title: "yiduobo的每日leetcode 2559.统计范围内的元音字符串数"
question_id: "2559"
question: "统计范围内的元音字符串数"
problem_url: "https://leetcode.cn/problems/count-vowel-strings-in-ranges/"
difficulty: "Medium"
rating: 1435
created: "2023-06-29T00:43:01+08:00"
updated: "2023-06-29T00:43:01+08:00"
upvotes: 0
comments: 0
---

# 2559. 统计范围内的元音字符串数

> **[yiduobo的每日leetcode 2559.统计范围内的元音字符串数](https://zhuanlan.zhihu.com/p/640273654) · 知乎 · 2023-06-29 · 赞同 0**
> 力扣：[2559. 统计范围内的元音字符串数](https://leetcode.cn/problems/count-vowel-strings-in-ranges/) · Medium · 灵茶山艾府：[前缀和（Python3/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2559.统计范围内的元音字符串数

[力扣](https://leetcode.cn/problems/count-vowel-strings-in-ranges/)

如果将元音字符串视为1，非元音字符串视为0，那么本题就是一个经典的区间和问题。对于区间和问题，经典的做法是将区间和转化为前缀和之差，于是只需对字符串数组进行一趟遍历，根据当前遍历到的字符串是否为元音字符串来更新前缀和数组，然后利用前缀和来求解每个查询。

最后附上python代码：

```python
class Solution(object):
    def vowelStrings(self, words, queries):
        """
        :type words: List[str]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        vowel_set = set(['a', 'e', 'i', 'o', 'u'])
        s = [0]
        for w in words:
            s.append(s[-1])
            if w[0] in vowel_set and w[-1] in vowel_set:
                s[-1] += 1
        
        res = []
        for x, y in queries:
            res.append(s[y + 1] - s[x])
        
        return res
```
