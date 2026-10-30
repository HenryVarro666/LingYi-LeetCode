---
title: "3210. 找出加密后的字符串"
aliases: ["yiduobo的每日leetcode 3210.找出加密后的字符串"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/brainteaser", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/708145815"
zhihu_id: "708145815"
zhihu_title: "yiduobo的每日leetcode 3210.找出加密后的字符串"
question_id: "3210"
question: "找出加密后的字符串"
problem_url: "https://leetcode.cn/problems/find-the-encrypted-string/"
difficulty: "Easy"
created: "2024-07-10T22:00:07+08:00"
updated: "2024-07-10T22:00:07+08:00"
upvotes: 1
comments: 0
---

# 3210. 找出加密后的字符串

> **[yiduobo的每日leetcode 3210.找出加密后的字符串](https://zhuanlan.zhihu.com/p/708145815) · 知乎 · 2024-07-10 · 赞同 1**
> 力扣：[3210. 找出加密后的字符串](https://leetcode.cn/problems/find-the-encrypted-string/) · Easy · 灵茶山艾府：[简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3210.找出加密后的字符串

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-encrypted-string/description/)

题目给出一个字符串s以及一个正整数k，要求将s中的每个字符c以循环的方式替换成c后面的第k个字符，问替换后的字符串是什么。

按照题目要求一趟遍历，对于当前遍历到的下标index，将s[(index + k) % len(s)]填充到答案的index位上即可。

最后附上python代码：

```python
class Solution(object):
    def getEncryptedString(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: str
        """

        return ''.join([s[(index + k) % len(s)] for index in range(len(s))])
```
