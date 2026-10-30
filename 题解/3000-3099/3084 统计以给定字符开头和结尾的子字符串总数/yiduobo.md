---
title: "3084. 统计以给定字符开头和结尾的子字符串总数"
aliases: ["yiduobo的每日leetcode 3084.统计以给定字符开头和结尾的子字符串总数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/698672874"
zhihu_id: "698672874"
zhihu_title: "yiduobo的每日leetcode 3084.统计以给定字符开头和结尾的子字符串总数"
question_id: "3084"
question: "统计以给定字符开头和结尾的子字符串总数"
problem_url: "https://leetcode.cn/problems/count-substrings-starting-and-ending-with-given-character/"
difficulty: "Medium"
created: "2024-05-19T23:56:15+08:00"
updated: "2024-05-19T23:56:15+08:00"
upvotes: 1
comments: 0
---

# 3084. 统计以给定字符开头和结尾的子字符串总数

> **[yiduobo的每日leetcode 3084.统计以给定字符开头和结尾的子字符串总数](https://zhuanlan.zhihu.com/p/698672874) · 知乎 · 2024-05-19 · 赞同 1**
> 力扣：[3084. 统计以给定字符开头和结尾的子字符串总数](https://leetcode.cn/problems/count-substrings-starting-and-ending-with-given-character/) · Medium · 灵茶山艾府：[简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3084.统计以给定字符开头和结尾的子字符串总数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-substrings-starting-and-ending-with-given-character/description/)

不妨设字符c在字符串s中一共出现了freq次，那么对于第一个c，如果以这个c作为子串的开头，那么其后方包括其自身一共有freq个c可以作为子串的结尾，而对于第二个c，则有freq - 1个可用的结尾，以此类推，因此最终答案就是freq + freq - 1 + ... + 1 \= (freq + 1) \* freq / 2。

最后附上python代码：

```python
class Solution(object):
    def countSubstrings(self, s, c):
        """
        :type s: str
        :type c: str
        :rtype: int
        """

        freq = 0
        for char in s:
            if char == c:
                freq += 1
        
        return freq * (freq + 1) // 2
```
