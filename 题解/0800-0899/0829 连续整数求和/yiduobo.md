---
title: "829. 连续整数求和"
aliases: ["yiduobo的每日leetcode 829.连续整数求和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/344815770"
zhihu_id: "344815770"
zhihu_title: "yiduobo的每日leetcode 829.连续整数求和"
question_id: "829"
question: "连续整数求和"
problem_url: "https://leetcode.cn/problems/consecutive-numbers-sum/"
created: "2021-01-21T22:21:12+08:00"
updated: "2021-01-21T22:21:12+08:00"
upvotes: 0
comments: 0
---

# 829. 连续整数求和

> **[yiduobo的每日leetcode 829.连续整数求和](https://zhuanlan.zhihu.com/p/344815770) · 知乎 · 2021-01-21 · 赞同 0**
> 力扣：[829. 连续整数求和](https://leetcode.cn/problems/consecutive-numbers-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

829.连续整数求和

[力扣](https://leetcode-cn.com/problems/consecutive-numbers-sum/)

首先，根据求和公式，设这些连续整数最小的为p，一共有k个，那么就有

p + (p + 1) + ... + (p + k - 1) \= (p \* 2 + k - 1) \* k \= n \* 2

于是可以逐个枚举k，若n \* 2模k等于0，那么设tmp \= n \* 2 / k，即

p \* 2 + k - 1 \= n \* 2 / k

解得

p \* 2 \= n \* 2 / k - k + 1

此时需要判断式子右边的部分是否为偶数，同时由于所有数都应该是正整数，因此p也需要大于0。若都满足，那么就可以解得一个合法的p。

注意到n \* 2 \= (p \* 2 + k - 1) \* k >\= (k + 1) \* k，因此k枚举的上限就是sqrt(n \* 2)。同时注意到随着k的增大，p是逐渐减小的，那么一旦对于当前的k解得p小于0，那么就无须枚举后续的k了。

最后附上python代码：

```python
class Solution(object):
    def consecutiveNumbersSum(self, N):
        """
        :type N: int
        :rtype: int
        """

        N += N
        k = 1
        res = 0
        while k * k <= N:
            if N % k == 0:
                tmp = N / k
                if (tmp - k + 1) % 2 == 0:
                    p = (tmp - k + 1) / 2
                    if p > 0:
                        res += 1
                    else:
                        return res
            
            k += 1
        
        return res
```
