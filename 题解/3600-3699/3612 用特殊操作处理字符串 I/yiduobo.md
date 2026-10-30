---
title: "3612. 用特殊操作处理字符串I"
aliases: ["yiduobo的每日leetcode 3612.用特殊操作处理字符串I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1942985225379517376"
zhihu_id: "1942985225379517376"
zhihu_title: "yiduobo的每日leetcode 3612.用特殊操作处理字符串I"
question_id: "3612"
question: "用特殊操作处理字符串 I"
problem_url: "https://leetcode.cn/problems/process-string-with-special-operations-i/"
difficulty: "Medium"
created: "2025-08-24T16:29:54+08:00"
updated: "2025-08-24T16:29:55+08:00"
upvotes: 0
comments: 0
---

# 3612. 用特殊操作处理字符串I

> **[yiduobo的每日leetcode 3612.用特殊操作处理字符串I](https://zhuanlan.zhihu.com/p/1942985225379517376) · 知乎 · 2025-08-24 · 赞同 0**
> 力扣：[3612. 用特殊操作处理字符串 I](https://leetcode.cn/problems/process-string-with-special-operations-i/) · Medium · 灵茶山艾府：[模拟（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3612.用特殊操作处理字符串I

<https://leetcode.cn/problems/process-string-with-special-operations-i/description/>

题目给出一个字符串s，其长度不超过20，由小写英文字母和特殊字符\*、\#以及%组成。

现在要求按一下规则从左到右处理s中的字符，构造一个新的字符串result：

1、若当前字符是小写英文字母，则将其添加到result中

2、若当前字符是'\*'，则需要删除result中的最后一个字符(若存在)

3、若当前字符是'\#'，则复制当前的result，并追加到其自身后面

4、若当前字符是'%'，则反转当前的result

问最终的字符串result是什么。

由于s的长度不超过20，而只有复制操作才会快速让result的规模变大，那么在极限情况下，最终字符串的长度也不会超过2^19，因此完全可以暴力模拟。于是只需使用一个数组记录当前字符串，那么对于每种操作执行对应的操作即可。

最后附上python代码：

```python
class Solution(object):
    def processStr(self, s):
        """
        :type s: str
        :rtype: str
        """
        
        res = []
        for c in s:
            if c == '*':
                if res:
                    res.pop()
            elif c == '#':
                res.extend(res)
            elif c == '%':
                res.reverse()
            else:
                res.append(c)
        
        return ''.join(res)
```
