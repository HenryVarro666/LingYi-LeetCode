---
title: "4030. 判断ASCII值回文"
aliases: ["yiduobo的每日leetcode 4030.判断ASCII值回文"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/string", "题单/位运算", "题单/位运算/一-基础题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2077560863314204147"
zhihu_id: "2077560863314204147"
zhihu_title: "yiduobo的每日leetcode 4030.判断ASCII值回文"
question_id: "4030"
question: "判断 ASCII 值回文"
problem_url: "https://leetcode.cn/problems/check-ascii-palindromic/"
difficulty: "Easy"
rating: 1165
created: "2026-08-31T01:13:22+08:00"
updated: "2026-08-31T01:13:22+08:00"
upvotes: 1
comments: 0
---

# 4030. 判断ASCII值回文

> **[yiduobo的每日leetcode 4030.判断ASCII值回文](https://zhuanlan.zhihu.com/p/2077560863314204147) · 知乎 · 2026-08-31 · 赞同 1**
> 力扣：[4030. 判断 ASCII 值回文](https://leetcode.cn/problems/check-ascii-palindromic/) · Easy · 灵茶山艾府：[两种方法：字符串 / 位运算（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4030.判断ASCII值回文

<https://leetcode.cn/problems/check-ascii-palindromic/description/>

题目给出一个由小写英文字母组成的字符串s。

要求将s中的每个字符替换为其ascii值对应的8位二进制表示，包括前导零，然后按照原有顺序拼接起来，构造出一个二进制字符串。

若这个字符串是回文串，则返回true，否则返回false。

最直接的做法自然是按照题目要求先进行进制转换，然后拼接得到字符串，最后从两侧向中间扫，判断是否为回文串。不过本题中构成字符串的是ascii码的二进制表示，基于这一点可以做出一些分析并进行优化。

首先，a到z的ascii码占据了97到123，而97刚好是64 + 32 + 1，也就是说这些ascii码开头的三位一定是011。而题目需要构成回文串，因此在对应的字符位上一定是110，即这些ascii码的后三位必须是110。

根据上面的结论，最终可用的字符就只有三种

- 01100110，对应的字符是f
- 01110110，对应的字符是v
- 01101110，对应的字符是n

需要注意，01111110这种情况的十进制表示是126，已经超出了a到z的范围，所以不可用。

另外，v和n必须在回文对称的位置上出现，而f则可以出现在回文对称的位置上或者字符串的正中心。于是只需两个指针left和right从s的两侧向中间扫，判断当前的字符对是否符合上面的条件即可。

最后附上python代码：

```python
class Solution(object):
    def isPalindromic(self, s):
        """
        :type s: str
        :rtype: bool
        """
        
        left = 0
        right = len(s) - 1
        # a-z => 97-122 => 011XXXXX
        # 01100110 <=> 01100110  f <=> f
        # 01101110 <=> 01110110  n <=> v
        while left < right:
            if s[left] == 'n':
                if s[right] != 'v':
                    return False
            elif s[left] == 'v':
                if s[right] != 'n':
                    return False
            elif s[left] == 'f':
                if s[right] != 'f':
                    return False
            else:
                return False
            
            left += 1
            right -= 1
        
        if left == right:
            return s[left] == "f"
        return True
```
