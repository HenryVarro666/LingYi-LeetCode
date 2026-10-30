---
title: "1147. 段式回文"
aliases: ["yiduobo的每日leetcode 1147.段式回文"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/recursion", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/378051003"
zhihu_id: "378051003"
zhihu_title: "yiduobo的每日leetcode 1147.段式回文"
question_id: "1147"
question: "段式回文"
problem_url: "https://leetcode.cn/problems/longest-chunked-palindrome-decomposition/"
difficulty: "Hard"
rating: 1912
created: "2021-06-05T00:07:58+08:00"
updated: "2021-06-05T00:07:58+08:00"
upvotes: 0
comments: 0
---

# 1147. 段式回文

> **[yiduobo的每日leetcode 1147.段式回文](https://zhuanlan.zhihu.com/p/378051003) · 知乎 · 2021-06-05 · 赞同 0**
> 力扣：[1147. 段式回文](https://leetcode.cn/problems/longest-chunked-palindrome-decomposition/) · Hard · 灵茶山艾府：[【图解】贪心做法，一图秒懂！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1147.段式回文

[力扣](https://leetcode-cn.com/problems/longest-chunked-palindrome-decomposition/)

贪心法的题目。对于两个前缀A和B，不妨设A的长度大于B。那么若此时存在后缀A'与A相同，后缀B'与B相同，那么就说明前缀A自身存在一个与B完全相同的后缀，同时后缀A'则存在一个与B完全相同的前缀，因此A和A'至少可以分解成两段匹配的段氏回文，这也就说明了我们应该使用贪心法，每次从两端向中心探测，当出现一个匹配的段氏回文时就立即将其加入答案，这样一来才能得到最多的段数。

最后附上python代码：

```python
class Solution(object):
    def longestDecomposition(self, text):
        """
        :type text: str
        :rtype: int
        """

        l = 0
        r = len(text) - 1
        res = 0
        p = l
        while l < r:
            while p < r and text[p] != text[r]:
                p += 1
            
            if p == r:
                return res + 1
            
            part_len = p - l + 1
            q = r - part_len + 1
            if q <= p:
                return res + 1
            
            if text[l:p] == text[q:r]:
                res += 2
                l = p + 1
                r = q - 1
                p = l
            else:
                p += 1
        
        if l == r:
            res += 1
        return res
```
