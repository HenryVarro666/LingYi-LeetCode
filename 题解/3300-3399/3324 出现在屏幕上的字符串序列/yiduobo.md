---
title: "3324. 出现在屏幕上的字符串序列"
aliases: ["yiduobo的每日leetcode 3324.出现在屏幕上的字符串序列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2364594563"
zhihu_id: "2364594563"
zhihu_title: "yiduobo的每日leetcode 3324.出现在屏幕上的字符串序列"
question_id: "3324"
question: "出现在屏幕上的字符串序列"
problem_url: "https://leetcode.cn/problems/find-the-sequence-of-strings-appeared-on-the-screen/"
difficulty: "Medium"
created: "2024-10-21T22:57:58+08:00"
updated: "2024-10-21T22:58:10+08:00"
upvotes: 0
comments: 0
---

# 3324. 出现在屏幕上的字符串序列

> **[yiduobo的每日leetcode 3324.出现在屏幕上的字符串序列](https://zhuanlan.zhihu.com/p/2364594563) · 知乎 · 2024-10-21 · 赞同 0**
> 力扣：[3324. 出现在屏幕上的字符串序列](https://leetcode.cn/problems/find-the-sequence-of-strings-appeared-on-the-screen/) · Medium · 灵茶山艾府：[模拟（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3324.出现在屏幕上的字符串序列

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-sequence-of-strings-appeared-on-the-screen/description/)

题目给出一个字符串target，现在alice将会使用一种特殊的键盘输入target。这个键盘只有两个按键：

1、在已有字符串的末尾添加字符'a'

2、将已有字符的最后一个字符变为字母表中的下一个字符

问最少需要按多少次键才能让alice输入target。

注意到只有第二种操作才能修正字符串中的字符，而且只能修正最后这个字符，因此在这里的输入序列必然是先一个1添加一个'a'，然后若干个2将最后这个'a'修正成target中对应的字符，重复这个过程直到填充完整个字符串。

按照上面这个方式模拟每一个字符的填充过程即可。

最后附上python代码：

```python
class Solution(object):
    def stringSequence(self, target):
        """
        :type target: str
        :rtype: List[str]
        """
        
        res = []
        now = []
        while len(now) < len(target):
            now.append('a')
            res.append(''.join(now))

            while now[-1] != target[len(now) - 1]:
                now[-1] = chr(ord(now[-1]) + 1)
                res.append(''.join(now))
        
        return res
```
