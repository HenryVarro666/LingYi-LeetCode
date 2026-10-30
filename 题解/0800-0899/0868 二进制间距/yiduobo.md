---
title: "868. 二进制间距"
aliases: ["yiduobo的每日leetcode 868.二进制间距"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "题单/位运算", "题单/位运算/一-基础题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/350258755"
zhihu_id: "350258755"
zhihu_title: "yiduobo的每日leetcode 868.二进制间距"
question_id: "868"
question: "二进制间距"
problem_url: "https://leetcode.cn/problems/binary-gap/"
difficulty: "Easy"
rating: 1307
created: "2021-02-11T11:01:49+08:00"
updated: "2021-02-11T11:01:49+08:00"
upvotes: 0
comments: 0
---

# 868. 二进制间距

> **[yiduobo的每日leetcode 868.二进制间距](https://zhuanlan.zhihu.com/p/350258755) · 知乎 · 2021-02-11 · 赞同 0**
> 力扣：[868. 二进制间距](https://leetcode.cn/problems/binary-gap/) · Easy · 灵茶山艾府：[计算尾零个数（Python/Java/C++/Go/C/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

868.二进制间距

[力扣](https://leetcode-cn.com/problems/binary-gap/)

我们需要知道n的二进制表示中1的所有位置，那么可以使用n与2的幂次进行与运算来确定当前位置上是否为1。于是现在可以维护一个变量pow2，不断将其左移同时判断当前位上是否为1，并根据这些位置来更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def binaryGap(self, n):
        """
        :type n: int
        :rtype: int
        """

        now = 1
        pos = 0
        while n & now == 0:
            pos += 1
            now <<= 1
        
        last = pos
        pos += 1
        now <<= 1
        res = 0
        while now <= n:
            while now <= n and n & now == 0:
                pos += 1
                now <<= 1
            res = max(res, pos - last)
            last = pos
            pos += 1
            now <<= 1
        
        return res
```
