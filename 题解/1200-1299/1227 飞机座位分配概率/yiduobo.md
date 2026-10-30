---
title: "1227. 飞机座位分配概率"
aliases: ["yiduobo的每日leetcode 1227.飞机座位分配概率"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser", "leetcode/dynamic-programming", "leetcode/probability-and-statistics", "题单/数学算法", "题单/数学算法/三-概率期望"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/384045737"
zhihu_id: "384045737"
zhihu_title: "yiduobo的每日leetcode 1227.飞机座位分配概率"
question_id: "1227"
question: "飞机座位分配概率"
problem_url: "https://leetcode.cn/problems/airplane-seat-assignment-probability/"
difficulty: "Medium"
created: "2021-06-25T21:47:05+08:00"
updated: "2021-06-25T21:47:05+08:00"
upvotes: 1
comments: 0
---

# 1227. 飞机座位分配概率

> **[yiduobo的每日leetcode 1227.飞机座位分配概率](https://zhuanlan.zhihu.com/p/384045737) · 知乎 · 2021-06-25 · 赞同 1**
> 力扣：[1227. 飞机座位分配概率](https://leetcode.cn/problems/airplane-seat-assignment-probability/) · Medium · 灵茶山艾府：[【图解】没想明白？一张图秒懂！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1227.飞机座位分配概率

[力扣](https://leetcode-cn.com/problems/airplane-seat-assignment-probability/)

很有意思的问题，体现了递归的思想。不妨设f[n]表示有n个人时，第n个人坐到自己位子上的概率，那么对于n\=1的情况，答案就是1。当n大于1时，则有两种可能：

1、第1个人坐到了自己的位子上，那么此时的答案就是1。

2、第1个人坐到了别人的位子上，不妨设这个人坐到了第k个人的座位上，那么第2到第k - 1个人都能坐到自己的位子上，而第k个人的行动模式将会变成和第1个人一样。此时剩下了n - k个人，也就是说此时的概率为f[n - k]。

综合起来，就有

f[n] \= 1 / n + 1 / n \* f[n - 1] + 1 / n \* f[n - 2] + ... + 1 / n \* f[1]

变形后就有

n \* f[n] \= 1 + f[n - 1] + f[n - 2] + ... + f[1]

进一步，有

(n + 1) \* f[n + 1] \= 1 + f[n] + f[n - 1] + ... + f[1]

两式相减就有

(n + 1) \* f[n + 1] - n \* f[n] \= f[n]

于是最终可知

(n + 1) \* f[n + 1] \= (n + 1) \* f[n]

也就是

f[n + 1] \= f[n]

由于f[2] \= 0.5，因此对于所有的n >\= 2，都有f[n] \= 0.5

最后附上python代码：

```python
class Solution(object):
    def nthPersonGetsNthSeat(self, n):
        """
        :type n: int
        :rtype: float
        """

        if n == 1:
            return 1.0
        
        return 0.5
```
