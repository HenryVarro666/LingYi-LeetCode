---
title: "233. 数字1的个数"
aliases: ["yiduobo的每日leetcode 233.数字1的个数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/150102170"
zhihu_id: "150102170"
zhihu_title: "yiduobo的每日leetcode 233.数字1的个数"
question_id: "233"
question: "数字 1 的个数"
problem_url: "https://leetcode.cn/problems/number-of-digit-one/"
difficulty: "Hard"
created: "2020-06-22T21:31:27+08:00"
updated: "2020-06-22T21:31:27+08:00"
upvotes: 0
comments: 0
---

# 233. 数字1的个数

> **[yiduobo的每日leetcode 233.数字1的个数](https://zhuanlan.zhihu.com/p/150102170) · 知乎 · 2020-06-22 · 赞同 0**
> 力扣：[233. 数字 1 的个数](https://leetcode.cn/problems/number-of-digit-one/) · Hard · 灵茶山艾府：[两种方法：数位 DP / 数学公式（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

233.数字1的个数<https://leetcode-cn.com/problems/number-of-digit-one/>

数字1出现的次数可以认为是每一位上1出现的次数之后，于是我们从低位开始往高位考察：

1、个位上的1一定是x \* 10 + 1这种形式出现的

2、十位上的1一定是x \* 100 + (10 \~ 19)这种形式出现的

3、百位上的1一定是x \* 1000 + (100 \~ 199)这种形式出现的

4、千位上的1一定是x \* 10000 + (1000 \~ 1999)这种形式出现的

...

于是，假设我们现在需要考察(x \* 10 ^ k + p)这个数第k位上的1出现了几次，其中p是第k位以及之后的部分构成的数，那么需要统计形如

x \* 10^k + (10^(k - 1) \~ 2 \* 10^(k - 1) - 1)

的数出现了多少次。

首先，当第k + 1位为0到x - 1时，一定会出现完整的10^(k - 1)到2 \* 10^(k - 1) - 1，一共是x个10^(k - 1)个1。

例如对于六位数28XXXX考察其千位上的1，那么一定会出现1000\~1999，11000\~11999，...，281000\~281999，这里一共有28 \* 10 ^ 3 \= 28000个1。

上面统计的是0\~x \* 10^k - 1这些数中有多少个1，而对于x \* 10^k到x \* 10^k + p这一段中也可能会出现1，这里就需要对比p和10^(k - 1)的大小了：

1、若p小于10^(k - 1)，那么此时x \* 10^k到x \* 10^k + p这一段中第k位上不会出现1。例如280999，其中p\=999小于10^(k - 1)，于是280000到280999这一段千位上是没有1的。

2、若p大于等于2 \* 10^(k - 1) - 1，那么此时x \* 10^k到x \* 10^k + p这一段中第k位上将会出现10^(k - 1)个1。例如281999，其中p\=1999等于2 \* 10^(k - 1) - 1，于是280000到281999这一段千位上会有281000到281999一共1000个1。

3、若p位于10^(k - 1)到2 \* 10^(k - 1) - 1之间，那么此时x \* 10^k到x \* 10^k + p这一段中第k位上将会出现p - 10^(k-1) + 1个1。例如81234，其中p\=1234位于1000到1999之间，于是280000到281234这一段千位上会有281000到81234一共1235个1。

于是现在就有了一种做法：对于整数n，从低位开始往高位遍历，考察当前位上会出现多少个1。

1、不妨设当前计算到第k位，那么首先通过n / 10^k，可以获得从0到n / 10^k - 1这些作为高位起头的1的个数，一共是(n / 10^k) \* 10^(k - 1)个。

2、接下来考察以n / 10^k起头的1的个数，通过n % 10^k获取到后面的k - 1位，然后对比这个结果与10^(k - 1)以及2 \* 10^(k - 1) - 1的大小，计算出1的个数。

3、所有的计算结果加和即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def countDigitOne(self, n):
        """
        :type n: int
        :rtype: int
        """

        pow10 = 10
        res = 0
        while pow10 <= n * 10:
            res += n / pow10 * (pow10 / 10)
            tmp = n % pow10
            if tmp >= pow10 / 10:
                if tmp < 2 * pow10 / 10 - 1:
                    res += tmp - pow10 / 10 + 1
                else:
                    res += pow10 / 10

            pow10 *= 10

        return res
```
