---
title: "3884. 双端字符匹配"
aliases: ["yiduobo的每日leetcode 3884.双端字符匹配"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2022433975768031664"
zhihu_id: "2022433975768031664"
zhihu_title: "yiduobo的每日leetcode 3884.双端字符匹配"
question_id: "3884"
question: "双端字符匹配"
problem_url: "https://leetcode.cn/problems/first-matching-character-from-both-ends/"
difficulty: "Easy"
created: "2026-03-31T22:06:40+08:00"
updated: "2026-03-31T22:06:40+08:00"
upvotes: 1
comments: 0
---

# 3884. 双端字符匹配

> **[yiduobo的每日leetcode 3884.双端字符匹配](https://zhuanlan.zhihu.com/p/2022433975768031664) · 知乎 · 2026-03-31 · 赞同 1**
> 力扣：[3884. 双端字符匹配](https://leetcode.cn/problems/first-matching-character-from-both-ends/) · Easy · 灵茶山艾府：[遍历一半即可（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3884.双端字符匹配

<https://leetcode.cn/problems/first-matching-character-from-both-ends/description/>

题目给出一个长度为n的字符串s，其中只包含小写字母。

要求找出最小的index，满足s[index]与s[n - index - 1]相同。

若不存在合法的index，则返回-1。

直接按照题目要求从0开始向上遍历index，若期间出现了某个index满足s[index]与s[n - index - 1]相同，那么答案就是index，反之若直到index > n - index - 1都没有出现这样的index，那么答案就是-1。

最后附上python代码：

```python
class Solution(object):
    def firstMatchingIndex(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        index = 0
        n = len(s)
        while index <= n - index - 1 and s[index] != s[n - index - 1]:
            index += 1
        
        if index <= n - index - 1:
            return index
        return -1
```
