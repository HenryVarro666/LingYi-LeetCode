---
title: "3823. 反转一个字符串里的字母后反转特殊字符"
aliases: ["yiduobo的每日leetcode 3823.反转一个字符串里的字母后反转特殊字符"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2001436050774589870"
zhihu_id: "2001436050774589870"
zhihu_title: "yiduobo的每日leetcode 3823.反转一个字符串里的字母后反转特殊字符"
question_id: "3823"
question: "反转一个字符串里的字母后反转特殊字符"
problem_url: "https://leetcode.cn/problems/reverse-letters-then-special-characters-in-a-string/"
difficulty: "Easy"
rating: 1250
created: "2026-02-01T23:30:23+08:00"
updated: "2026-02-01T23:30:24+08:00"
upvotes: 0
comments: 0
---

# 3823. 反转一个字符串里的字母后反转特殊字符

> **[yiduobo的每日leetcode 3823.反转一个字符串里的字母后反转特殊字符](https://zhuanlan.zhihu.com/p/2001436050774589870) · 知乎 · 2026-02-01 · 赞同 0**
> 力扣：[3823. 反转一个字符串里的字母后反转特殊字符](https://leetcode.cn/problems/reverse-letters-then-special-characters-in-a-string/) · Easy · 灵茶山艾府：[双指针（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3823.反转一个字符串里的字母后反转特殊字符

<https://leetcode.cn/problems/reverse-letters-then-special-characters-in-a-string/description/>

题目给出一个由小写英文字母和特殊字符组成的字符串s。现在要求先反转其中的小写字母，并将它们放回原来字母占据的位置，然后反转特殊字符，并将它们放回原来特殊字符占据的位置。

问反转后得到的结果字符串。

由于题目中的反转操作是分别将小写字母以及特殊字符反转后，再放回原来的位置，因此可以认为反转小写字母与反转特殊字符是互不相关的，也就是说可以一起执行。

具体来说，可以先对s进行一趟遍历，记录其中的小写字母以及特殊字符，形成数组lower以及sp，接下来再对s一趟遍历，若当前字符是小写字母，那么就将lower的最后一个字符加入到答案数组中，同时将其从lower中弹出，反之就将sp的最后一个字符加入到答案数组中，同时将其中sp中弹出。

最后附上python代码：

```python
class Solution(object):
    def reverseByType(self, s):
        """
        :type s: str
        :rtype: str
        """
        
        lower = []
        sp = []
        for c in s:
            if 'a' <= c <= 'z':
                lower.append(c)
            else:
                sp.append(c)

        res = []
        for c in s:
            if 'a' <= c <= 'z':
                res.append(lower[-1])
                lower.pop()
            else:
                res.append(sp[-1])
                sp.pop()
        
        return ''.join(res)
```
