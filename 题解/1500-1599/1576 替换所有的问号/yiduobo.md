---
title: "1576. 替换所有的问号"
aliases: ["yiduobo的每日leetcode 1576.替换所有的问号"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/429577344"
zhihu_id: "429577344"
zhihu_title: "yiduobo的每日leetcode 1576.替换所有的问号"
question_id: "1576"
question: "替换所有的问号"
problem_url: "https://leetcode.cn/problems/replace-all-s-to-avoid-consecutive-repeating-characters/"
created: "2021-11-04T23:30:11+08:00"
updated: "2021-11-05T22:32:45+08:00"
upvotes: 0
comments: 0
---

# 1576. 替换所有的问号

> **[yiduobo的每日leetcode 1576.替换所有的问号](https://zhuanlan.zhihu.com/p/429577344) · 知乎 · 2021-11-04 · 赞同 0**
> 力扣：[1576. 替换所有的问号](https://leetcode.cn/problems/replace-all-s-to-avoid-consecutive-repeating-characters/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1576.替换所有的问号

[力扣](https://leetcode-cn.com/problems/replace-all-s-to-avoid-consecutive-repeating-characters/)

题目并没有规定字符使用的次数，那么对于某个问号：

1、若其前面和后面都不是a，那么就将其替换成a

2、若其前面或后面中有a，但没有b，那么就将其替换成b

3、若其前后和后面中有一个a和一个b，那么就将其替换成c

根据上面的原则，从头开始向后一趟扫描，记录上一个位置的字符，或者上一个位置由问号替换后得到的字符。若当前位置为问号，那么使用记录的上一个位置的字符，结合该位置下一个字符来判断该问号应该如何处理即可。

最后附上python代码：

```python
class Solution(object):
    def modifyString(self, s):
        """
        :type s: str
        :rtype: str
        """

        res = []
        last = None
        n = len(s)
        for index, char in enumerate(s):
            if char == '?':
                if last != 'a' and (index + 1 >= n or s[index + 1] != 'a'):
                    res.append('a')
                    last = 'a'
                elif last != 'b' and (index + 1 >= n or s[index + 1] != 'b'):
                    res.append('b')
                    last = 'b'
                else:
                    res.append('c')
                    last = 'c'
            else:
                res.append(char)
                last = char
        
        return ''.join(res)
```
