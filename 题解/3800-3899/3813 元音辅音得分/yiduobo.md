---
title: "3813. 元音辅音得分"
aliases: ["yiduobo的每日leetcode 3813.元音辅音得分"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1996684949244359667"
zhihu_id: "1996684949244359667"
zhihu_title: "yiduobo的每日leetcode 3813.元音辅音得分"
question_id: "3813"
question: "元音辅音得分"
problem_url: "https://leetcode.cn/problems/vowel-consonant-score/"
difficulty: "Easy"
created: "2026-01-20T21:59:01+08:00"
updated: "2026-01-20T21:59:04+08:00"
upvotes: 0
comments: 0
---

# 3813. 元音辅音得分

> **[yiduobo的每日leetcode 3813.元音辅音得分](https://zhuanlan.zhihu.com/p/1996684949244359667) · 知乎 · 2026-01-20 · 赞同 0**
> 力扣：[3813. 元音辅音得分](https://leetcode.cn/problems/vowel-consonant-score/) · Easy · 灵茶山艾府：[库函数写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3813.元音辅音得分

<https://leetcode.cn/problems/vowel-consonant-score/description/>

题目给出一个字符串s，由小写英文字母，空格和数字组成。

令v表示s中元音字母的数量，c表示辅音字母的数量。

现在要求计算s的得分score：

若c > 0，则score \= floor(v / c)，其中floor表示向下取整

若c \= 0，则score \= 0

按照题目要求模拟即可。对s进行一趟遍历，计算对应的v和c，然后计算对应的score就行了。

最后附上python代码：

```python
class Solution(object):
    def vowelConsonantScore(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        vowel = set(['a', 'e', 'i', 'o', 'u'])
        v = 0
        c = 0
        for char in s:
            if char in vowel:
                v += 1
            elif 'a' <= char <= 'z':
                c += 1
        
        if c > 0:
            return v // c
        else:
            return 0
```
