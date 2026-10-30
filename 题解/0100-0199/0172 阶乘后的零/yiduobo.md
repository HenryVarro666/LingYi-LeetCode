---
title: "172. 阶乘后的0"
aliases: ["yiduobo的每日leetcode 172.阶乘后的0"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/number-theory", "题单/数学算法", "题单/面试经典-150-题", "题单/数学算法/一-数论", "题单/面试经典-150-题/数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/144931760"
zhihu_id: "144931760"
zhihu_title: "yiduobo的每日leetcode 172.阶乘后的0"
question_id: "172"
question: "阶乘后的零"
problem_url: "https://leetcode.cn/problems/factorial-trailing-zeroes/"
difficulty: "Medium"
created: "2020-05-31T22:03:11+08:00"
updated: "2020-05-31T22:03:11+08:00"
upvotes: 0
comments: 0
---

# 172. 阶乘后的0

> **[yiduobo的每日leetcode 172.阶乘后的0](https://zhuanlan.zhihu.com/p/144931760) · 知乎 · 2020-05-31 · 赞同 0**
> 力扣：[172. 阶乘后的零](https://leetcode.cn/problems/factorial-trailing-zeroes/) · Medium · 灵茶山艾府：[严谨数学证明（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

172.阶乘后的0 <https://leetcode-cn.com/problems/factorial-trailing-zeroes/>

经典的数学题。首先，末尾的0是由于阶乘过程中因子2与因子5相乘得到的。显然5的数量少于2的数量，于是可以问题实际上就是问n的阶乘中有多少个因子5。

对于因子5而言：

1、所有能整除5的数都可以提供一个因子5。

2、所有能整除25的数都可以提供两个因子5。但是需要注意能整除25必然能整除5，因此在步骤一种已经计算过一个因子5了，在这里只需要再计算一个因子5。

3、所有能整除125的数都可以提供三个因子5。与上面相同，能整除125的数必然能整除5，也必然能整除25，因此在前面两步中已经计算了两个因子5，在这里同样只需要再计算一个因子5即可。

4、计算往后推算5的乘方，同样是只计算一次因子5。

另外，还需要知道如何计算1到n之间有多少个数能整除k。显然k，2k，3k，...，pk都能整除k，那么这里就是要找到这个p，满足pk \<\= n且(p + 1)k > n。做法很简单，直接用n除以k取整就行了。

于是我们可以不断计算5的幂次five_pow，同时计算在1到n之间有多少个数能整除five_pow，然后将其累加到答案上即可。

最后附上python代码：

```python
class Solution(object):
    def trailingZeroes(self, n):
        """
        :type n: int
        :rtype: int
        """

        res = 0
        five_pow = 5
        while n >= five_pow:
            res += n / five_pow
            five_pow *= 5

        return res
```
