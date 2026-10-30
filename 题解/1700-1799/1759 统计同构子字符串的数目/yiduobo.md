---
title: "1759. 统计同构子字符串的数目"
aliases: ["yiduobo的每日leetcode 1759.统计同构子字符串的数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/459627301"
zhihu_id: "459627301"
zhihu_title: "yiduobo的每日leetcode 1759.统计同构子字符串的数目"
question_id: "1759"
question: "统计同构子字符串的数目"
problem_url: "https://leetcode.cn/problems/count-number-of-homogenous-substrings/"
created: "2022-01-19T23:23:16+08:00"
updated: "2022-01-19T23:23:16+08:00"
upvotes: 0
comments: 0
---

# 1759. 统计同构子字符串的数目

> **[yiduobo的每日leetcode 1759.统计同构子字符串的数目](https://zhuanlan.zhihu.com/p/459627301) · 知乎 · 2022-01-19 · 赞同 0**
> 力扣：[1759. 统计同构子字符串的数目](https://leetcode.cn/problems/count-number-of-homogenous-substrings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1759.统计同构子字符串的数目

[力扣](https://leetcode-cn.com/problems/count-number-of-homogenous-substrings/)

由于题目定义了同构子字符串必须所有字符都相同，那么一个很自然的想法就是将字符串中的连续字符切分出来然后分别考察。

对于一个长度为k的由同一个字符构成的字符串而言，其可以构成k个长度为1的同构子字符串，k - 1个长度为2的同构子字符串，以此类推，最终是构成一个长度为k的同构子字符串。那么这里一共就有

1 + 2 + ... + k \= (1 + k) \* k / 2个同构子字符串

于是现在的做法就是从头开始向后一趟扫描，使用一个变量cnt记录当前由相同字符构成的字符串长度。若当前字符与上一个字符相同，那么将cnt加上1，否则使用cnt \* (1 + cnt) / 2来更新答案，并将cnt置为0。

遍历完成后，要记得最后这个字符串还没有计算，因此还需要将答案再加上cnt \* (1 + cnt) / 2。

最后附上python代码：

```python
class Solution(object):
    def countHomogenous(self, s):
        """
        :type s: str
        :rtype: int
        """

        now = None
        cnt = 0
        res = 0
        mod = 10 ** 9 + 7
        for char in s:
            if char == now:
                cnt += 1
            else:
                res = (res + cnt * (cnt + 1) / 2) % mod
                now = char
                cnt = 1
        
        return (res + cnt * (cnt + 1) / 2) % mod
```
