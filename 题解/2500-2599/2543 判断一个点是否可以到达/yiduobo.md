---
title: "2543. 判断一个点是否可以到达"
aliases: ["yiduobo的每日leetcode 2543.判断一个点是否可以到达"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/数学算法", "题单/贪心算法", "题单/数学算法/一-数论", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/637870102"
zhihu_id: "637870102"
zhihu_title: "yiduobo的每日leetcode 2543.判断一个点是否可以到达"
question_id: "2543"
question: "判断一个点是否可以到达"
problem_url: "https://leetcode.cn/problems/check-if-point-is-reachable/"
difficulty: "Hard"
rating: 2221
created: "2023-06-20T22:58:56+08:00"
updated: "2023-06-20T22:58:56+08:00"
upvotes: 0
comments: 0
---

# 2543. 判断一个点是否可以到达

> **[yiduobo的每日leetcode 2543.判断一个点是否可以到达](https://zhuanlan.zhihu.com/p/637870102) · 知乎 · 2023-06-20 · 赞同 0**
> 力扣：[2543. 判断一个点是否可以到达](https://leetcode.cn/problems/check-if-point-is-reachable/) · Hard · 灵茶山艾府：[问题转换+GCD+具体构造方法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2543.判断一个点是否可以到达

[力扣](https://leetcode.cn/problems/check-if-point-is-reachable/)

题目的数据规模很大，直接bfs肯定是不行，必须想办法找规律。

首先观察题目中给出的四种操作，可以发现前两种减法不会影响x和y的最大公约数，而后两种倍增操作则可能使得x和y的最大公约数也倍增。换言之，若可以到达(X, Y)，那么X和Y的最大公约数必然是2的幂次。

有了充分条件，很自然继续向下猜测这个2的幂次是否也是必要条件。

不妨反过来，从(X, Y)倒推(1, 1)。此时的四种操作就变成了(x, y + x)，(x + y, y)，(x / 2, y)，(x, y / 2)。其中后两种操作分别需要x和y是2的倍数。

可以发现，反过来的前两种操作依然不影响最大公约数，而后两种操作则可能是的最大公约数折半。于是可以不断对X和Y执行后两种操作，直到二者都为奇数为止。而当二者都为奇数时，则可以采用前两种操作，让二者中的较大值加上较小值得到新的偶数，再进行折半。这样一来，就可以保证每轮操作X和Y中有一方是在不断减小的，而二者的最大公约数则依然是2的幂次，那么在若干轮操作后，就一定可以将二者都变为1。

根据上面的结论，就只需要求解X和Y的最大公约数，判断其是否是2的幂次即可。

```python
class Solution(object):
    def isReachable(self, targetX, targetY):
        """
        :type targetX: int
        :type targetY: int
        :rtype: bool
        """

        while targetX:
            targetY, targetX = targetX, targetY % targetX
        
        return targetY & (targetY - 1) == 0
```
