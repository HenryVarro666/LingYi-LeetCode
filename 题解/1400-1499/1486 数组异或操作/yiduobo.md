---
title: "1486. 数组异或操作"
aliases: ["yiduobo的每日leetcode 1486.数组异或操作"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/bao-li", "题单/位运算", "题单/位运算/二-异或-XOR-的性质"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/416056888"
zhihu_id: "416056888"
zhihu_title: "yiduobo的每日leetcode 1486.数组异或操作"
question_id: "1486"
question: "数组异或操作"
problem_url: "https://leetcode.cn/problems/xor-operation-in-an-array/"
difficulty: "Easy"
rating: 1181
created: "2021-10-01T15:25:51+08:00"
updated: "2021-10-01T15:25:52+08:00"
upvotes: 0
comments: 0
---

# 1486. 数组异或操作

> **[yiduobo的每日leetcode 1486.数组异或操作](https://zhuanlan.zhihu.com/p/416056888) · 知乎 · 2021-10-01 · 赞同 0**
> 力扣：[1486. 数组异或操作](https://leetcode.cn/problems/xor-operation-in-an-array/) · Easy · 灵茶山艾府：[两种方法：暴力 / O(1) 数学公式（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1486.数组异或操作

[力扣](https://leetcode-cn.com/problems/xor-operation-in-an-array/)

由于问题的规模很小，因此直接循环暴力计算也是可以的，不过这里还存在更好的数学做法。

首先，对于nums[i] \= start + 2 \* i 这种形式，如果从二进制位的角度来看，这个数的奇偶性取决于start的奇偶性，也就是说nums[i]的最后一位是0还是1取决于start是偶数还是奇数。当start为偶数时，nums中所有数的最后一位都是0，那么答案的最后一位也是0。当start为奇数时，nums中所有数的最后一位都是1，若此时的n为偶数，偶数个1异或之后的结果为1，那么答案的最后一位就是0；若n为奇数，则反过来，答案的最后一位为1。

综合起来，若start和n都为奇数时，答案的最后一位为1，否则最后一位为0。

确定了最后一位之后，在计算nums[0] ^ nums[1] ^ ... ^ nums[n - 1]时就无需再考虑最后一位了，于是可以将式子改写成

res \= (((nums[0] >> 1) ^ (nums[1] >> 1) ^ ... ^ (nums[n - 1] >> 1)) \<\< 1) + suffix

这里的suffix表示的是通过start和n确定的最后一位的值。

如果将nums[i] \= start + 2 \* i 带入上面的式子，那么要计算的式子就变成了

res \= ((start >> 1) ^ ((start >> 1) + 1) ^ ... ^ ((start >> 1) + (n - 1))) \<\< 1) + suffix

不妨设start' \= start >> 1，就有

res \= ((start' ^ (start' + 1) ^ ... ^ (start' + (n - 1))) \<\< 1) + suffix

对于括号中的连续异或，很自然想到了使用前缀异或来处理。设prefix_s[i]表示

0 ^ 1 ^ ... ^ i

那么就有

res \= ((prefix_s[start' + (n - 1)] ^ prefix_s[start' - 1]) \<\< 1) + suffix

在这里需要特别注意start' \= 0的情况，此时的前缀异或实际上就是prefix_s[start' + (n - 1)]，不需要再去异或prefix_s[start' - 1]了。

接下来分析prefix_s的求法。对于一个偶数x而言，有一个很好的性质就是

x ^ (x + 1) \= 1

因为偶数x一定可以写成XX...XXX0的形式，而x + 1则可以写成XX...XXX1的形式，二者异或之后就只剩下最后的1了。

于是在这里求解prefix_s[i]的时候，可以根据i对4的余数分成4种情况：

1、i \= 4 \* k

从0到i - 1一共是4 \* k - 1 - 0 + 1 \= 4 \* k个数，两两分组可以分出2 \* k组。每一组的异或值都是1，而这里2 \* k为偶数，因此就有0 ^ 1 ^ ... ^(i - 1) \= 0，最终prefix_s[i] \= 0 ^ i \= i

2、i \= 4 \* k + 1

从0到i一共是4 \* k + 1 - 0 + 1 \= 4 \* k + 2个数，两两分组可以分出2 \* k +1组。每一组的异或值都是1，而这里2 \* k +1为奇数，因此就有0 ^ 1 ^ ... ^ i \= 1，最终prefix_s[i] \= 1

3、i \= 4 \* k + 2

从0到i - 1一共是4 \* k + 1 - 0 + 1 \= 4 \* k + 2个数，两两分组可以分出2 \* k +1组。每一组的异或值都是1，而这里2 \* k +1为奇数，因此就有0 ^ 1 ^ ... ^ (i - 1) \= 1，最终prefix_s[i] \= 1 ^ i

4、i \= 4 \* k + 3

从0到i一共是4 \* k + 3 - 0 + 1 \= 4 \* k + 4个数，两两分组可以分出2 \* k +2组。每一组的异或值都是1，而这里2 \* k + 2为偶数，因此就有0 ^ 1 ^ ... ^ i \= 0，最终prefix_s[i] \= 0

根据以上结论，就可以在O(1)的时间复杂度内求出prefix_s[i]了。

最后附上python代码：

```python
class Solution(object):
    def xorOperation(self, n, start):
        """
        :type n: int
        :type start: int
        :rtype: int
        """

        if n & 1 and start & 1:
            suffix = 1
        else:
            suffix = 0

        start >>= 1
        end = start + n - 1

        res = self.prefix_s(end)
        if start > 0:
            res ^= self.prefix_s(start - 1)
        
        return (res << 1) + suffix

    def prefix_s(self, x):
        if x % 4 == 0:
            return x
        elif x % 4 == 1:
            return 1
        elif x % 4 == 2:
            return x ^ 1
        else:
            return 0
```
