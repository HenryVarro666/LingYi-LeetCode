---
title: "290. 单词规律"
aliases: ["yiduobo的每日leetcode 290.单词规律"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/156841564"
zhihu_id: "156841564"
zhihu_title: "yiduobo的每日leetcode 290.单词规律"
question_id: "290"
question: "单词规律"
problem_url: "https://leetcode.cn/problems/word-pattern/"
created: "2020-07-05T17:00:52+08:00"
updated: "2020-07-05T17:00:52+08:00"
upvotes: 0
comments: 0
---

# 290. 单词规律

> **[yiduobo的每日leetcode 290.单词规律](https://zhuanlan.zhihu.com/p/156841564) · 知乎 · 2020-07-05 · 赞同 0**
> 力扣：[290. 单词规律](https://leetcode.cn/problems/word-pattern/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

290.单词规律<https://leetcode-cn.com/problems/word-pattern/>

比较基础的题目，使用一个dict维护每个字母到单词的映射即可。

需要注意每个字母与单词必须一一对应，因此首先二者的数量必须一致，另外当某个字母不在dict中时，其对应的单词也必须没有被使用过。

最后附上python代码：

```python
class Solution(object):
    def wordPattern(self, pattern, str):
        """
        :type pattern: str
        :type str: str
        :rtype: bool
        """

        words = str.split(' ')
        if len(pattern) != len(words):
            return False
        word_dict = {}
        used_set = set()
        for index, char in enumerate(pattern):
            if char not in word_dict:
                if words[index] in used_set:
                    return False
                word_dict[char] = words[index]
                used_set.add(words[index])
            if word_dict[char] != words[index]:
                return False

        return True
```
