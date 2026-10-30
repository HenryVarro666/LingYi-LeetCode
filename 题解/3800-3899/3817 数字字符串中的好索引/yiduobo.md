---
title: "3817. 数字字符串中的好索引"
aliases: ["yiduobo的每日leetcode 3817.数字字符串中的好索引"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1997070916656570551"
zhihu_id: "1997070916656570551"
zhihu_title: "yiduobo的每日leetcode 3817.数字字符串中的好索引"
question_id: "3817"
question: "数字字符串中的好索引"
problem_url: "https://leetcode.cn/problems/good-indices-in-a-digit-string/"
created: "2026-01-23T01:50:41+08:00"
updated: "2026-01-23T01:50:45+08:00"
upvotes: 0
comments: 0
---

# 3817. 数字字符串中的好索引

> **[yiduobo的每日leetcode 3817.数字字符串中的好索引](https://zhuanlan.zhihu.com/p/1997070916656570551) · 知乎 · 2026-01-23 · 赞同 0**
> 力扣：[3817. 数字字符串中的好索引](https://leetcode.cn/problems/good-indices-in-a-digit-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3817.数字字符串中的好索引

<https://leetcode.cn/problems/good-indices-in-a-digit-string/>

题目给出一个由数字组成的字符串s，其长度不超过10^5。

对于s，若存在一个子串，其以索引index结尾，且其数值等于index的十进制表示，那么就称其为好索引。

要求找出s的所有好索引，并按照升序排列返回。

由于s的长度不超过10^5，那么其最大的索引也就是99999，是一个五位数。换言之，对于任意一个索引index，最多只需要截取从index开始向前的5个字符，转化为数字后与index进行比较就行了。

单次截取和转化的时间复杂度都很低，因此在这里可以直接暴力遍历所有的索引index，截取index对应长度的字符串，转化为数字后与index进行比较。若相等，则将index加入到答案中。

最后附上python代码：

```python
class Solution(object):
    def goodIndices(self, s):
        """
        :type s: str
        :rtype: List[int]
        """
        
        res = []
        for index in range(len(s)):
            length = len(str(index))
            if int(s[index - length + 1: index + 1]) == index:
                res.append(index)
        
        return res
```
