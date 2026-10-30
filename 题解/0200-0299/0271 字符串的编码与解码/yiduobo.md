---
title: "271. 字符串的编码与解码"
aliases: ["yiduobo的每日leetcode 271.字符串的编码与解码"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/593968673"
zhihu_id: "593968673"
zhihu_title: "yiduobo的每日leetcode 271.字符串的编码与解码"
question_id: "271"
question: "字符串的编码与解码"
problem_url: "https://leetcode.cn/problems/encode-and-decode-strings/"
created: "2022-12-24T02:48:14+08:00"
updated: "2022-12-24T02:48:14+08:00"
upvotes: 0
comments: 0
---

# 271. 字符串的编码与解码

> **[yiduobo的每日leetcode 271.字符串的编码与解码](https://zhuanlan.zhihu.com/p/593968673) · 知乎 · 2022-12-24 · 赞同 0**
> 力扣：[271. 字符串的编码与解码](https://leetcode.cn/problems/encode-and-decode-strings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

271.字符串的编码与解码

[力扣](https://leetcode.cn/problems/encode-and-decode-strings/)

本题主要需要实现的是如何将字符串数组中每个字符串的长度通过某种编码方式或者其他手段融入到密文中，而这个密文也能无歧义地解码出每个字符串的长度从而还原出字符串。

从题目的意思来看，字符串中字符的ascii码取值范围可能在0到255之间，同时单个字符串的长度也没有给出上限，因此通过指定某种特殊符号作为分隔符，或者划分某个特殊区域记录下一个字符串长度的做法都是有问题的。

注意到题目中的ascii码取值范围是8位的二进制，那么如果将其拆分为两个4位的二进制，实际需要占用的ascii码的数量就从256变成了16，此时就可以使用长度为2，取值范围在从'a'开始的16个字符所构成的字符串来表示原字符串中的任意字符了。另一方面，此时也就解放了其他的字符，因此可以使用其他字符来做特殊标识，表示当前字符串已经结束，从而达成题目的需求。

最后附上python代码：

```python
class Codec:

    def encode(self, strs):
        """Encodes a list of strings to a single string.
        
        :type strs: List[str]
        :rtype: str
        """

        res = []
        for s in strs:
            for char in s:
                v = ord(char)
                res.append(chr(v / 16 + 97))
                res.append(chr(v % 16 + 97))
            res.append('00')
        
        return ''.join(res)

    def decode(self, s):
        """Decodes a single string to a list of strings.
        
        :type s: str
        :rtype: List[str]
        """
        res = []
        tmp = []
        for i in range(0, len(s), 2):
            if s[i] != '0':
                tmp.append(chr((ord(s[i]) - 97) * 16 + ord(s[i + 1]) - 97))
            else:
                res.append(''.join(tmp))
                tmp = []
        
        return res

# Your Codec object will be instantiated and called as such:
# codec = Codec()
# codec.decode(codec.encode(strs))
```
