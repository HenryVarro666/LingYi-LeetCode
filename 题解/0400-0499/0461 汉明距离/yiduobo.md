---
title: "461. 汉明距离"
aliases: ["yiduobo的每日leetcode 461.汉明距离"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/222954443"
zhihu_id: "222954443"
zhihu_title: "yiduobo的每日leetcode 461.汉明距离"
question_id: "461"
question: "汉明距离"
problem_url: "https://leetcode.cn/problems/hamming-distance/"
created: "2020-09-07T20:05:02+08:00"
updated: "2020-09-07T20:05:02+08:00"
upvotes: 0
comments: 0
---

# 461. 汉明距离

> **[yiduobo的每日leetcode 461.汉明距离](https://zhuanlan.zhihu.com/p/222954443) · 知乎 · 2020-09-07 · 赞同 0**
> 力扣：[461. 汉明距离](https://leetcode.cn/problems/hamming-distance/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

461.汉明距离<https://leetcode-cn.com/problems/hamming-distance/>

汉明距离指的是二进制下两个数不同位置的数目，那么很自然就想到对两个数取异或，异或结果中1的个数就是汉明距离。而对于统计1的个数，则可以通过x & x - 1这个操作逐个分离出x的最低位的1，然后统计其个数即可。

最后附上python代码：

```python
class Solution(object):
    def hammingDistance(self, x, y):
        """
        :type x: int
        :type y: int
        :rtype: int
        """

        x ^= y
        res = 0
        while x:
            x &= x - 1
            res += 1
        return res
```
