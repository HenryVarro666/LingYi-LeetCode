---
title: "1016. 子串能表示从1到N数字的二进制串"
aliases: ["yiduobo的每日leetcode 1016.子串能表示从1到N数字的二进制串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/enumeration", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/一-定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/368101813"
zhihu_id: "368101813"
zhihu_title: "yiduobo的每日leetcode 1016.子串能表示从1到N数字的二进制串"
question_id: "1016"
question: "子串能表示从 1 到 N 数字的二进制串"
problem_url: "https://leetcode.cn/problems/binary-string-with-substrings-representing-1-to-n/"
difficulty: "Medium"
created: "2021-04-26T23:58:47+08:00"
updated: "2021-04-26T23:58:47+08:00"
upvotes: 0
comments: 0
---

# 1016. 子串能表示从1到N数字的二进制串

> **[yiduobo的每日leetcode 1016.子串能表示从1到N数字的二进制串](https://zhuanlan.zhihu.com/p/368101813) · 知乎 · 2021-04-26 · 赞同 0**
> 力扣：[1016. 子串能表示从 1 到 N 数字的二进制串](https://leetcode.cn/problems/binary-string-with-substrings-representing-1-to-n/) · Medium · 灵茶山艾府：[三种算法：从暴力到优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

1016.子串能表示从1到N数字的二进制串

[力扣](https://leetcode-cn.com/problems/binary-string-with-substrings-representing-1-to-n/)

题目这里的N最大可以到10^9，看上去非常吓人，但是注意到S的长度最多就1000，那么可以进行下面的分析。我们首先可以找到k，这里的k满足

2^k \<\= N \< 2^(k + 1)

那么这里的2^(k - 1)到2^k - 1这些都是小于N的，同时这些数的二进制表示都是k位的，也就是说有2^k - 1 - 2^(k - 1) + 1 \= 2^(k - 1)个长度为k的不同二进制数。而对于S而言，其长度为k的子串总共也就length(S) - k + 1个，那么有解的必要条件是

length(S) - k + 1 >\= 2^(k - 1)

另外，对于2^k到N这一共N - 2^k + 1个数而言，它们都是k + 1位的，那么同样可以得到必要条件

length(S) - k >\= N - 2^k + 1

若这两个条件不成立，那么可以直接返回false。若这两个条件成立，那么这里的N和k必然是很小的，根据条件1可以得知这里的K必然小于等于10。

另外，对于1到2^(k - 1) - 1这些数而言，若它们加上2^(k - 1)，那么其二进制表示实际上是在最高位上新增了一位1，十进制表示则变成了2^(k - 1) + 1到2^k - 1。也就是说，若S的子串可以覆盖住2^(k - 1)到2^k - 1，那么其必然也能覆盖住1到2^(k - 1) - 1，也就是可以覆盖住1到2^k - 1了。

例如1到7，二进制表示分别为1，10，11，100，101，110，111。那么此时 加上8之后，得到的是9到15，这些数的二进制表示为1001，1010，1011，1100，1101，1110，1111。可以发现1到7分别是9到15的后缀，那么若此时s可以覆盖住8到15，那么也自然可以覆盖住1到7，也就是说此时的s可以覆盖住1到15。

有了上面的性质，我们就可以枚举出s中所有长度为k以及k + 1的子串并将其加入哈希表，然后检测2^k到N之间所有的数是否在哈希表中即可。

最后附上python代码：

```python
class Solution(object):
    def queryString(self, S, N):
        """
        :type S: str
        :type N: int
        :rtype: bool
        """

        pow2 = 1
        l = 1
        while pow2 <= N:
            pow2 += pow2
            l += 1
        
        pow2 /= 2
        l -= 1
        if max(pow2 / 2, N - pow2 + 1) > len(S) - l + 1:
            return False
        
        num_set = set()
        now = 0
        for index in range(l):
            now += now + int(S[index])

        num_set.add(now)
        for index in range(l, len(S)):
            now %= pow2
            now += now + int(S[index])
            num_set.add(now)
        
        if l > 1:
            now = 0
            for index in range(l - 1):
                now += now + int(S[index])

            num_set.add(now)
            pow2 /= 2
            for index in range(l - 1, len(S)):
                now %= pow2
                now += now + int(S[index])
                num_set.add(now)
        
        for num in range(pow2 + pow2, N + 1):
            if num not in num_set:
                return False
        
        return True
```
