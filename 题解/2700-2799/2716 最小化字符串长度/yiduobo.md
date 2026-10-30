---
title: "2716. 最小化字符串长度"
aliases: ["yiduobo的每日leetcode 2716.最小化字符串长度"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/651726606"
zhihu_id: "651726606"
zhihu_title: "yiduobo的每日leetcode 2716.最小化字符串长度"
question_id: "2716"
question: "最小化字符串长度"
problem_url: "https://leetcode.cn/problems/minimize-string-length/"
difficulty: "Easy"
created: "2023-08-23T03:06:10+08:00"
updated: "2023-08-23T03:06:10+08:00"
upvotes: 0
comments: 0
---

# 2716. 最小化字符串长度

> **[yiduobo的每日leetcode 2716.最小化字符串长度](https://zhuanlan.zhihu.com/p/651726606) · 知乎 · 2023-08-23 · 赞同 0**
> 力扣：[2716. 最小化字符串长度](https://leetcode.cn/problems/minimize-string-length/) · Easy · 灵茶山艾府：[两种写法：哈希集合 / 位运算（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2716.最小化字符串长度

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimize-string-length/)

按照题目中的删除方式，可以将每种重复出现的字符删除到只剩下一个为止，因此最终答案就是字符串中不同字符的数目。

最后附上python代码：

```python
class Solution(object):
    def minimizedStringLength(self, s):
        """
        :type s: str
        :rtype: int
        """

        return len(set(s))
```
