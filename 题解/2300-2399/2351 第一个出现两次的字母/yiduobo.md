---
title: "2351. 第一个出现两次的字母"
aliases: ["yiduobo的每日leetcode 2351.第一个出现两次的字母"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/561248637"
zhihu_id: "561248637"
zhihu_title: "yiduobo的每日leetcode 2351.第一个出现两次的字母"
question_id: "2351"
question: "第一个出现两次的字母"
problem_url: "https://leetcode.cn/problems/first-letter-to-appear-twice/"
difficulty: "Easy"
created: "2022-09-05T00:30:19+08:00"
updated: "2022-09-05T00:30:19+08:00"
upvotes: 1
comments: 0
---

# 2351. 第一个出现两次的字母

> **[yiduobo的每日leetcode 2351.第一个出现两次的字母](https://zhuanlan.zhihu.com/p/561248637) · 知乎 · 2022-09-05 · 赞同 1**
> 力扣：[2351. 第一个出现两次的字母](https://leetcode.cn/problems/first-letter-to-appear-twice/) · Easy · 灵茶山艾府：[位运算 O(1) 空间](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2351.第一个出现两次的字母

[力扣](https://leetcode.cn/problems/first-letter-to-appear-twice/)

一趟遍历，使用集合记录以及出现过的字符。若当前遍历到的字符char在集合中，那么char就是最终答案，否则将char加入到集合中然后继续向后遍历。

最后附上python代码：

```python
class Solution(object):
    def repeatedCharacter(self, s):
        """
        :type s: str
        :rtype: str
        """

        char_set = set()
        for char in s:
            if char in char_set:
                return char
            char_set.add(char)
```
