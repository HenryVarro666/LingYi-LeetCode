---
title: "3110. 字符串的分数"
aliases: ["yiduobo的每日leetcode 3110.字符串的分数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/700813170"
zhihu_id: "700813170"
zhihu_title: "yiduobo的每日leetcode 3110.字符串的分数"
question_id: "3110"
question: "字符串的分数"
problem_url: "https://leetcode.cn/problems/score-of-a-string/"
difficulty: "Easy"
created: "2024-05-30T23:38:30+08:00"
updated: "2024-05-30T23:38:30+08:00"
upvotes: 0
comments: 0
---

# 3110. 字符串的分数

> **[yiduobo的每日leetcode 3110.字符串的分数](https://zhuanlan.zhihu.com/p/700813170) · 知乎 · 2024-05-30 · 赞同 0**
> 力扣：[3110. 字符串的分数](https://leetcode.cn/problems/score-of-a-string/) · Easy · 灵茶山艾府：[遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3110.字符串的分数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/score-of-a-string/description/)

从下标1开始向后一趟遍历，将当前字符与前一个字符ascii码之差的绝对值累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def scoreOfString(self, s):
        """
        :type s: str
        :rtype: int
        """

        res = 0
        for index in range(1, len(s)):
            res += abs(ord(s[index]) - ord(s[index - 1]))
        
        return res
```
