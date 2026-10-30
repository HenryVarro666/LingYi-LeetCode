---
title: "890. 查找和替换模式"
aliases: ["yiduobo的每日leetcode 890.查找和替换模式"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/352198853"
zhihu_id: "352198853"
zhihu_title: "yiduobo的每日leetcode 890.查找和替换模式"
question_id: "890"
question: "查找和替换模式"
problem_url: "https://leetcode.cn/problems/find-and-replace-pattern/"
created: "2021-02-22T23:15:47+08:00"
updated: "2021-02-22T23:15:47+08:00"
upvotes: 0
comments: 0
---

# 890. 查找和替换模式

> **[yiduobo的每日leetcode 890.查找和替换模式](https://zhuanlan.zhihu.com/p/352198853) · 知乎 · 2021-02-22 · 赞同 0**
> 力扣：[890. 查找和替换模式](https://leetcode.cn/problems/find-and-replace-pattern/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

890.查找和替换模式

[力扣](https://leetcode-cn.com/problems/find-and-replace-pattern/)

对于这个问题，直觉上不应该两两比较pattern以及word中的字符串，而是应该将pattern和word中的字符都转化为某种相似的结构然后进行比较。

我这里采用的是将小写字符映射到数字的做法。对于当前处理的字符串s，设now等于0，表示当前出现过了多少个字符。接下来从左往右遍历s，若当前字符char之前未出现过，那么就建立char到now的映射，同时将now加上1。遍历完成之后，s就转化为了一个数字串，然后用数字串与pattern的数字串进行匹配即可。

最后附上python代码：

```python
class Solution(object):
    def findAndReplacePattern(self, words, pattern):
        """
        :type words: List[str]
        :type pattern: str
        :rtype: List[str]
        """

        pattern_list = self.get_list(pattern)

        res = []
        for word in words:
            if self.get_list(word) == pattern_list:
                res.append(word)
        
        return res

    def get_list(self, s):
        num_dict = {}
        now = 0
        ret = []
        for char in s:
            if char not in num_dict:
                num_dict[char] = now
                now += 1
            ret.append(num_dict[char])
        
        return ret
```
