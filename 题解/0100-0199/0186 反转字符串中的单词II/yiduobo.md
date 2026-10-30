---
title: "186. 反转字符串中的单词II"
aliases: ["yiduobo的每日leetcode 186.反转字符串中的单词II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/591359079"
zhihu_id: "591359079"
zhihu_title: "yiduobo的每日leetcode 186.反转字符串中的单词II"
question_id: "186"
question: "反转字符串中的单词II"
problem_url: "https://leetcode.cn/problems/reverse-words-in-a-string-ii/"
created: "2022-12-13T00:30:11+08:00"
updated: "2022-12-13T00:30:11+08:00"
upvotes: 0
comments: 0
---

# 186. 反转字符串中的单词II

> **[yiduobo的每日leetcode 186.反转字符串中的单词II](https://zhuanlan.zhihu.com/p/591359079) · 知乎 · 2022-12-13 · 赞同 0**
> 力扣：[186. 反转字符串中的单词II](https://leetcode.cn/problems/reverse-words-in-a-string-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

186.反转字符串中的单词II

[力扣](https://leetcode.cn/problems/reverse-words-in-a-string-ii/)

题目要求将单词的顺序反转，但是单词本身不变，同时不能使用额外的空间。

反转单词间的相对顺序最简单的做法自然是反转整个数组，但是这样一来每个单词自身就被反转了，此时只需一趟遍历，将每个单词自身再进行一次反转就可以抵消掉反转整个数组带来的影响了。

最后附上python代码：

```python
class Solution(object):
    def reverseWords(self, s):
        """
        :type s: List[str]
        :rtype: None Do not return anything, modify s in-place instead.
        """

        def reverse_part(left, right):
            while left < right:
                s[left], s[right] = s[right], s[left]
                left += 1
                right -= 1
        
        reverse_part(0, len(s) - 1)
        
        p = 0
        for index in range(1, len(s)):
            if s[index] == ' ':
                reverse_part(p, index - 1)
                p = index + 1
        
        reverse_part(p, len(s) - 1)
```
