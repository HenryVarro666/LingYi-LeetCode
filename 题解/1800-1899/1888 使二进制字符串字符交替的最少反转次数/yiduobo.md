---
title: "1888. 使二进制字符串字符交替的最少反转次数"
aliases: ["yiduobo的每日leetcode 1888.使二进制字符串字符交替的最少反转次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/一-定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/478444868"
zhihu_id: "478444868"
zhihu_title: "yiduobo的每日leetcode 1888.使二进制字符串字符交替的最少反转次数"
question_id: "1888"
question: "使二进制字符串字符交替的最少反转次数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-flips-to-make-the-binary-string-alternating/"
difficulty: "Medium"
rating: 2006
created: "2022-03-09T23:31:02+08:00"
updated: "2022-03-09T23:31:02+08:00"
upvotes: 1
comments: 0
---

# 1888. 使二进制字符串字符交替的最少反转次数

> **[yiduobo的每日leetcode 1888.使二进制字符串字符交替的最少反转次数](https://zhuanlan.zhihu.com/p/478444868) · 知乎 · 2022-03-09 · 赞同 1**
> 力扣：[1888. 使二进制字符串字符交替的最少反转次数](https://leetcode.cn/problems/minimum-number-of-flips-to-make-the-binary-string-alternating/) · Medium · 灵茶山艾府：[s + s 上的滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1888.使二进制字符串字符交替的最少反转次数

[力扣](https://leetcode-cn.com/problems/minimum-number-of-flips-to-make-the-binary-string-alternating/)

题目中有循环位移和反转两种操作，首先可以明确的是，两种操作交替进行是没有意义的，完全可以先循环位移到最终的位置，然后再执行反转，此时消耗的反转次数与交替执行是一样的。

注意到循环位移是没有代价的，那么完全可以先尝试每种循环位移，然后分别判断当前情况通过反转得到交替字符串的最少反转次数。需要注意的是，循环位移会改变0和1的分布状况。不妨设odd_one和even_one分别表示奇数位上1的个数以及偶数位上1的个数。之所以只记录这两个值，是因为通过这两个值与字符串的长度n可以计算出奇数位上0的个数以及偶数位上0的个数。

当进行循环位移时：

1、若字符串长度为偶数，那么就相当于对字符串进行了奇偶互换，此时直接交换odd_one和even_one即可

2、若字符串长度为奇数，则可以认为是第1到第n - 1位上的数进行了奇偶互换，同时第0位上的数移动到第n - 1位后奇偶性保持不变，那么

2-1）若第0位上的值为1，说明第1到第n - 1位上的数中有even_one - 1个偶数位上的1以及odd_one个奇数位上的1，二者需要互换，同时第0位上的1依然需要计算到偶数位上的1中，因此最终奇数位上的1就是even_one - 1个，而偶数位上的1则变为odd_one + 1个

2-2）若第0位上的值为0，那么这个数不会影响到1的分布状况，因此此时与字符串长度为偶数的情况一样，直接交换odd_one和even_one即可

根据上面的结论，就可以根据之前的odd_one和even_one在O(1)的时间内知道当前的odd_one以及even_one。接下来需要想办法将当前字符串变为01交替的字符串。目标字符串有两种，即1010开头的以及0101开头的。

首先考察1010开头的。对于这种情况，需要偶数位上的0以及奇数位上的1进行反转。对于偶数位上的0，由于字符串的长度为n，那么有(n + 1) / 2个数位是偶数位，这里需要加1的原因是对于长度为奇数的字符串，偶数位比奇数位多出一位。又由于此时偶数位上的even_one个1，因此偶数位上0的个数就是(n + 1) / 2 - even_one。另一方面，奇数位上1的个数就是odd_one。综合起来，一共需要反转的次数就是(n + 1) / 2 - even_one + odd_one。

接下来考察0101开头的。对于这种情况，需要偶数位上的1以及奇数位上的0进行反转。其中偶数位上的1的个数就是even_one，而对于奇数位上的0而言，由于字符串的长度为n，那么有n / 2个数位是奇数位，其中又有odd_one个1，因此奇数位上0的个数就是n / 2 - odd_one。综合起来，一共需要反转的次数就是even_one + n / 2 - odd_one。

综合起来，此时需要的操作次数就是min((n + 1) / 2 - even_one + odd_one, even_one + n / 2 - odd_one)

对于每种交替位移后的情况计算上面这个值，其中最小的就是最终答案。

具体实现时，我没有统计odd_one，而是统计了1的总数tot_one以及even_one，然后通过tot_one - even_one来计算出odd_one。

最后附上python代码：

```python
class Solution(object):
    def minFlips(self, s):
        """
        :type s: str
        :rtype: int
        """

        odd_one = 0
        even_one = 0
        n = len(s)
        for index, char in enumerate(s):
            if char == '1':
                if index % 2 == 0:
                    even_one += 1
                else:
                    odd_one += 1

        res = min((n + 1) / 2 - even_one + odd_one, even_one + n / 2 - odd_one)

        for index in range(n - 1):
            odd_one, even_one = even_one, odd_one
            if s[index] == '1' and n & 1:
                odd_one -= 1
                even_one += 1
            
            res = min(res, (n + 1) / 2 - even_one + odd_one, even_one + n / 2 - odd_one)
        
        return res
```
