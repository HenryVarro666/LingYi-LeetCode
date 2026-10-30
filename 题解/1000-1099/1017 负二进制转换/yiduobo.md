---
title: "1017. 负二进制转换"
aliases: ["yiduobo的每日leetcode 1017.负二进制转换"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/368104812"
zhihu_id: "368104812"
zhihu_title: "yiduobo的每日leetcode 1017.负二进制转换"
question_id: "1017"
question: "负二进制转换"
problem_url: "https://leetcode.cn/problems/convert-to-base-2/"
created: "2021-04-27T00:19:38+08:00"
updated: "2021-04-27T00:19:38+08:00"
upvotes: 0
comments: 0
---

# 1017. 负二进制转换

> **[yiduobo的每日leetcode 1017.负二进制转换](https://zhuanlan.zhihu.com/p/368104812) · 知乎 · 2021-04-27 · 赞同 0**
> 力扣：[1017. 负二进制转换](https://leetcode.cn/problems/convert-to-base-2/)

传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

1017.负二进制转换

[力扣](https://leetcode-cn.com/problems/convert-to-base-2/)

对于(-2)^k而言，若k为偶数，那么与2^k是一样的；若k为奇数，那么最后会等于-2^k。

若此时有2^k需要转换成-2进制，那么当k为偶数时，其表示与2进制相同；若k为奇数时，就有2^k \= 2^(k + 1) - 2^k \= 2^(k + 1) + (-2^k) \= (-2)^(k + 1) + (-2)^k，也就是说其负二进制表示下应该是基于2进制再添加一个k + 1位的1。

例如样例1中的2^1，其需要表示为2^2 - 2^1 \= (-2)^2 + (-2)^1 \= 110(base -2)

而对于样例3中的2^2，其直接可以表示为2^2 \= (-2)^2 \= 100(base -2)

于是我们可以先将N转化为2进制，然后根据从低到高一趟扫描，根据当前位置的值以及奇偶性来进行转换。但是需要注意的是，这里的转换时可能产生进位的。例如对于N \= 6的情况，有6 \= 2^2 + 2^1 \= 2^2 + (2^2 - 2^1) \= (-2)^2 + (-2)^2 + (-2)^1

此时有两个(-2)^2，产生了进位。

那么一个直观的想法是

(-2)^k + (-2)^k \= 2 \* (-2)^k \= -1 \* -2 \* (-2)^k \= -(-2)^(k + 1)

也就是说若此时存在(-2)^(k + 1)，其将被这两个(-2)^k给抵消掉；若不存在，那么则可以如法炮制，通过

(-2)^(k + 1) + (-2)^(k + 1) \= -(-2)^(k + 2)

变形后可得-(-2)^(k + 1) \= (-2)^(k + 2) + (-2)^(k + 1)，也就是将第k + 1位置为1，同时第k + 2位再次产生了进位

还是以N \= 6的情况来说明。此前得到6 \= (-2)^2 + (-2)^2 + (-2)^1，由于此时不存在(-2)^3，因此此时需要将其变形为

6 \= (-2)^2 + (-2)^2 + (-2)^1

\= -(-2)^3 + (-2)^1

\= (-2)^4 + (-2)^3 + (-2)^1

\= 11010(base - 2)

最后附上python代码：

```python
class Solution(object):
    def baseNeg2(self, N):
        """
        :type N: int
        :rtype: str
        """

        if N == 0:
            return "0"

        x = N
        origin = []
        while x:
            origin.append(x % 2)
            x /= 2
        
        p = 0
        res = []
        for index, num in enumerate(origin):
            if index < len(res):
                res[index] += num
            else:
                res.append(num)

            if index % 2 == 1 and num == 1:
                if index + 1 < len(res):
                    res[index + 1] += num
                else:
                    res.append(num)

        p = 0
        while p < len(res):
            if res[p] > 1:
                if p + 1 < len(res) and res[p + 1] > 0:
                    res[p + 1] -= 1
                else:
                    if p + 1 < len(res):
                        res[p + 1] += 1
                    else:
                        res.append(1)
                    if p + 2 < len(res):
                        res[p + 2] += 1
                    else:
                        res.append(1)
                res[p] -= 2
            p += 1

        res.reverse()
        return ''.join(str(x) for x in res)
```
