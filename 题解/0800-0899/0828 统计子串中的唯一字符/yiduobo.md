---
title: "828. 统计子串中的唯一字符"
aliases: ["yiduobo的每日leetcode 828.统计子串中的唯一字符"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/string", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/344813526"
zhihu_id: "344813526"
zhihu_title: "yiduobo的每日leetcode 828.统计子串中的唯一字符"
question_id: "828"
question: "统计子串中的唯一字符"
problem_url: "https://leetcode.cn/problems/count-unique-characters-of-all-substrings-of-a-given-string/"
difficulty: "Hard"
rating: 2034
created: "2021-01-21T22:20:57+08:00"
updated: "2021-01-21T22:20:57+08:00"
upvotes: 0
comments: 0
---

# 828. 统计子串中的唯一字符

> **[yiduobo的每日leetcode 828.统计子串中的唯一字符](https://zhuanlan.zhihu.com/p/344813526) · 知乎 · 2021-01-21 · 赞同 0**
> 力扣：[828. 统计子串中的唯一字符](https://leetcode.cn/problems/count-unique-characters-of-all-substrings-of-a-given-string/) · Hard · 灵茶山艾府：[一次遍历：用变化量来思考（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

828.统计子串中的唯一字符

[力扣](https://leetcode-cn.com/problems/count-unique-characters-of-all-substrings-of-a-given-string/)

题目描述得比较复杂，简单来说就是对于一个字符串，若该字符串中只出现了一次的字符数量为k，那么就记这个子串得k分。现在给出一个字符串s，要求s的所有子串的总得分是多少。

题目描述的角度是从字符串出发的，我们也从单个字符的角度出发，例如样例ABC：

1、对于A，其可以在字符串A、AB、ABC中计分，那么其得分为3

2、对于B，其可以在字符串AB、B、BC、ABC中计分，那么其得分为4

3、对于C，其可以在字符串C、BC、ABC中计分，那么其得分为3

因此最终答案为10

再看样例ABA：

1、对于第一个A，其可以在A、AB中计分，但不能在ABA中计分，因此其得分为2

2、对于B，其可以在AB、B、BA、ABA中计分，那么其得分为4

3、对于第二个A，其可以在BA、A中计分，但不能在ABA中计分，因此其得分为2

因此最终答案为8

到了这里，可以得知对于单个字母而言，其得分就是其单独出现的所有子串的个数。

对于位于index的字母，我们可以先计算出其该字母上一次出现的位置prev，以及下一次出现的位置next，那么该字符可以往左侧扩展的长度就是index - prev，可以往右扩展的长度则为next - index，因此可形成的合法子串数量就是(index - prev) \* (next - index)

而对于prev以及next的计算，则可以通过正反两趟扫描使用动态规划计算得到。

于是现在的做法就是先计算出prev以及next，然后逐个遍历字符串中的每个字母，通过prev以及next统计当前字母的得分并累加到答案。

最后附上python代码：

```python
class Solution(object):
    def uniqueLetterString(self, s):
        """
        :type s: str
        :rtype: int
        """

        if not s:
            return 0

        mod = 10 ** 9 + 7
        n = len(s)
        prev = [{s[0] : 0}]
        for index in range(1, n):
            prev.append(prev[-1].copy())
            prev[-1][s[index]] = index
        next = [{s[n - 1] : n - 1}]
        for index in range(n - 2, -1, -1):
            next.append(next[-1].copy())
            next[-1][s[index]] = index
        next.reverse()
        
        res = 0
        for index, char in enumerate(s):
            if index == 0:
                prev_pos = -1
            else:
                prev_pos = prev[index - 1].get(char, -1)
            
            if index == n - 1:
                next_pos = n
            else:
                next_pos = next[index + 1].get(char, n)
            
            res += (index - prev_pos) * (next_pos - index)
            res %= mod

        return res
```
