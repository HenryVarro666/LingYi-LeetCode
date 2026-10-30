---
title: "2607. 使子数组元素和相等"
aliases: ["yiduobo的每日leetcode 2607.使子数组元素和相等"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/math", "leetcode/number-theory", "leetcode/zhong-wei-shu", "题单/数学算法", "题单/贪心算法", "题单/数学算法/一-数论", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/645157262"
zhihu_id: "645157262"
zhihu_title: "yiduobo的每日leetcode 2607.使子数组元素和相等"
question_id: "2607"
question: "使子数组元素和相等"
problem_url: "https://leetcode.cn/problems/make-k-subarray-sums-equal/"
difficulty: "Medium"
rating: 2071
created: "2023-07-22T04:42:33+08:00"
updated: "2023-07-22T04:42:33+08:00"
upvotes: 0
comments: 0
---

# 2607. 使子数组元素和相等

> **[yiduobo的每日leetcode 2607.使子数组元素和相等](https://zhuanlan.zhihu.com/p/645157262) · 知乎 · 2023-07-22 · 赞同 0**
> 力扣：[2607. 使子数组元素和相等](https://leetcode.cn/problems/make-k-subarray-sums-equal/) · Medium · 灵茶山艾府：[【转换】中位数贪心+裴蜀定理（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2607.使子数组元素和相等

[力扣](https://leetcode.cn/problems/make-k-subarray-sums-equal/)

题目要求最终子数组中每个长度为k的子数组之和都相等，那么首先可以明确的是对于原字符串中处于下标i以及下标i + k的数必须要完全相同，因为从i到i + k - 1这一段长度为k的子数组之和需要与i + 1到k这一段长度为k的子数组之和相等，那么去掉中间公共的i + 1到i + k - 1这一段后，剩下的两端，也就是下标i和下标i + k的这两个数也同样必须相等。

另一方面，由于题目中的数组是一个循环数组，那么可能出现i + ak \= j + bn的情况，其中n为数组的长度。在这种情况下，处于下标i和下标j的数也需要完全相同。可以发现，最初始的结论可以理解成下面这个式子中a等于1，b等于0的特殊情况，那么接下来就只需要对i + ak \= j + bn这个式子进行讨论。

不妨将式子变形，得到j - i \= ak - bn，可以发现这里的j - i实际上就可以理解成数组中下标对之间的距离，而后面的ak - bn，则可以变形成为(ap - bq)g，其中g为k和n的最大公约数，a \= pg，n \= qg。由于p和q互质，那么ap - bg在选择合适的a和b时可以得到任意整数，也就表明了这里的i和j只要满足下标之差为g的倍数，那么这两个下标上的数就必须相等。

到了这里，就可以将所有数按照下标模g的余数进行分组，其中同一组中的数必须完全相同，不同组之间的数互不影响。接下来的问题就变成了给出若干个数组，要求对于其中的每一个数组，都需要通过最少次数的加1或者减1操作，将该数组中的所有数变成同一个数。这是一个经典的贪心问题，对于每个数组只需取当前数组的中位数作为变化的目标就能使得操作次数最少。于是只需对每个数组分别排序，然后分别遍历每个数组，计算当前值与其所在数组中位数之差并累加到最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def makeSubKSumEqual(self, arr, k):
        """
        :type arr: List[int]
        :type k: int
        :rtype: int
        """

        n = len(arr)
        x, y = n, k
        while y:
            x, y = y, x % y
        
        g = x

        num_list = [[] for _ in range(g)]
        for index, v in enumerate(arr):
            num_list[index % g].append(v)
        
        res = 0
        for r in range(g):
            num_list[r].sort()
            mid = num_list[r][len(num_list[r]) / 2]
            for v in num_list[r]:
                if v < mid:
                    res += mid - v
                else:
                    res += v - mid
        
        return res
```
