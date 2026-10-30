---
title: "564. 寻找最近的回文数"
aliases: ["yiduobo的每日leetcode 564.寻找最近的回文数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/math", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/266299399"
zhihu_id: "266299399"
zhihu_title: "yiduobo的每日leetcode 564.寻找最近的回文数"
question_id: "564"
question: "寻找最近的回文数"
problem_url: "https://leetcode.cn/problems/find-the-closest-palindrome/"
difficulty: "Hard"
created: "2020-10-16T21:37:24+08:00"
updated: "2020-10-16T21:37:46+08:00"
upvotes: 0
comments: 0
---

# 564. 寻找最近的回文数

> **[yiduobo的每日leetcode 564.寻找最近的回文数](https://zhuanlan.zhihu.com/p/266299399) · 知乎 · 2020-10-16 · 赞同 0**
> 力扣：[564. 寻找最近的回文数](https://leetcode.cn/problems/find-the-closest-palindrome/) · Hard · 灵茶山艾府：[只需考虑 5 个数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

546.寻找最近的回文数<https://leetcode-cn.com/problems/find-the-closest-palindrome/>

题目要找最近的回文数，因此可以将n从中间分成两部分，调整其中的一部分，让另一部分适配调整后的结果从而形成最终的答案。可以明确的是，应该调整前半部分让后半部分来适配，因为变动低位数字的代价比变动高位数字的代价要大。

于是我们将n分成两个部分，接下来需要调整first_part的值，然后翻转后得出答案。题目要求寻找最近的回文数，因此对于first_part，只需要考察first_part + 1，first_part - 1以及first_part保持不变这三种情况。

对于first_part + 1而言，存在一种特殊情况，即first_part\=99...9。此时通过first_part + 1形成的候选答案应该是1..0001，其中0的个数应该为n的总位数减1。

对于first_part而言，存在一种特殊情况，即翻转后得到的候选答案就是n，此时应该舍去。

对于first_part - 1而言，存在一种特殊情况，即first_part \= 100..0。此时通过first_part - 1形成的候选答案应该是99..9，其中9的个数应该为n的总位数减1。

通过这三种方法获取候选答案之后，只需要按照其与n的差的绝对值以及其自身大小选出最终的答案即可。

另外，这里n的位数可能是奇数也可能是偶数，在处理位数为奇数的翻转时需要注意处理最中间的那一位。

最后附上python代码：

```python
class Solution(object):
    def nearestPalindromic(self, n):
        """
        :type n: str
        :rtype: str
        """

        l = len(n)

        first_part = n[:(l + 1) / 2]
        if l % 2 == 1:
            same = first_part + first_part[::-1][1:]
        else:
            same = first_part + first_part[::-1]

        upper_part = str(int(first_part) + 1)
        if len(first_part) < len(upper_part):
            upper = '1' + '0' * (l - 1) + '1'
        else:
            if l % 2 == 1:
                upper = upper_part + upper_part[::-1][1:]
            else:
                upper = upper_part + upper_part[::-1]
        
        lower_part = str(int(first_part) - 1)
        if first_part == '1' or len(first_part) > len(lower_part):
            lower = '9' * (l - 1)
            if not lower:
                lower = '0'
        else:
            if l % 2 == 1:
                lower = lower_part + lower_part[::-1][1:]
            else:
                lower = lower_part + lower_part[::-1]

        same_diff = abs(int(same) - int(n))
        lower_diff = int(n) - int(lower)
        upper_diff = int(upper) - int(n)
        if lower_diff <= upper_diff:
            if same_diff == 0 or same_diff >= lower_diff:
                return lower
            else:
                return same
        else:
            if same_diff == 0 or same_diff > upper_diff:
                return upper
            else:
                return same
```
