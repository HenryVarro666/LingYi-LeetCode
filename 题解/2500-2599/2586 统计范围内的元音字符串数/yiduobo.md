---
title: "2586. 统计范围内的元音字符串数"
aliases: ["yiduobo的每日leetcode 2586.统计范围内的元音字符串数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/642978400"
zhihu_id: "642978400"
zhihu_title: "yiduobo的每日leetcode 2586.统计范围内的元音字符串数"
question_id: "2586"
question: "统计范围内的元音字符串数"
problem_url: "https://leetcode.cn/problems/count-the-number-of-vowel-strings-in-range/"
difficulty: "Easy"
created: "2023-07-12T00:59:39+08:00"
updated: "2023-07-12T00:59:39+08:00"
upvotes: 0
comments: 0
---

# 2586. 统计范围内的元音字符串数

> **[yiduobo的每日leetcode 2586.统计范围内的元音字符串数](https://zhuanlan.zhihu.com/p/642978400) · 知乎 · 2023-07-12 · 赞同 0**
> 力扣：[2586. 统计范围内的元音字符串数](https://leetcode.cn/problems/count-the-number-of-vowel-strings-in-range/) · Easy · 灵茶山艾府：[遍历（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2586.统计范围内的元音字符串数

[力扣](https://leetcode.cn/problems/count-the-number-of-vowel-strings-in-range/)

直接枚举范围[l, r]内的所有字符串，检测当前字符串的首位字符是否都是元音字符，若是，则更新答案。

最后附上python代码：

```python
class Solution(object):
    def vowelStrings(self, words, left, right):
        """
        :type words: List[str]
        :type left: int
        :type right: int
        :rtype: int
        """

        vowel_set = set(['a', 'e', 'i', 'o', 'u'])
        res = 0
        for w in words[left : right + 1]:
            if w[0] in vowel_set and w[-1] in vowel_set:
                res += 1
        
        return res
```
