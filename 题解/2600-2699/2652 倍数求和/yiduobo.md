---
title: "2652. 倍数求和"
aliases: ["yiduobo的每日leetcode 2652.倍数求和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "题单/数学算法", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/647406451"
zhihu_id: "647406451"
zhihu_title: "yiduobo的每日leetcode 2652.倍数求和"
question_id: "2652"
question: "倍数求和"
problem_url: "https://leetcode.cn/problems/sum-multiples/"
difficulty: "Easy"
created: "2023-08-02T03:30:14+08:00"
updated: "2023-08-02T03:30:14+08:00"
upvotes: 0
comments: 0
---

# 2652. 倍数求和

> **[yiduobo的每日leetcode 2652.倍数求和](https://zhuanlan.zhihu.com/p/647406451) · 知乎 · 2023-08-02 · 赞同 0**
> 力扣：[2652. 倍数求和](https://leetcode.cn/problems/sum-multiples/) · Easy · 灵茶山艾府：[数学做法：O(1) 容斥原理（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2652.倍数求和

[力扣](https://leetcode.cn/problems/sum-multiples/)

题目的数据规模很小，直接暴力求解完全是可行，不过在这里使用容斥原理是更好的做法。

首先，对于一个大于0的数x，大小在1到n之间，且为x倍数的最小值自然是x，而最大值则可以先计算n整除x的结果cnt，然后使用cnt \* x得到x倍数的最大值。那么所有x的倍数求和就是

x + 2x + 3x + ... + cnt \* x \= (1 + cnt) \* cnt / 2 \* x

根据这个结论，就可以在O(1)的时间内计算出1到n之间所有是x倍数的数之和了。那么对于本题，则可以先将3、5、7的倍数之和分别计算出来然后累加。不过在这里有一个问题就是，某些数可能同时是3、5、7中的两个数或者三个数的倍数，例如15、21、35等等。

那么对于同时是3和5的倍数，即15的倍数的数，这些数的和在计算3的倍数之和以及5的倍数之和时都会被计算进行，也就是说多计算了一次。同样的，对于21的倍数以及35的倍数都被计算了两次，因此在这里需要将15、21、35的倍数之和都减去一次。

不过在这里又出现了新的问题。对于同时是3、5、7倍数，也就是105的倍数的数，其在计算3、5、7的倍数之和时各被计算了一次，而在减去15、21、35的倍数之和时又各被减去了一次，因此在这里已经没有105的倍数之和了，因此最后还需要额外加上一个105的倍数之和。

最后附上python代码：

```python
class Solution(object):
    def sumOfMultiples(self, n):
        """
        :type n: int
        :rtype: int
        """

        def calc(x):
            cnt = n / x
            return (1 + cnt) * cnt / 2 * x
        
        return calc(3) + calc(5) + calc(7) - calc(15) - calc(21) - calc(35) + calc(105)
```
