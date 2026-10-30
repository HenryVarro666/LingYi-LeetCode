---
title: "1015. 可被K整除的最小整数"
aliases: ["yiduobo的每日leetcode 1015.可被K整除的最小整数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/math", "leetcode/enumeration", "leetcode/number-theory", "题单/链表-二叉树与回溯", "题单/数学算法", "题单/链表-二叉树与回溯/一-链表", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/367794295"
zhihu_id: "367794295"
zhihu_title: "yiduobo的每日leetcode 1015.可被K整除的最小整数"
question_id: "1015"
question: "可被 K 整除的最小整数"
problem_url: "https://leetcode.cn/problems/smallest-integer-divisible-by-k/"
difficulty: "Medium"
created: "2021-04-25T21:52:12+08:00"
updated: "2021-04-25T21:52:12+08:00"
upvotes: 0
comments: 0
---

# 1015. 可被K整除的最小整数

> **[yiduobo的每日leetcode 1015.可被K整除的最小整数](https://zhuanlan.zhihu.com/p/367794295) · 知乎 · 2021-04-25 · 赞同 0**
> 力扣：[1015. 可被 K 整除的最小整数](https://leetcode.cn/problems/smallest-integer-divisible-by-k/) · Medium · 灵茶山艾府：[三种算法+优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

1015.可被K整除的最小整数

[力扣](https://leetcode-cn.com/problems/smallest-integer-divisible-by-k/)

题目要求找到最小的形如11...1且模K等于0的整数。

设l位的11...1为N[l]，l - 1位的11...1为N[l - 1]，那么对于N[l]而言，其可以写成

N[l] % K \= (10^(l - 1) + N[l - 1]) % K

\= (10^(l - 1) % K + N[l - 1] % K) % K

也就是说我们只要知道了N[l - 1]以及10^(l - 1)对K取模的结果，就可以计算得到N[l]对K取模的结果。

对于10^l，又有

10^l % K \= 10^(l - 1) \* 10 % K \= (10^(l - 1) % K) \* 10 % K

也就是说10^l % K也可以通过更小规模的10^(l - 1) % K计算得到

那么接下来就只需要维护一个now表示N[l]对K取模的余数，然后再维护一个变量remain表示当前10^l对K取模的余数。

此时就只需要不断扩展l，然后计算出当前的N[l]并通过之前的10^(l - 1) % K来更新10^l % K。若N[l] % K等于0，那么当前扩展的轮次即为最终答案；若某一时刻N[l] % K在之前出现过，那么说明余数进入了一个循环，问题无解，于是返回-1。

最后附上python代码：

```python
class Solution(object):
    def smallestRepunitDivByK(self, K):
        """
        :type K: int
        :rtype: int
        """

        rem_set = set()
        remain = 1
        res = 0
        now = 0
        while True:
            res += 1
            now = (now + remain) % K
            if now == 0:
                return res
            if now in rem_set:
                break
            rem_set.add(now)
            remain = (remain * 10) % K

        return -1
```
