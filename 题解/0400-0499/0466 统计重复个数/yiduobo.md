---
title: "466. 统计重复个数"
aliases: ["yiduobo的每日leetcode 466.统计重复个数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/228795873"
zhihu_id: "228795873"
zhihu_title: "yiduobo的每日leetcode 466.统计重复个数"
question_id: "466"
question: "统计重复个数"
problem_url: "https://leetcode.cn/problems/count-the-repetitions/"
created: "2020-09-09T20:34:40+08:00"
updated: "2020-09-09T20:34:40+08:00"
upvotes: 0
comments: 0
---

# 466. 统计重复个数

> **[yiduobo的每日leetcode 466.统计重复个数](https://zhuanlan.zhihu.com/p/228795873) · 知乎 · 2020-09-09 · 赞同 0**
> 力扣：[466. 统计重复个数](https://leetcode.cn/problems/count-the-repetitions/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

466.统计重复个数<https://leetcode-cn.com/problems/count-the-repetitions/>

这题看上去跟无限循环小数找循环节差不太多。

首先需要明确的一点是，在匹配时应该采用贪心法，尽可能地使用s1中靠前的字符去匹配s2中的字符。

接下来是需要想办法找到这个循环节。对于循环节而言，一般存在一个进入长度以及循环长度，例如1/6，答案为0.1666666...，其中0.1就是进入循环的部分，而循环节就是6。那么在这里，就需要先找出进入循环的长度unloop1与unloop2，表示用unloop1个s1可以匹配上unloop2个s2。当然，这里不一定能形成完美的匹配，于是可以记录下来用unloop1个s1匹配s2时，第unloop2 + 1个s2能匹配的位置pos。在匹配的过程中，如果再一次出现了已经出现过的pos，那么说明从老的pos到新的pos之间这一段恰好是整数个s1匹配上了整数个s2，即我们要找的循环节。

到了这里，就找到了进入循环的长度以及循环节的长度，之后通过简单的乘除法就能找出匹配的个数。当然，由于n个s1不一定恰好能全部用在循环中，那么可以将剩下的s1从pos开始继续对s2进行匹配，找出剩下能匹配的个数。

最后附上python代码：

```python
class Solution(object):
    def getMaxRepetitions(self, s1, n1, s2, n2):
        """
        :type s1: str
        :type n1: int
        :type s2: str
        :type n2: int
        :rtype: int
        """

        if not n1:
            return 0

        cnt1 = cnt2 = 0
        pos_dict = {}
        pos = 0
        while True:
            cnt1 += 1
            for char in s1:
                if char == s2[pos]:
                    pos += 1
                    if pos == len(s2):
                        cnt2 += 1
                        pos = 0

            if cnt1 == n1:
                return cnt2 / n2

            if pos in pos_dict:
                unloop1, unloop2 = pos_dict[pos]
                loop1 = cnt1 - unloop1
                loop2 = cnt2 - unloop2

                res = unloop2 + (n1 - unloop1) / loop1 * loop2
                for index in range((n1 - unloop1) % loop1):
                    for char in s1:
                        if char == s2[pos]:
                            pos += 1
                            if pos == len(s2):
                                res += 1
                                pos = 0
                
                return res/n2

            else:
                pos_dict[pos] = [cnt1, cnt2]
```
