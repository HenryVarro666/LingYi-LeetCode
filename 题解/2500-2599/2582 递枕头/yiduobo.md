---
title: "2582. 递枕头"
aliases: ["yiduobo的每日leetcode 2582.递枕头"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/642510704"
zhihu_id: "642510704"
zhihu_title: "yiduobo的每日leetcode 2582.递枕头"
question_id: "2582"
question: "递枕头"
problem_url: "https://leetcode.cn/problems/pass-the-pillow/"
difficulty: "Easy"
created: "2023-07-10T03:07:52+08:00"
updated: "2023-07-10T03:07:52+08:00"
upvotes: 0
comments: 0
---

# 2582. 递枕头

> **[yiduobo的每日leetcode 2582.递枕头](https://zhuanlan.zhihu.com/p/642510704) · 知乎 · 2023-07-10 · 赞同 0**
> 力扣：[2582. 递枕头](https://leetcode.cn/problems/pass-the-pillow/) · Easy · 灵茶山艾府：[O(1) 公式（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2582.递枕头

[力扣](https://leetcode.cn/problems/pass-the-pillow/)

找规律的题目。通过样例可以发现，每次枕头需要经过2 \* (n - 1)轮才会重新回到1的手中，于是可以将time对这个值取模。接下来对于取模后的time，若其位于前半区，也就是time \< n - 1时，会按照正序传递，此时对应的答案就是time + 1，反之当time位于后半区时，会按逆序传递，此时对应的答案就是2 \* n - 1 - time。

最后附上python代码：

```python
class Solution(object):
    def passThePillow(self, n, time):
        """
        :type n: int
        :type time: int
        :rtype: int
        """

        time %= (n - 1) * 2
        if time < n - 1:
            return time + 1
        else:
            return n * 2 - 1 - time
```
