---
title: "58. 最后一个单词的长度"
aliases: ["yiduobo的每日leetcode 58.最后一个单词的长度"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string", "leetcode/api", "题单/面试经典-150-题", "题单/面试经典-150-题/数组-/-字符串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/128671359"
zhihu_id: "128671359"
zhihu_title: "yiduobo的每日leetcode 58.最后一个单词的长度"
question_id: "58"
question: "最后一个单词的长度"
problem_url: "https://leetcode.cn/problems/length-of-last-word/"
difficulty: "Easy"
created: "2020-04-10T21:10:56+08:00"
updated: "2020-04-10T21:10:56+08:00"
upvotes: 0
comments: 0
---

# 58. 最后一个单词的长度

> **[yiduobo的每日leetcode 58.最后一个单词的长度](https://zhuanlan.zhihu.com/p/128671359) · 知乎 · 2020-04-10 · 赞同 0**
> 力扣：[58. 最后一个单词的长度](https://leetcode.cn/problems/length-of-last-word/) · Easy · 灵茶山艾府：[两种写法：手写循环/库函数（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

58.最后一个单词的长度<https://leetcode-cn.com/problems/length-of-last-word/>

简单的字符串处理问题。

从后往前，找到第一个非空字符，那么这个字符就是最后一个单词的结尾字符。接下来从这个结尾字符往前，找到第一个空字符，那么这个空字符的后一个字符就是最后一个单词的起始字符。最后减一下就能得到答案。

需要特别注意往前找字符时可能会出现的边界问题。

最后附上python代码：

```python
class Solution(object):
    def lengthOfLastWord(self, s):
        """
        :type s: str
        :rtype: int
        """

        end = len(s) - 1
        while end >= 0 and s[end] == ' ':
            end -= 1
        start = end
        while start >=0 and s[start] != ' ':
            start -= 1
        return end - start
```
