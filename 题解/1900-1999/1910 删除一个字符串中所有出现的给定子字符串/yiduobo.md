---
title: "1910. 删除一个字符串中所有给定的子字符串"
aliases: ["yiduobo的每日leetcode 1910.删除一个字符串中所有给定的子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/482843978"
zhihu_id: "482843978"
zhihu_title: "yiduobo的每日leetcode 1910.删除一个字符串中所有给定的子字符串"
question_id: "1910"
question: "删除一个字符串中所有出现的给定子字符串"
problem_url: "https://leetcode.cn/problems/remove-all-occurrences-of-a-substring/"
difficulty: "Medium"
created: "2022-03-17T22:53:33+08:00"
updated: "2022-03-17T22:53:34+08:00"
upvotes: 0
comments: 0
---

# 1910. 删除一个字符串中所有给定的子字符串

> **[yiduobo的每日leetcode 1910.删除一个字符串中所有给定的子字符串](https://zhuanlan.zhihu.com/p/482843978) · 知乎 · 2022-03-17 · 赞同 0**
> 力扣：[1910. 删除一个字符串中所有出现的给定子字符串](https://leetcode.cn/problems/remove-all-occurrences-of-a-substring/) · Medium · 灵茶山艾府：[Go 简单模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1910.删除一个字符串中所有给定的子字符串

[力扣](https://leetcode-cn.com/problems/remove-all-occurrences-of-a-substring/)

字符串匹配的题目，由于数据规模并不大，那么使用平方的暴力算法也是可行的，不过使用kmp是更好的做法。

常规的kmp算法再找到匹配的子串后一般就退出了，在这里稍微有点区别。首先，再出现匹配后需要将其从答案中删去，同时用来表示part前缀匹配长度的变量pos也需要回档。关于回档，最简单的想法就是将匹配过程中的所有pos都储存起来。

当出现匹配时，则可以采取与答案相同的操作，将记录pos的这些值弹出len(part)个。若弹出操作之后g为空，那么pos就应该从0开始，否则pos应该赋值为g[-1]。

最后附上python代码：

```python
class Solution(object):
    def removeOccurrences(self, s, part):
        """
        :type s: str
        :type part: str
        :rtype: str
        """

        f = []
        m = len(part)

        pos = 0
        f.append(0)
        for index in range(1, m):
            while pos > 0 and part[pos] != part[index]:
                pos = f[pos - 1]
            if part[pos] == part[index]:
                pos += 1
            f.append(pos)

        pos = 0
        res = []
        g = []
        for index in range(len(s)):
            res.append(s[index])
            while pos > 0 and part[pos] != s[index]:
                pos = f[pos - 1]
            if part[pos] == s[index]:
                pos += 1
            g.append(pos)
            if pos == m:
                for _ in range(m):
                    res.pop()
                    g.pop()
                if g:
                    pos = g[-1]
                else:
                    pos = 0
        
        return ''.join(res)
```
