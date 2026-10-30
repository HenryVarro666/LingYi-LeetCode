---
title: "1684. 统计一致字符串的数目"
aliases: ["yiduobo的每日leetcode 1684.统计一致字符串的数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/445428199"
zhihu_id: "445428199"
zhihu_title: "yiduobo的每日leetcode 1684.统计一致字符串的数目"
question_id: "1684"
question: "统计一致字符串的数目"
problem_url: "https://leetcode.cn/problems/count-the-number-of-consistent-strings/"
created: "2021-12-15T00:04:59+08:00"
updated: "2021-12-15T00:04:59+08:00"
upvotes: 0
comments: 0
---

# 1684. 统计一致字符串的数目

> **[yiduobo的每日leetcode 1684.统计一致字符串的数目](https://zhuanlan.zhihu.com/p/445428199) · 知乎 · 2021-12-15 · 赞同 0**
> 力扣：[1684. 统计一致字符串的数目](https://leetcode.cn/problems/count-the-number-of-consistent-strings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

1684.统计一致字符串的数目

[力扣](https://leetcode-cn.com/problems/count-the-number-of-consistent-strings/)

比较基础的题目，使用allowed构造哈希表，然后检测word中的每个字符是否出现在哈希表中即可。

最后附上python代码：

```python
class Solution(object):
    def countConsistentStrings(self, allowed, words):
        """
        :type allowed: str
        :type words: List[str]
        :rtype: int
        """

        allowed_set = set()
        for char in allowed:
            allowed_set.add(char)
        
        res = len(words)
        for word in words:
            for char in word:
                if char not in allowed_set:
                    res -= 1
                    break
        
        return res
```
