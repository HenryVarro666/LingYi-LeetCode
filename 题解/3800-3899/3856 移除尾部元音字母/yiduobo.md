---
title: "3856. 移除尾部元音字母"
aliases: ["yiduobo的每日leetcode 3856.移除尾部元音字母"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2012639235971249497"
zhihu_id: "2012639235971249497"
zhihu_title: "yiduobo的每日leetcode 3856.移除尾部元音字母"
question_id: "3856"
question: "移除尾部元音字母"
problem_url: "https://leetcode.cn/problems/trim-trailing-vowels/"
difficulty: "Easy"
created: "2026-03-06T23:02:13+08:00"
updated: "2026-03-06T23:02:16+08:00"
upvotes: 0
comments: 0
---

# 3856. 移除尾部元音字母

> **[yiduobo的每日leetcode 3856.移除尾部元音字母](https://zhuanlan.zhihu.com/p/2012639235971249497) · 知乎 · 2026-03-06 · 赞同 0**
> 力扣：[3856. 移除尾部元音字母](https://leetcode.cn/problems/trim-trailing-vowels/) · Easy · 灵茶山艾府：[循环 / 库函数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3856.移除尾部元音字母

<https://leetcode.cn/problems/trim-trailing-vowels/description/>

题目给出一个由小写字母组成的字符串s，现在要求移除s尾部所有的元音字母。

问执行完移除操作后得到的字符串是什么。

将s转化为list，然后不断检测其最后一个元素是否为元音字母，如果是，则将其pop掉。重复此过程直到list为空，或者最后一个元素不是元音字母为止。

处理完成后，将list重新转化回字符串即可。

最后附上python代码：

```python
class Solution(object):
    def trimTrailingVowels(self, s):
        """
        :type s: str
        :rtype: str
        """
        
        vowel = set(['a', 'e', 'i', 'o', 'u'])
        res = list(s)
        while res and res[-1] in vowel:
            res.pop()
        
        return ''.join(res)
```
