---
title: "2448. 使数组相等的最小开销"
aliases: ["yiduobo的每日leetcode 2448.使数组相等的最小开销"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/sorting", "leetcode/zhong-wei-shu", "题单/贪心算法", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/584986960"
zhihu_id: "584986960"
zhihu_title: "yiduobo的每日leetcode 2448.使数组相等的最小开销"
question_id: "2448"
question: "使数组相等的最小开销"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-make-array-equal/"
difficulty: "Hard"
rating: 2005
created: "2022-11-19T23:05:34+08:00"
updated: "2022-11-19T23:05:34+08:00"
upvotes: 1
comments: 0
---

# 2448. 使数组相等的最小开销

> **[yiduobo的每日leetcode 2448.使数组相等的最小开销](https://zhuanlan.zhihu.com/p/584986960) · 知乎 · 2022-11-19 · 赞同 1**
> 力扣：[2448. 使数组相等的最小开销](https://leetcode.cn/problems/minimum-cost-to-make-array-equal/) · Hard · 灵茶山艾府：[两种做法：枚举+考虑变化量 / 中位数贪心](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2448.使数组相等的最小开销

[力扣](https://leetcode.cn/problems/minimum-cost-to-make-array-equal/)

不妨设当数组中的数都变为x时的总开销最小，那么此时的总开销就是

c \= abs(x - nums[0]) \* cost[0] + abs(x - nums[1]) \* cost[1] + ... + abs(x - nums[n - 1]) \* cost[n - 1]

这是若干个绝对值函数的叠加，也就是说这必然是个开口向上的凸函数。更进一步的，可以明确最终的x必然就等于nums中的某一个数。简单的证明如下：

在这里不妨将nums和cost组合起来，按照nums的大小从小到大进行排序。记排序后的nums为数组b，cost为数组k，那么就有

c \= abs(x - b[0]) \* k[0] + abs(x - b[0]) \* b[1] + ... + abs(x - b[n - 1]) \* k[n - 1]

其中b[0] \<\= b[1] \<\= ... \<\= b[n - 1]，那么：

1、当x \<\= b[0]时：

c \= b[0] \* k[0] + b[1] \* k[1] + ... b[n - 1] \* k[n - 1] - (k[0] + k[1] + ... + k[n - 1]) \* x

为了使得c最小，显然应该让x取最大值，此时x取b[0]是最优的

2、当b[i] \<\= x \<\= b[i + 1]时：

c \= (k[0] + k[1] + ... + k[i] - k[i + 1] - k[i + 2] - ... - k[n - 1]) \* x + (b[i + 1] \* k[i + 1] + b[i + 2] \* k[i +2] + ... + b[n - 1] \* k[n - 1] - b[0] \* k[0] - b[1] \* k[1] - ... - b[i] \* k[i])

这是一个典型的一次函数的式子，因此其极值点要么在x \= b[i]，要么在x \= b[i + 1]

3、当b[n - 1] \<\= x时：

此时情况与情况1类似，当x取b[n - 1]时c最小

综合起来，就说明了最终的x必然与nums中的某个数相同。

有了这个结论，就可以从小到大枚举b中的每个数作为x的取值，然后计算此时的c并更新答案。根据上面情况2中的式子，可以发现最终c的计算可以分解成k、k \* b的前缀和以及后缀和之间的操作，那么在这里就可以先计算出k的总和以及k \* b的总和，然后在遍历过程中计算k、k \* b的前缀和，然后利用总和计算出对应的后缀和，再带入上面的式子计算出对应的c。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, nums, cost):
        """
        :type nums: List[int]
        :type cost: List[int]
        :rtype: int
        """

        sorted_info = sorted(zip(nums, cost))
        suf_k = suf_b = 0
        for b, k in sorted_info:
            suf_k += k
            suf_b += b * k
        
        res = None

        pre_b = pre_k = 0
        for b, k in sorted_info:
            suf_k -= k
            suf_b -= b * k
            now = suf_b - suf_k * b + pre_k * b - pre_b
            if res is None or res > now:
                res = now

            pre_k += k
            pre_b += b * k

        return res
```
