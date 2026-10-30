---
title: "2067. 等计数子串的数量"
aliases: ["yiduobo的每日leetcode 2067.等计数子串的数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/625945823"
zhihu_id: "625945823"
zhihu_title: "yiduobo的每日leetcode 2067.等计数子串的数量"
question_id: "2067"
question: "等计数子串的数量"
problem_url: "https://leetcode.cn/problems/number-of-equal-count-substrings/"
created: "2023-04-30T05:01:43+08:00"
updated: "2023-04-30T05:01:43+08:00"
upvotes: 0
comments: 0
---

# 2067. 等计数子串的数量

> **[yiduobo的每日leetcode 2067.等计数子串的数量](https://zhuanlan.zhihu.com/p/625945823) · 知乎 · 2023-04-30 · 赞同 0**
> 力扣：[2067. 等计数子串的数量](https://leetcode.cn/problems/number-of-equal-count-substrings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

2067.等计数子串的数量

[力扣](https://leetcode.cn/problems/number-of-equal-count-substrings/)

由于题目中的s仅有小写字符构成，那么所有的等计数子串中的不同字符数量必然在1到26之间，于是可以枚举这个不同字符的数量tot_char，这样就得到出现了tot_char个不同字符的等计数子串的长度sub_len \= tot_char \* count。接下来就是经典的滑动窗口问题了，使用一个长度为sub_len的窗口从左向右滑动，维护窗口内每种字符出现的次数。若某一时刻窗口内每种字符都恰好出现了count次，那么就将答案加上1。

最后附上python代码：

```python
class Solution(object):
    def equalCountSubstrings(self, s, count):
        """
        :type s: str
        :type count: int
        :rtype: int
        """

        def check(cnt):
            for v in cnt.values():
                if v != count:
                    return 0
            return 1

        res = 0
        n = len(s)
        for tot_char in range(1, 27):
            sub_len = tot_char * count
            cnt = {}
            if sub_len <= n:
                for char in s[:sub_len]:
                    cnt[char] = cnt.get(char, 0) + 1
                res += check(cnt)

                for index, char in enumerate(s[sub_len:]):
                    cnt[char] = cnt.get(char, 0) + 1
                    cnt[s[index]] -= 1
                    if cnt[s[index]] == 0:
                        cnt.pop(s[index])
                    res += check(cnt)

        return res
```
