---
title: "3773. 最大等长连续字符组"
aliases: ["yiduobo的每日leetcode 3773.最大等长连续字符组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1982238320646977532"
zhihu_id: "1982238320646977532"
zhihu_title: "yiduobo的每日leetcode 3773.最大等长连续字符组"
question_id: "3773"
question: "最大等长连续字符组"
problem_url: "https://leetcode.cn/problems/maximum-number-of-equal-length-runs/"
created: "2025-12-11T20:58:55+08:00"
updated: "2025-12-15T21:26:01+08:00"
upvotes: 1
comments: 0
---

# 3773. 最大等长连续字符组

> **[yiduobo的每日leetcode 3773.最大等长连续字符组](https://zhuanlan.zhihu.com/p/1982238320646977532) · 知乎 · 2025-12-11 · 赞同 1**
> 力扣：[3773. 最大等长连续字符组](https://leetcode.cn/problems/maximum-number-of-equal-length-runs/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3773.最大等长连续字符组

[3773. 最大等长连续字符组 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-number-of-equal-length-runs/)

题目给出一个由小写英文字母组成的字符串s。

s中的一个连续字符组定义为一个由无法再扩展的相同字符组成的子串。例如hello中的连续字符组为h、e、ll、o。问s中长度相同的字符组出现的最大次数是多少。

一趟遍历，将s分离成由相同字符组成的子串，并使用哈希表记录每种长度出现的次数。接下来返回哈希表中的最大次数即可。

最后附上python代码：

```python
class Solution(object):
    def maxSameLengthRuns(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        freq = {}
        p = 0
        while p < len(s):
            q = p + 1
            while q < len(s) and s[q] == s[p]:
                q += 1
            freq[q - p] = freq.get(q - p, 0) + 1
            p = q

        return max(freq.values())
```
