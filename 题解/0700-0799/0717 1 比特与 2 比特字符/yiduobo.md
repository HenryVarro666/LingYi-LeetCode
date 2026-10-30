---
title: "717. 1比特与2比特字符"
aliases: ["yiduobo的每日leetcode 717.1比特与2比特字符"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/330936042"
zhihu_id: "330936042"
zhihu_title: "yiduobo的每日leetcode 717.1比特与2比特字符"
question_id: "717"
question: "1 比特与 2 比特字符"
problem_url: "https://leetcode.cn/problems/1-bit-and-2-bit-characters/"
difficulty: "Easy"
created: "2020-12-04T23:36:30+08:00"
updated: "2020-12-04T23:36:30+08:00"
upvotes: 0
comments: 0
---

# 717. 1比特与2比特字符

> **[yiduobo的每日leetcode 717.1比特与2比特字符](https://zhuanlan.zhihu.com/p/330936042) · 知乎 · 2020-12-04 · 赞同 0**
> 力扣：[717. 1 比特与 2 比特字符](https://leetcode.cn/problems/1-bit-and-2-bit-characters/) · Easy · 灵茶山艾府：[题意解读，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

717.1比特与2比特字符

[力扣](https://leetcode-cn.com/problems/1-bit-and-2-bit-characters/)

由于1比特字符和2比特字符的起头不一样，因此我们可以从头开始往后扫描，若当前字符为0，那么必须解码成1比特字符；若当前字符为1，那么必须连同下一个字符一起解码成2比特字符。依次解码所有字符，判断最后一个解码的字符是否为1比特即可。

最后附上python代码：

```python
class Solution(object):
    def isOneBitCharacter(self, bits):
        """
        :type bits: List[int]
        :rtype: bool
        """

        now = 0
        while now < len(bits):
            if bits[now] == 1:
                now += 2
            else:
                now += 1
                if now == len(bits):
                    return True

        return False
```
