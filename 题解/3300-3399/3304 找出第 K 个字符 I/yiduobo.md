---
title: "3304. 找出第K个字符I"
aliases: ["yiduobo的每日leetcode 3304.找出第K个字符I"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1091055353"
zhihu_id: "1091055353"
zhihu_title: "yiduobo的每日leetcode 3304.找出第K个字符I"
question_id: "3304"
question: "找出第 K 个字符 I"
problem_url: "https://leetcode.cn/problems/find-the-k-th-character-in-string-game-i/"
difficulty: "Easy"
created: "2024-10-15T00:28:32+08:00"
updated: "2024-10-15T00:28:32+08:00"
upvotes: 1
comments: 0
---

# 3304. 找出第K个字符I

> **[yiduobo的每日leetcode 3304.找出第K个字符I](https://zhuanlan.zhihu.com/p/1091055353) · 知乎 · 2024-10-15 · 赞同 1**
> 力扣：[3304. 找出第 K 个字符 I](https://leetcode.cn/problems/find-the-k-th-character-in-string-game-i/) · Easy · 灵茶山艾府：[O(1) 做法，一行代码解决（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3304.找出第K个字符I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-k-th-character-in-string-game-i/)

题目给出一个字符串word，初始状态下word \= 'a'。接下来每一轮，word中的每个字符都将生成字母表中的下一个字符，z将生成a，并将所有生成的字符按顺序拼接在word的后面。例如c将变成cd，而zb将变成zbac。

现在在问经过若干轮操作后，若word中至少具有k个字符，第k个字符是什么。

题目中k的范围较小，那么就可以直接暴力模拟整个操作的过程直到字符串的长度大于等于k，然后返回其中第k个字符即可。

最后附上python代码：

```python
class Solution(object):
    def kthCharacter(self, k):
        """
        :type k: int
        :rtype: str
        """

        chars = ['a']
        while len(chars) < k:
            for index in range(len(chars)):
                chars.append(chr((ord(chars[index]) - 97 + 1) % 26 + 97))
        
        return chars[k - 1]
```
