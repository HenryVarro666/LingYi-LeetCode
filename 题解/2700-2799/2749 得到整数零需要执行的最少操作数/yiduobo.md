---
title: "2749. 得到整数零需要执行的最少操作数"
aliases: ["yiduobo的每日leetcode 2749.得到整数零需要执行的最少操作数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/enumeration", "题单/位运算", "题单/贪心算法", "题单/位运算/八-思维题", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/654101142"
zhihu_id: "654101142"
zhihu_title: "yiduobo的每日leetcode 2749.得到整数零需要执行的最少操作数"
question_id: "2749"
question: "得到整数零需要执行的最少操作数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-the-integer-zero/"
difficulty: "Medium"
rating: 2132
created: "2023-09-04T01:37:40+08:00"
updated: "2023-09-04T01:37:40+08:00"
upvotes: 0
comments: 0
---

# 2749. 得到整数零需要执行的最少操作数

> **[yiduobo的每日leetcode 2749.得到整数零需要执行的最少操作数](https://zhuanlan.zhihu.com/p/654101142) · 知乎 · 2023-09-04 · 赞同 0**
> 力扣：[2749. 得到整数零需要执行的最少操作数](https://leetcode.cn/problems/minimum-operations-to-make-the-integer-zero/) · Medium · 灵茶山艾府：[上下界分析 + 枚举答案（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2749.得到整数零需要执行的最少操作数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-operations-to-make-the-integer-zero/)

题目给出两个数num1和num2，要求找出满足等式num1 \= k \* num2 + 2^p[0] + 2^p[1] + ... 2^p[k - 1]的最小的k。由于涉及到2的幂次，那么不妨将k \* num2也移动到左侧，记v \= num1 - k \* num2，然后从二进制位的角度来考虑问题如何通过构造p数组得到v。

可以明确的是，如果题目有解，那么这个最小的k不会太大，因为v中的二进制位上的1是有限的，于是可以从1开始向上枚举k，检测对于当前的k是否能构造出幂次数组p。

对于当前的v，若这个值小于等于0，那么对于当前的k是不存在构造数组p的方法的，同时随着k的增大，这个值必然还是负数，因此说明无解，此时直接返回-1即可。

而对于v大于0的情况，若v二进制表示中1的数量有t个，那么p数组的长度就至少要等于t，也就是说这里的k必须要大于等于t。而对于p数组长度的上限，也就是当前k的上限，则恰好等于v，也就是数组p长度为v，且其中全都是0。也就是说，若此时的t \<\= k \<\= v，那么就存在一种可行的构造方案，此时的k就是最终答案了。

在这里补充一下为什么必然存在可行的构造方案。对于2^m，其可以写成

2^m

2^(m - 1) + 2^(m - 1)

2^(m - 1) + 2^(m - 2) + 2^(m - 2)

2^(m - 2) + 2^(m - 2) + 2^(m - 2) + 2^(m - 2)

2^(m - 2) + 2^(m - 2) + 2^(m - 2) + 2^(m - 3) + 2^(m - 3)

...

2^0 + 2^0 + ... + 2^0

可以发现，每次只需将当前表达式中次数最高的项拆分成两个次数减一的项，就可以得到一个项数加1的构造方案，也就是说对于2^m，可以构造出长度在1到2^m之间数组p，因此对于上面提到的v，其可以拆分为t个2的幂次，因此可以构造出长度在t到v之间的数组p来得到v。

最后附上python代码：

```python
class Solution(object):
    def makeTheIntegerZero(self, num1, num2):
        """
        :type num1: int
        :type num2: int
        :rtype: int
        """

        k = 1
        while num1 - num2 * k > 0:
            v = num1 - num2 * k
            t = sum([int(x) for x in list(bin(v)[2:])])
            if t <= k <= v:
                return k
            k += 1
        
        return -1
```
