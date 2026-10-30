---
title: "693. 交替位二进制数"
aliases: ["yiduobo的每日leetcode 693.交替位二进制数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "题单/位运算", "题单/位运算/一-基础题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/312273889"
zhihu_id: "312273889"
zhihu_title: "yiduobo的每日leetcode 693.交替位二进制数"
question_id: "693"
question: "交替位二进制数"
problem_url: "https://leetcode.cn/problems/binary-number-with-alternating-bits/"
difficulty: "Easy"
created: "2020-11-25T22:47:48+08:00"
updated: "2020-11-25T22:47:48+08:00"
upvotes: 0
comments: 0
---

# 693. 交替位二进制数

> **[yiduobo的每日leetcode 693.交替位二进制数](https://zhuanlan.zhihu.com/p/312273889) · 知乎 · 2020-11-25 · 赞同 0**
> 力扣：[693. 交替位二进制数](https://leetcode.cn/problems/binary-number-with-alternating-bits/) · Easy · 灵茶山艾府：[O(1) 做法原理讲解（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

693.交替位二进制数

[力扣](https://leetcode-cn.com/problems/binary-number-with-alternating-bits/)

题目要去检测n的二进制表示是否是01相间的，最直观的做法就是逐位分离判断，我在这里采用的做法是想将n右移一位得到n'，若n是01相间的，那么n'也是01相间的，而且n和n'的01正好是反过来的，此时如果将n异或上n'，设其为p，那么p必然是全1。

到了这里，问题就转化为判断p是否为全1。如果p是全1，那么p + 1就必然是100...000这种形式的数，那么此时通过p & (p + 1)是否为0就能确定p是否为全1。

最后附上python代码：

```python
class Solution(object):
    def hasAlternatingBits(self, n):
        """
        :type n: int
        :rtype: bool
        """

        p = ((n >> 1) ^ n)

        return p & (p + 1) == 0
```
