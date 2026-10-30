---
title: "651. 4键键盘"
aliases: ["yiduobo的每日leetcode 651.4键键盘"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/603345997"
zhihu_id: "603345997"
zhihu_title: "yiduobo的每日leetcode 651.4键键盘"
question_id: "651"
question: "4键键盘"
problem_url: "https://leetcode.cn/problems/4-keys-keyboard/"
created: "2023-02-04T03:58:06+08:00"
updated: "2023-02-04T03:58:06+08:00"
upvotes: 0
comments: 0
---

# 651. 4键键盘

> **[yiduobo的每日leetcode 651.4键键盘](https://zhuanlan.zhihu.com/p/603345997) · 知乎 · 2023-02-04 · 赞同 0**
> 力扣：[651. 4键键盘](https://leetcode.cn/problems/4-keys-keyboard/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

651.4键键盘

[力扣](https://leetcode.cn/problems/4-keys-keyboard/)

除了最常规的+1操作之外，题目还有一套全选-复制-粘贴操作可以使用。

可以发现，这里相当于3次操作实现了乘以2，但是在此基础上可以继续执行粘贴操作，也就是4次操作乘以3、5次操作乘以4、6次操作乘以5等。但是需要注意的是，继续往后的7次操作乘以6是不划算的，因为对于下面两个执行序列，都是7次操作乘以6，但是后者的剪贴板比前者更优秀

全选-复制-粘贴-粘贴-粘贴-粘贴-粘贴

全选-复制-粘贴-全选-复制-粘贴-粘贴

另一方面，+1操作必然出现在乘法操作之前，因为先加后乘的话加的部分可以得到通过后续的乘法来放大，也就是说+1操作只会集中在最初的几次操作中。根据上面乘法的推论，实际上也可以套用到加法中，也就是当操作次数小于等于6时，全部执行加法是最优的，否则就应该选择上面的3次乘以2、4次乘以3、5次乘以4以及6次乘以5中的某一种，于是就有

当1 \<\= i \<\= 6时，有f[i] \= i

当i > 6时，有f[i] \= max(f[i - 3] \* 2, f[i - 4] \* 3, f[i - 5] \* 4, f[i - 6] \* 5)

根据上面的式子递推计算得到f[n]即可。

最后附上python代码：

```python
class Solution(object):
    def maxA(self, n):
        """
        :type n: int
        :rtype: int
        """

        if n <= 6:
            return n
        else:
            a, b, c, d, e, f = 1, 2, 3, 4, 5, 6
            for index in range(7, n + 1):
                a, b, c, d, e, f = b, c, d, e, f, max(d * 2, c * 3, b * 4, a * 5)
            
            return f
```
