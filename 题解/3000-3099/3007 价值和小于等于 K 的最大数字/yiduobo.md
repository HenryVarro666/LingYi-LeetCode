---
title: "3007. 价值和小于等于K的最大数字"
aliases: ["yiduobo的每日leetcode 3007.价值和小于等于K的最大数字"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/recursion", "leetcode/memoization", "leetcode/math", "leetcode/binary-search", "leetcode/dynamic-programming", "题单/二分算法", "题单/动态规划", "题单/位运算", "题单/二分算法/二-二分答案", "题单/动态规划/十-数位-DP", "题单/位运算/五-试填法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/693652288"
zhihu_id: "693652288"
zhihu_title: "yiduobo的每日leetcode 3007.价值和小于等于K的最大数字"
question_id: "3007"
question: "价值和小于等于 K 的最大数字"
problem_url: "https://leetcode.cn/problems/maximum-number-that-sum-of-the-prices-is-less-than-or-equal-to-k/"
difficulty: "Medium"
rating: 2258
created: "2024-04-21T03:42:05+08:00"
updated: "2024-04-21T03:42:05+08:00"
upvotes: 1
comments: 0
---

# 3007. 价值和小于等于K的最大数字

> **[yiduobo的每日leetcode 3007.价值和小于等于K的最大数字](https://zhuanlan.zhihu.com/p/693652288) · 知乎 · 2024-04-21 · 赞同 1**
> 力扣：[3007. 价值和小于等于 K 的最大数字](https://leetcode.cn/problems/maximum-number-that-sum-of-the-prices-is-less-than-or-equal-to-k/) · Medium · 灵茶山艾府：[三种方法：二分答案+数位 DP/数学公式/试填法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3007.价值和小于等于K的最大数字

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-number-that-sum-of-the-prices-is-less-than-or-equal-to-k/description/)

对于这类问题，一种常见的思路是先观察2的幂次中的规律，然后想办法从高位向低位进行构造。而对于本题，则可以先观察0到15中的1在第x位上分布的情况。

首先考察最简单的x \= 1的情况。

0000、0001 -> 0-1中总计1个1

0010、0011 -> 2-3中总计3个1

0100、0101、0110、0111 -> 4-7中总计8个1

1000、1001、1010、1011、1100、1101、1110、1111 -> 8-15中总计20个1

如果注意对齐

第一组：

0000、0001

0010、0011

第二组：

0000、0001、0010、0011

0100、0101、0110、0111

第三组：

0000、0001、0010、0011、0100、0101、0110、0111

1000、1001、1010、1011、1100、1101、1110、1111

换言之，所有的2^(i - 1)到2^i - 1之间的数相比与0到2^(i - 1) - 1之间的数刚好是在最高位上多出一个1。

更形式化的，令f[i]表示0到2^i - 1之间有多少个1，那么就有f[i] \= f[i - 1] \* 2 + 2^(i - 1)。其中两倍的f[i - 1]对应的是低位对齐部分的1，而2^(i - 1)则对应的是2^(i - 1)到2^i - 1这些数的最高位上的1。

上面讨论的是x \= 1的情况，而对于x > 1的情况，处理方法也是类似。

对于f[i]，首先依然有f[i] \= f[i - 1] \* 2。另外，如果i是x的倍数，那么此时2^(i - 1)到2^i - 1这些数的最高位就是x的倍数，此时应该将2^(i - 1)累加到f[i]中；反之，就应该跳过这一步。

到了这里，就可以先不断向上计算f[i]，直到当前的f[i]大于k为止。至此，就得到了最终答案的位数i。

显然，最终答案的最高位也就是第i位一定为1，接下来就可以从第i - 1位开始向后构造。

对于答案的第m位，如果其为1，也就是说答案的前缀为1.....1，就相当于需要将1.....100...000、1.....100...001、...、1.....111...111这些数中处于x倍数位上的1也加入到答案中。

对于这些数，不妨分为两个部分来计算。

第一个部分是答案的前缀1.....1。由于是从高位到低位逐位填充的，那么在这里就可以计算出这个前缀本身有多少位处于x的倍数上，记为preifx_one。这里一共有2^(m - 1)个数，因此可以提供prefix_one \* 2^(m - 1)个位于x的倍数位上的1。

第二个部分就是所有的这些后缀，刚好是从00...000到11...111，其对应的恰好就是最开始预处理得到的f[m - 1]。

因此，如果将答案的第m位置为1，那么就会添加prefix_one \* 2^(m - 1) + f[m - 1]个额外的1，不妨记为cnt。那么当cnt小于k时，就应该将第m位置为1，并将cnt减去k，反之就应该将第m位置为0。

填充好第m位之后，就可以继续填充后续的低位来适配当前剩余的cnt了。

需要注意的是，上面这种按位填充的做法找出的v是通过每一步都计算小于v的数带来的影响计算得到的，因此找出来的数v实际上表示的是0到v - 1之间的数中处于x倍数位上的1的数目之和不超过k，因此最终答案应该是v - 1而不是找到的v。

最后附上python代码：

```python
class Solution(object):
    def findMaximumNumber(self, k, x):
        """
        :type k: int
        :type x: int
        :rtype: int
        """

        f = [0]
        p = 1
        while f[-1] <= k:
            f.append(f[-1] + f[-1])
            if p % x == 0:
                f[-1] += (1 << (p - 1)) 
            p += 1

        print(f)

        p -= 1
        res = 1 << (p - 1)
        if p % x == 0:
            prefix_one = 1
        else:
            prefix_one = 0
        k -= f[-2]

        for index in range(p - 1, 0, -1):
            cnt = prefix_one * (1 << (index - 1)) + f[index - 1]

            if cnt <= k:
                res |= 1 << (index - 1)
                k -= cnt
                if index % x == 0:
                    prefix_one += 1
        
        return res - 1
```
