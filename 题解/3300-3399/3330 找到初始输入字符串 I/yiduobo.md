---
title: "3330. 找到初始输入字符串I"
aliases: ["yiduobo的每日leetcode 3330.找到初始输入字符串I"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/24370493116"
zhihu_id: "24370493116"
zhihu_title: "yiduobo的每日leetcode 3330.找到初始输入字符串I"
question_id: "3330"
question: "找到初始输入字符串 I"
problem_url: "https://leetcode.cn/problems/find-the-original-typed-string-i/"
difficulty: "Easy"
created: "2025-02-17T22:47:32+08:00"
updated: "2025-02-17T22:47:32+08:00"
upvotes: 0
comments: 0
---

# 3330. 找到初始输入字符串I

> **[yiduobo的每日leetcode 3330.找到初始输入字符串I](https://zhuanlan.zhihu.com/p/24370493116) · 知乎 · 2025-02-17 · 赞同 0**
> 力扣：[3330. 找到初始输入字符串 I](https://leetcode.cn/problems/find-the-original-typed-string-i/) · Easy · 灵茶山艾府：[相邻相同字母的个数加一（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3330.找到初始输入字符串I

[3330. 找到初始输入字符串 I - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-original-typed-string-i/description/)

题目给出一个字符串，这个字符串是逐个字符输入得到的，但是其中可能存在至多一处误输入，这里的误输入指的是某个字符被重复输入了若干次。现在要求从s反推出一开始想要输入的字符串有多少种可能。

由于误输入是某个字符被重复输入若干次，那么误输入一定会形成相同字符形成的子串，而对于一个长度为k的由相同字符形成的子串，其可能是由长度为1到长度为k - 1的子串经过误输入得到的，也就是说一共有k - 1中可能的情况。另一方面，由于题目保证了最多只存在一处误输入，于是可以一趟遍历，将字符串分离成若干段由相同字符构成的子串，然后针对每段子串计算可能的情况，累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def possibleStringCount(self, word):
        """
        :type word: str
        :rtype: int
        """
        
        res = 0
        p = 0
        while p < len(word):
            q = p + 1
            while q < len(word) and word[q] == word[p]:
                q += 1
            
            res += q - p - 1
            p = q
        
        return res + 1
```
