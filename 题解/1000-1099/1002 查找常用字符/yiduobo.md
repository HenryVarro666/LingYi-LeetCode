---
title: "1002. 查找常用字符"
aliases: ["yiduobo的每日leetcode 1002.查找常用字符"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/366179660"
zhihu_id: "366179660"
zhihu_title: "yiduobo的每日leetcode 1002.查找常用字符"
question_id: "1002"
question: "查找常用字符"
problem_url: "https://leetcode.cn/problems/find-common-characters/"
created: "2021-04-19T23:31:25+08:00"
updated: "2021-04-19T23:31:25+08:00"
upvotes: 0
comments: 0
---

# 1002. 查找常用字符

> **[yiduobo的每日leetcode 1002.查找常用字符](https://zhuanlan.zhihu.com/p/366179660) · 知乎 · 2021-04-19 · 赞同 0**
> 力扣：[1002. 查找常用字符](https://leetcode.cn/problems/find-common-characters/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

1002.查找常用字符

[力扣](https://leetcode-cn.com/problems/find-common-characters/)

比较基础的题目。统计每个字符串中各个字符出现的次数，然后对于每个字符而言，这些字符串统计的出现次数中的最小值即为答案中对应字符出现的次数。

最后附上python代码：

```python
class Solution(object):
    def commonChars(self, A):
        """
        :type A: List[str]
        :rtype: List[str]
        """

        char_dict = {}

        for char in A[0]:
            char_dict[char] = char_dict.get(char, 0) + 1

        for word in A[1:]:
            tmp_dict = {}
            for char in word:
                tmp_dict[char] = tmp_dict.get(char, 0) + 1

            for asc in range(97, 123):
                char = chr(asc)
                char_dict[char] = min(char_dict.get(char, 0), tmp_dict.get(char, 0))

        res = []
        for char in char_dict:
            res.extend([char] * char_dict[char])
        
        return res
```
