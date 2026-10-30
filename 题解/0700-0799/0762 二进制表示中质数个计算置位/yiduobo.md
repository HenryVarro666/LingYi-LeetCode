---
title: "762. 二进制表示中质数个计数置位"
aliases: ["yiduobo的每日leetcode 762.二进制表示中质数个计数置位"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/recursion", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "leetcode/combinatorics", "题单/动态规划", "题单/数学算法", "题单/动态规划/十-数位-DP", "题单/数学算法/一-数论", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/338585823"
zhihu_id: "338585823"
zhihu_title: "yiduobo的每日leetcode 762.二进制表示中质数个计数置位"
question_id: "762"
question: "二进制表示中质数个计算置位"
problem_url: "https://leetcode.cn/problems/prime-number-of-set-bits-in-binary-representation/"
difficulty: "Easy"
rating: 1383
created: "2020-12-21T23:36:57+08:00"
updated: "2020-12-21T23:36:57+08:00"
upvotes: 0
comments: 0
---

# 762. 二进制表示中质数个计数置位

> **[yiduobo的每日leetcode 762.二进制表示中质数个计数置位](https://zhuanlan.zhihu.com/p/338585823) · 知乎 · 2020-12-21 · 赞同 0**
> 力扣：[762. 二进制表示中质数个计算置位](https://leetcode.cn/problems/prime-number-of-set-bits-in-binary-representation/) · Easy · 灵茶山艾府：[三种方法：暴力枚举 / 数位 DP / 组合数学（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

762.二进制表示中质数个计数置位

[力扣](https://leetcode-cn.com/problems/prime-number-of-set-bits-in-binary-representation/)

看题目描述，应该是可以用从短到长的位运算加动态规划来做的，不过注意到这里最多也就一百万个数，因此我在这里选择直接遍历每个数，分解其二进制表示中的每一位然后进行统计。

由于2的20次方为1048576，因此我们最大只需要考虑到19个1的情况。

最后附上python代码：

```python
class Solution(object):
    def countPrimeSetBits(self, L, R):
        """
        :type L: int
        :type R: int
        :rtype: int
        """

        res = 0
        for now in range(L, R + 1):
            cnt = 0
            while now:
                now &= now - 1
                cnt += 1
            if cnt in [2, 3, 5, 7, 11, 13, 17, 19]:
                res += 1
            
        return res
```
