---
title: "1997. 访问完所有房间的第一天"
aliases: ["yiduobo的每日leetcode 1997.访问完所有房间的第一天"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/prefix-sum", "题单/动态规划", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/501418717"
zhihu_id: "501418717"
zhihu_title: "yiduobo的每日leetcode 1997.访问完所有房间的第一天"
question_id: "1997"
question: "访问完所有房间的第一天"
problem_url: "https://leetcode.cn/problems/first-day-where-you-have-been-in-all-the-rooms/"
difficulty: "Medium"
rating: 2260
created: "2022-04-19T21:33:17+08:00"
updated: "2022-04-19T21:33:18+08:00"
upvotes: 0
comments: 0
---

# 1997. 访问完所有房间的第一天

> **[yiduobo的每日leetcode 1997.访问完所有房间的第一天](https://zhuanlan.zhihu.com/p/501418717) · 知乎 · 2022-04-19 · 赞同 0**
> 力扣：[1997. 访问完所有房间的第一天](https://leetcode.cn/problems/first-day-where-you-have-been-in-all-the-rooms/) · Medium · 灵茶山艾府：[前缀和优化 DP（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1997.访问完所有房间的第一天

[力扣](https://leetcode-cn.com/problems/first-day-where-you-have-been-in-all-the-rooms/)

直接推导规律比较复杂，数组下标倒来倒去的太麻烦了，不妨直接把较小的情况打印出来看看。

可以明确的是，最后一个房间指向的nextVisit是没有意义的，只需要观察前面的数值分布。

由于题目的要求，nextVisit[0]必然等于0，因此所有的序列都是以[0, 0]开头的。

接下来考察[0, 0, X]和[0, 1, X]。对于[0, 0, X]，可以观察样例2，为[0, 0, 1, 0, 0 1, 2]，而对于[0, 1, X]，则可以观察样例3，为[0, 0, 1, 1, 2]。

对于[0, 0, X]和[0, 1, X]的差别，可以认为是在[0, 0, 1, 1, 2]的两个1中间插入一段[0, 0]。简单的猜想是由于nextVisit[1] \= 0，所以在两个1之间插入一段[0]对应的序列[0, 0]。

当然，这上面也只是一个猜想，最稳健的方法还是应该给出详细的证明。我在这里选择的是对于模拟n较小的情况然后验证，发现确实符合上面的规律。

令f[i]表示访问第i个房间所需的最小步数，那么对于f[i]，有

f\[i\] \= f\[i - 1\] + f\[i - 1\] - f\[nextVisit\[i - 1\]\] + 2

这里的简单理解是先走了f\[i - 1\]来到了i - 1，然后会跳到nextVisit\[i - 1\]。接下来从nextVisit\[i - 1\]再走到i - 1，可以拆分成0走到nextVisit\[i - 1\]以及nextVisit\[i - 1\]走到i - 1这两段，也就是f\[i - 1\] - f\[nextVist\[i - 1\]\]。最后的2则是两次来到i - 1这个位置计数。

最后附上python代码：

```python
class Solution(object):
    def firstDayBeenInAllRooms(self, nextVisit):
        """
        :type nextVisit: List[int]
        :rtype: int
        """

        f = [1, 3]
        n = len(nextVisit)
        mod = 10 ** 9 + 7
        for index in range(2, n):
            f.append((f[index - 1] + f[index - 1] - f[nextVisit[index - 1]] + 2) % mod)
        
        res = f[-1] - 1
        if res < 0:
            res += mod
        return res
```
