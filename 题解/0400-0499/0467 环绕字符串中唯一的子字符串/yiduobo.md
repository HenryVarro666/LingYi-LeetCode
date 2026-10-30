---
title: "467. 环绕字符串中唯一的子字符串"
aliases: ["yiduobo的每日leetcode 467.环绕字符串中唯一的子字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/228812555"
zhihu_id: "228812555"
zhihu_title: "yiduobo的每日leetcode 467.环绕字符串中唯一的子字符串"
question_id: "467"
question: "环绕字符串中唯一的子字符串"
problem_url: "https://leetcode.cn/problems/unique-substrings-in-wraparound-string/"
created: "2020-09-09T20:51:30+08:00"
updated: "2020-09-09T20:51:30+08:00"
upvotes: 0
comments: 0
---

# 467. 环绕字符串中唯一的子字符串

> **[yiduobo的每日leetcode 467.环绕字符串中唯一的子字符串](https://zhuanlan.zhihu.com/p/228812555) · 知乎 · 2020-09-09 · 赞同 0**
> 力扣：[467. 环绕字符串中唯一的子字符串](https://leetcode.cn/problems/unique-substrings-in-wraparound-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

467.环绕字符串中的唯一子字符串<https://leetcode-cn.com/problems/unique-substrings-in-wraparound-string/>

看到题目的第一想法是统计出连续字符形成的子串长度l，然后通过这个l就能计算出这个子串中有多少个唯一的子字符串了。

例如样例3中的zab，长度为3，那么符合条件的子字符串有一个长度为3的，两个长度为2的以及三个长度为1的，即对于长度为l的连续字符子串，可以形成(l + 1) \* l / 2个符合条件的子字符串。但是这样做有个问题就是，其中可能会出现重复的子字符串。例如zabc...za，在统计长度为2的子字符串时会统计两次za，这样就不符合题目要求了。

于是现在需要处理的问题就变成了如何去重。观察s可以发现，对于某个特定的字符，以该字符为首字符且长度固定的子字符是唯一的，设长度为l，那么就存在l个唯一的以该字符为首字符的字符串。若出现了两个以某个字符为首字符的字符串，那么其中较短的那个字符串必然被较长的字符串全面覆盖住，因此较短的那个字符串就没有保留下来的必要了。

至此，现在的做法就变成了从左往右逐个扫描p中的字符，并统计以该字符为首字符的连续字符子串的长度，并用dict来记录下来其中最长的长度，而最后的答案就是dict中value的和。

在实现上，记录字符串的末尾字符比首字符稍微方便一点，因此我在实现的时候记录的是以某字符为某尾字符的连续字符子串的长度。

最后附上python代码：

```python
class Solution(object):
    def findSubstringInWraproundString(self, p):
        """
        :type p: str
        :rtype: int
        """

        if not p:
            return 0
        
        f = {}
        now = ' '
        pos = 0
        for index, char in enumerate(p):
            if now == 'z' and char == 'a' or ord(now) == ord(char) - 1:
                now = char
                f[now] = max(f.get(now, 0), index - pos + 1)
            else:
                now = char
                pos = index
                f[now] = max(f.get(now, 0), 1)

        return sum(f.values())
```
