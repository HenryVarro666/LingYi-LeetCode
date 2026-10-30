---
title: "1456. 定长子串中元音的最大数目"
aliases: ["yiduobo的每日leetcode 1456.定长子串中元音的最大数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/一-定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/412246187"
zhihu_id: "412246187"
zhihu_title: "yiduobo的每日leetcode 1456.定长子串中元音的最大数目"
question_id: "1456"
question: "定长子串中元音的最大数目"
problem_url: "https://leetcode.cn/problems/maximum-number-of-vowels-in-a-substring-of-given-length/"
difficulty: "Medium"
rating: 1263
created: "2021-09-20T15:12:54+08:00"
updated: "2021-09-20T15:12:54+08:00"
upvotes: 0
comments: 0
---

# 1456. 定长子串中元音的最大数目

> **[yiduobo的每日leetcode 1456.定长子串中元音的最大数目](https://zhuanlan.zhihu.com/p/412246187) · 知乎 · 2021-09-20 · 赞同 0**
> 力扣：[1456. 定长子串中元音的最大数目](https://leetcode.cn/problems/maximum-number-of-vowels-in-a-substring-of-given-length/) · Medium · 灵茶山艾府：[【套路】教你解决定长滑窗！适用于所有定长滑窗题目！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1456.定长子串中元音的最大数目

[力扣](https://leetcode-cn.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/)

经典的滑动窗口问题。

首先初始化窗口为s[:k]，统计其中元音字符的数目now，并初始化答案为now。

接下来将窗口向后移动，根据滑入和滑出的字符更新now同时更新答案，直到窗口滑动到字符串末尾为止。

最后附上python代码：

```python
class Solution(object):
    def maxVowels(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """

        cnt = 0
        v_set = set(['a', 'e', 'i', 'o', 'u'])
        for index in range(k):
            if s[index] in v_set:
                cnt += 1
        
        res = cnt
        for index in range(k, len(s)):
            if s[index] in v_set:
                cnt += 1
            if s[index - k] in v_set:
                cnt -= 1
            res = max(res, cnt)
        
        return res
```
