---
title: "3090. 每个字符最多出现两次的最长子字符串"
aliases: ["yiduobo的每日leetcode 3090.每个字符最多出现两次的最长子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/699079776"
zhihu_id: "699079776"
zhihu_title: "yiduobo的每日leetcode 3090.每个字符最多出现两次的最长子字符串"
question_id: "3090"
question: "每个字符最多出现两次的最长子字符串"
problem_url: "https://leetcode.cn/problems/maximum-length-substring-with-two-occurrences/"
difficulty: "Easy"
rating: 1329
created: "2024-05-21T22:18:47+08:00"
updated: "2024-05-21T22:18:47+08:00"
upvotes: 1
comments: 0
---

# 3090. 每个字符最多出现两次的最长子字符串

> **[yiduobo的每日leetcode 3090.每个字符最多出现两次的最长子字符串](https://zhuanlan.zhihu.com/p/699079776) · 知乎 · 2024-05-21 · 赞同 1**
> 力扣：[3090. 每个字符最多出现两次的最长子字符串](https://leetcode.cn/problems/maximum-length-substring-with-two-occurrences/) · Easy · 灵茶山艾府：[滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3090.每个字符最多出现两次的最长子字符串

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-length-substring-with-two-occurrences/description/)

题目的数据规模很小，直接暴力是完全可行的。我在这里使用的是变长的滑动窗口从左向右滑动，保持窗口内每种字符出现次数不超过两次即可。

最后附上python代码：

```python
class Solution(object):
    def maximumLengthSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """

        freq = Counter()
        left = 0
        res = 0
        for right in range(len(s)):
            freq[s[right]] += 1
            while freq[s[right]] > 2:
                freq[s[left]] -= 1
                left += 1
            
            res = max(res, right - left + 1)
        
        return res
```
