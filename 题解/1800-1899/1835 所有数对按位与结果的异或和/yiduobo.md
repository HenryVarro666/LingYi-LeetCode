---
title: "1835. 所有数对按位与结果的异或和"
aliases: ["yiduobo的每日leetcode 1835.所有数对按位与结果的异或和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "题单/位运算", "题单/位运算/四-拆位-/-贡献法", "题单/位运算/六-恒等式"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/468860104"
zhihu_id: "468860104"
zhihu_title: "yiduobo的每日leetcode 1835.所有数对按位与结果的异或和"
question_id: "1835"
question: "所有数对按位与结果的异或和"
problem_url: "https://leetcode.cn/problems/find-xor-sum-of-all-pairs-bitwise-and/"
difficulty: "Hard"
rating: 1825
created: "2022-02-17T23:14:09+08:00"
updated: "2022-02-17T23:14:09+08:00"
upvotes: 0
comments: 0
---

# 1835. 所有数对按位与结果的异或和

> **[yiduobo的每日leetcode 1835.所有数对按位与结果的异或和](https://zhuanlan.zhihu.com/p/468860104) · 知乎 · 2022-02-17 · 赞同 0**
> 力扣：[1835. 所有数对按位与结果的异或和](https://leetcode.cn/problems/find-xor-sum-of-all-pairs-bitwise-and/) · Hard · 灵茶山艾府：[Python 一行](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1835.所有数对按位与结果的异或和

[力扣](https://leetcode-cn.com/problems/find-xor-sum-of-all-pairs-bitwise-and/)

题目的数据规模比较大，直接两两枚举然后计算显然是不行的。注意到题目这里的先对所有数对进行与操作，然后对这些结果进行异或操作，两步都是位运算，那么不妨从位的角度来看问题。

首先执行与操作。设arr1中有l1个数，arr2中有l2个数，那么两两与的话一共会产生l1 \* l2个结果。对于这些结果再执行异或运算。对于其中的某一位而言，其最终异或的结果可能是0或者1，这取决于之前的l1 \* l2个结果中该位上的1是偶数个还是奇数个。

对于这个问题也很好判别。设arr1中有p1个数该位为1，arr2中有p2个数该位为1。由于一个数对中必须两个数该位都是1，二者与运算的结果才为1，那么最终这l1 \* l2个与运算的结果中就只有p1 \* p2个结果在该位上位1，那么就可以通过判断p1 \* p2的奇偶性来决定最终异或结果在这一位上是0还是1。

于是现在就有了一种做法。枚举二进制中的每一位，分别计算arr1和arr2中这一位上为1的数的个数，根据二者乘积的奇偶性决定最终答案在这一位上是0还是1。

最后附上python代码：

```python
class Solution(object):
    def getXORSum(self, arr1, arr2):
        """
        :type arr1: List[int]
        :type arr2: List[int]
        :rtype: int
        """

        maxn = max(max(arr1), max(arr2))
        pow2 = [1]
        while pow2[-1] + pow2[-1] <= maxn:
            pow2.append(pow2[-1] + pow2[-1])

        res = 0
        for p in pow2:
            cnt1 = cnt2 = 0
            for num in arr1:
                if num & p:
                    cnt1 += 1
            for num in arr2:
                if num & p:
                    cnt2 += 1
            
            if cnt1 % 2 == 1 and cnt2 % 2 == 1:
                res += p
        
        return res
```
