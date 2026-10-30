---
title: "1704. 判断字符串的两半是否相似"
aliases: ["yiduobo的每日leetcode 1704.判断字符串的两半是否相似"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/448760786"
zhihu_id: "448760786"
zhihu_title: "yiduobo的每日leetcode 1704.判断字符串的两半是否相似"
question_id: "1704"
question: "判断字符串的两半是否相似"
problem_url: "https://leetcode.cn/problems/determine-if-string-halves-are-alike/"
created: "2021-12-23T01:00:57+08:00"
updated: "2021-12-23T01:00:58+08:00"
upvotes: 0
comments: 0
---

# 1704. 判断字符串的两半是否相似

> **[yiduobo的每日leetcode 1704.判断字符串的两半是否相似](https://zhuanlan.zhihu.com/p/448760786) · 知乎 · 2021-12-23 · 赞同 0**
> 力扣：[1704. 判断字符串的两半是否相似](https://leetcode.cn/problems/determine-if-string-halves-are-alike/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1704.判断字符串的两半是否相似

[力扣](https://leetcode-cn.com/problems/determine-if-string-halves-are-alike/)

比较基础的题目，分别遍历字符串的前半和后半部分，计算元音字母的数量即可。

最后附上python代码：

```python
class Solution(object):
    def halvesAreAlike(self, s):
        """
        :type s: str
        :rtype: bool
        """

        char_set = set(['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'])
        p = len(s) / 2
        cnt = 0
        
        for char in s[:p]:
            if char in char_set:
                cnt += 1
        
        for char in s[p:]:
            if char in char_set:
                cnt -= 1
        
        return cnt == 0
```
