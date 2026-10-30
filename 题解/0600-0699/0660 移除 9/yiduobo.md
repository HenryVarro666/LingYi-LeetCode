---
title: "660. 移除9"
aliases: ["yiduobo的每日leetcode 660.移除9"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/603545266"
zhihu_id: "603545266"
zhihu_title: "yiduobo的每日leetcode 660.移除9"
question_id: "660"
question: "移除 9"
problem_url: "https://leetcode.cn/problems/remove-9/"
difficulty: "Hard"
created: "2023-02-04T23:46:02+08:00"
updated: "2023-02-04T23:46:13+08:00"
upvotes: 0
comments: 0
---

# 660. 移除9

> **[yiduobo的每日leetcode 660.移除9](https://zhuanlan.zhihu.com/p/603545266) · 知乎 · 2023-02-04 · 赞同 0**
> 力扣：[660. 移除 9](https://leetcode.cn/problems/remove-9/) · Hard · 灵茶山艾府：[Go 九进制 递归](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

660.移除9

[力扣](https://leetcode.cn/problems/remove-9/)

题目乍一看是数位动态规划的问题，不过也可以尝试用组合数学去解决。

对于一个m位数，设其中有k位为9，那么这些9的分布就有C(m, k)种可能，而其他的(m - k)个数位上则可以自由选取0到8这一共9个数字，因此在1到10^m之间，有k个数位上有9的数字的数量为C(m, k) \* (9^(m - k))，其中k的取值范围是1 \<\= k \<\= m。

更进一步的，在1到10^m之间一共有

C(m, 1) \* (9^(m - 1)) + C(m, 2) \* (9^(m - 2)) + ... + C(m, m) \* (9^0)

上面这个式子非常眼熟，如果补充一项C(m, 0) \* 9^m，那么通过二项式定理就可以将上面的式子写成

C(m, 1) \* (9^(m - 1)) + C(m, 2) \* (9^(m - 2)) + ... + C(m, m) \* (9^0) \=

\- C(m, 0) \* 9^m + C(m, 0) \* 9^m + C(m, 1) \* (9^(m - 1)) + C(m, 2) \* (9^(m - 2)) + ... + C(m, m) \* (9^0) \=

(1 + 9)^m - C(m, 0) \* 9^m \= 10^m - 9^m

也就是说，在1到10^m之间某一位为9的数字一共是10^m - 9^m，而合法数字的个数恰好是9^m个。

从这个结论出发思考，可以发现这并不是巧合，因为换一个角度来看，本题给出的数字序列实际上就是9进制下的数字序列。因此对于本题，实际上就是问数字n在9进制下的表示，于是直接对n进行进制转换就可以得到最终结果了，并不需要使用上面提到的动态规划或者组合数学。

最后附上python代码：

```python
class Solution(object):
    def newInteger(self, n):
        """
        :type n: int
        :rtype: int
        """

        digits = []
        while n:
            digits.append(n % 9)
            n /= 9
        
        res = 0
        for digit in digits[::-1]:
            res = res * 10 + digit
        return res
```
