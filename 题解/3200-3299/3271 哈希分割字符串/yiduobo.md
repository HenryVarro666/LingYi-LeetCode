---
title: "3271. 哈希分割字符串"
aliases: ["yiduobo的每日leetcode 3271.哈希分割字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/784012120"
zhihu_id: "784012120"
zhihu_title: "yiduobo的每日leetcode 3271.哈希分割字符串"
question_id: "3271"
question: "哈希分割字符串"
problem_url: "https://leetcode.cn/problems/hash-divided-string/"
difficulty: "Medium"
created: "2024-10-01T00:21:04+08:00"
updated: "2024-10-01T00:21:04+08:00"
upvotes: 1
comments: 0
---

# 3271. 哈希分割字符串

> **[yiduobo的每日leetcode 3271.哈希分割字符串](https://zhuanlan.zhihu.com/p/784012120) · 知乎 · 2024-10-01 · 赞同 1**
> 力扣：[3271. 哈希分割字符串](https://leetcode.cn/problems/hash-divided-string/) · Medium · 灵茶山艾府：[模拟（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3271.哈希分割字符串

[. - 力扣（LeetCode）](https://leetcode.cn/problems/hash-divided-string/description/)

题目给出一个长度为n的仅包含小写字母的字符串s和一个整数k，这里的n为k的倍数。接下来要求将s按从前往后的顺序分割成n // k个长度为k的子串，对于每个子串，将其中每个字符在字母表中顺序累加起来后对26取模，得到hashedChar，再将字母表中第hashedChar个字符添加到最终答案里面。现在要求计算出最终答案。

直接按照题目要求模拟即可。先以k为步长遍历所有子串的起点，然后对于每个起点，往后遍历k个字符，计算这些字符在字母表中的顺序之和。字符在字母表中的顺序可以利用字符的ascii码减去'a'的ascii码计算得到，而字母表中的第hashedChar个字符的ascii码也可以通过hashedChar加上'a'的ascii码计算得到。

最后附上python代码：

```python
class Solution(object):
    def stringHash(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: str
        """

        res = []
        for index in range(0, len(s), k):
            h = sum([ord(c) - 97 for c in s[index : index + k]]) % 26
            res.append(chr(h + 97))
        
        return ''.join(res)
```
