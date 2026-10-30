---
title: "625. 最小因式分解"
aliases: ["yiduobo的每日leetcode 625.最小因式分解"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/602415886"
zhihu_id: "602415886"
zhihu_title: "yiduobo的每日leetcode 625.最小因式分解"
question_id: "625"
question: "最小因式分解"
problem_url: "https://leetcode.cn/problems/minimum-factorization/"
created: "2023-02-01T02:15:01+08:00"
updated: "2023-02-01T02:15:01+08:00"
upvotes: 0
comments: 0
---

# 625. 最小因式分解

> **[yiduobo的每日leetcode 625.最小因式分解](https://zhuanlan.zhihu.com/p/602415886) · 知乎 · 2023-02-01 · 赞同 0**
> 力扣：[625. 最小因式分解](https://leetcode.cn/problems/minimum-factorization/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

625.最小因式分解

[力扣](https://leetcode.cn/problems/minimum-factorization/)

题目要求b的的各位数相乘可以得到a，那么也就意味着a的质因子只能有2、3、5、7。对于这四种质因子，5和7只能单独出现，而对于2和3，则应该尽量使用8、9，如果构不成8也可以使用4，这样可以使得b的位数更少，从而达到题目要求的最小。

在这里有一个需要讨论的地方就是关于6的使用，即对于多个2和多个3同时出现时，什么情况应该组合成6。一个简单的思路是每次尽量组合出较大的因子，也就是按照9、8、6、4的顺序进行组合。这样做的理由是较大的因子被组合出来后，剩下的2和3能组合出的因子就会更小，此时只需将这个较小的因子放置在前方，得到的数就必然小于使用相对平均的方法分配出来的结果。

换言之，在这里只需从9到2逆序枚举，不断将num中对应的因子分离出去直到无法分离。若最终num不等于1，说明num还存在2、3、5、7之外的质因子，此时直接返回0，否则就根据各个因子分离的结果，按2到9的顺序依次排列好。若这个数大于2^31 - 1，那么同样是返回0，否则就返回这个数。

最后附上python代码：

```python
class Solution(object):
    def smallestFactorization(self, num):
        """
        :type num: int
        :rtype: int
        """

        if num == 1:
            return 1

        digit_list = [0] * 10
        for digit in range(9, 1, -1):
            while num % digit == 0:
                digit_list[digit] += 1
                num /= digit
        
        if num != 1:
            return 0

        res = 0
        for digit in range(2, 10):
            for _ in range(digit_list[digit]):
                res = res * 10 + digit
        
        if res > 2147483647:
            return 0

        return res
```
