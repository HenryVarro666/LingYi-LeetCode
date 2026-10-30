---
title: "3407. 字符串匹配模式"
aliases: ["yiduobo的每日leetcode 3407.字符串匹配模式"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string-matching"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/31686553202"
zhihu_id: "31686553202"
zhihu_title: "yiduobo的每日leetcode 3407.字符串匹配模式"
question_id: "3407"
question: "子字符串匹配模式"
problem_url: "https://leetcode.cn/problems/substring-matching-pattern/"
difficulty: "Easy"
created: "2025-03-21T02:05:31+08:00"
updated: "2025-03-21T02:05:31+08:00"
upvotes: 0
comments: 0
---

# 3407. 字符串匹配模式

> **[yiduobo的每日leetcode 3407.字符串匹配模式](https://zhuanlan.zhihu.com/p/31686553202) · 知乎 · 2025-03-21 · 赞同 0**
> 力扣：[3407. 子字符串匹配模式](https://leetcode.cn/problems/substring-matching-pattern/) · Easy · 灵茶山艾府：[库函数简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3407.字符串匹配模式

[3407. 子字符串匹配模式 - 力扣（LeetCode）](https://leetcode.cn/problems/substring-matching-pattern/description/)

题目给出一个字符串s以及一个模式字符串p，其中p恰好包含一个星号，这个星号可以替换成零个或者多个字符组成的任意字符串。问能否通过替换星号使得p变为s的子串。

不妨设星号在p中出现的下标为star，那么p可以分为三段，分别是p[:star], p[star]以及p[star + 1:]，其中p[star]为星号。相对应的，如果通过修改p[star]可以使得p变为s的子串，那么就必须满足p[:star]以及p[star + 1:]都是s的子串，且这两个子串不重叠。

为了使得二者不重叠，那么就应该让p[:star]在s中对应的子串尽量靠前，让p[star + 1:]在s中对应的子串尽量靠后，于是可以先找出p[:star]在s中第一次出现的下标left以及p[:star + 1:]在s中最后一次出现的下标right，接下来只需检测p[:star]最后一个字符的下标，即left + star - 1是否在right左侧即可。另外如果s中找不到p[:star]或者p[star + 1:]，那么答案自然也是-1。

需要特别注意可能有p[:star]或者p[star + 1:]不存在的情况，对于这两种情况，可以分别设置left和right为-1和len(s)，这样一来不会影响最后不等式的判断。

最后附上python代码：

```python
class Solution(object):
    def hasMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """
        
        star = p.find('*')

        if star > 0:
            left = s.find(p[:star])
            if left == -1:
                return False
        else:
            left = -1

        if star < len(p) - 1:
            right = s.rfind(p[star + 1:])
            if right == -1:
                return False
        else:
            right = len(s)

        return left + star - 1 < right
```
