---
title: "2939. 最大异或乘积"
aliases: ["yiduobo的每日leetcode 2939.最大异或乘积"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "题单/位运算", "题单/贪心算法", "题单/位运算/八-思维题", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/690999239"
zhihu_id: "690999239"
zhihu_title: "yiduobo的每日leetcode 2939.最大异或乘积"
question_id: "2939"
question: "最大异或乘积"
problem_url: "https://leetcode.cn/problems/maximum-xor-product/"
difficulty: "Medium"
rating: 2128
created: "2024-04-07T02:23:50+08:00"
updated: "2024-04-07T02:23:50+08:00"
upvotes: 1
comments: 0
---

# 2939. 最大异或乘积

> **[yiduobo的每日leetcode 2939.最大异或乘积](https://zhuanlan.zhihu.com/p/690999239) · 知乎 · 2024-04-07 · 赞同 1**
> 力扣：[2939. 最大异或乘积](https://leetcode.cn/problems/maximum-xor-product/) · Medium · 灵茶山艾府：[O(1) 做法！位运算的巧妙运用！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2939.最大异或乘积

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-xor-product/)

题目给出两个数a和b，然后给出一个数n，要求0到2^n - 1之间找出一个x，使得a^x与b^x的乘积最大。

首先考虑特殊情况。当n等于0时，x只能为0，此时相当于没有进行异或操作，答案就是a \* b。

接下来考虑一般情况。由于n的限制，x最大只能到2^n - 1，因此对于a和b中更高位的部分是不会与x进行异或操作的，此时可以先将其分别分离出来，记为a_high以及b_high。具体的分离方法则可以先将a或b右移n位，然后再左移n位。

得到a_high和b_high之后，将其二者分别与a和b进行异或操作，得到将与x进行异或操作的a_low和b_low。

对于a_low和b_low，由于是异或操作，不妨从二进制位的角度来考虑。对于其中的某一位，如果a_low的这一位与b_low一样，那么就可以让x在这一位上取反，使得a_low^x与b_low^x的这一位都为1，从而使得最终答案最大。记最终异或结果中这些位的值为common，那么为了计算common，则可以先记c \= a_low^b_low，也就是a_low和b_low的不同位，然后对c进行取反操作，就得到了common。

最后，则是关于c中的1应该如何分配。当c不等于0时，由于a_low和b_low在c等于1的这些位上都不同，那么无论x如何取值，异或结果中也是一个0和一个1，此时就需要将c分成first和second，使得最终的异或结果乘积最大。

由于高位的high、低位的common以及first、second表示的位数是互不相同的，因此最终的异或结果a^x \= a_high + common + first，b^x \= b_high + common + second，目标是使得这两个值的乘积最大。

将(a_high + common + first) \* (b_high + common + second)的括号打开，得到的是a_high \* b_high + (a_high + b_high + first + second) \* common + common^2 + a_high \* second + b_high \* first + first \* second

其中a_high \* b_high是定值，括号内的first + second等于c，因此括号内(a_high + b_high + c) \* common也是定值，common^2同样是定值，那么实际上就是通过a_high \* second + b_high \* first + first \* second来决定first和second应该如何分配c中的1。

1、当a_high等于b_high时：

此时a_high \* second + b_high \* first这两项也可以合并成a_high \* c从而忽略掉，那么就是要让first \* second最大。对于两数之和相等，要让两数乘积最大这个问题，很明显就应该让两数尽可能接近。由于first和second都是由2的幂次组成，那么在这里将first设置为最高次的幂次，second设置为其他的幂次之和，就可以使得first和second最接近

2、当a_high大于b_high时：

令diff \= a_high - b_high，就可以得到a_high \* second + b_high \* first + first \* second \= (b_high + diff) \* second + b_high \* first + first \* second \= b_high \* c + (diff + first) \* second。其中b_high \* c这一项是定值，因此在这里就是要使得(diff + first) \* second最大。另外又由于diff中具有比n位更高位的幂次，因此diff显然是大于c的，在这里就应该将c全部分配到second上，也就是令first \= 0，second \= c

3、当a_high小于b_high时：

与情况2对称，将c全部分配到first上，令first \= c，seoncd \= 0即可

得到first和second后，根据(a_high + common + first) \* (b_high + common + second)计算最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def maximumXorProduct(self, a, b, n):
        """
        :type a: int
        :type b: int
        :type n: int
        :rtype: int
        """

        mod = 10 ** 9 + 7

        if n == 0:
            return a * b % mod

        a_high = a >> n << n
        b_high = b >> n << n
        
        a ^= a_high
        b ^= b_high
        c = a ^ b
        common = c ^ ((1 << n) - 1)

        first = second = 0

        if c != 0:
            if a_high == b_high:
                first = (1 << (len(bin(c)) - 3))
                second = c ^ first
            elif a_high > b_high:
                first = 0
                second = c
            else:
                first = c
                second = 0

        return (a_high + common + first) * (b_high + common + second) % mod
```
