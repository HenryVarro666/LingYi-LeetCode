---
title: "2143. 在两个数组的区间中选取数字"
aliases: ["yiduobo的每日leetcode 2143.在两个数组的区间中选取数字"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/626826348"
zhihu_id: "626826348"
zhihu_title: "yiduobo的每日leetcode 2143.在两个数组的区间中选取数字"
question_id: "2143"
question: "在两个数组的区间中选取数字"
problem_url: "https://leetcode.cn/problems/choose-numbers-from-two-arrays-in-range/"
created: "2023-05-05T00:27:37+08:00"
updated: "2023-05-05T00:27:37+08:00"
upvotes: 0
comments: 0
---

# 2143. 在两个数组的区间中选取数字

> **[yiduobo的每日leetcode 2143.在两个数组的区间中选取数字](https://zhuanlan.zhihu.com/p/626826348) · 知乎 · 2023-05-05 · 赞同 0**
> 力扣：[2143. 在两个数组的区间中选取数字](https://leetcode.cn/problems/choose-numbers-from-two-arrays-in-range/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2143.在两个数组的区间中选取数字

[力扣](https://leetcode.cn/problems/choose-numbers-from-two-arrays-in-range/)

首先，自然是将题目转化成从区间中选取数字，使得nums1中选取数字之和减去nums2中选取数字之和恰好等于0。另外，由于题目中数组长度不超过100，同时数值大小在-100到100之间，换言之任意选择方案的数字和之差必然在-10000到10000之间，这个数据规模可以使用动态规划来求解。

令f[i][j]表示以第i个数字为右边界的区间中，数字和之差为j的方案数，那么对于f[i][j]：

1、仅从nums1[i]或者nums2[i]中选择一个，不考虑前面的数，那么就可以初始化

f\[i\]\[nums1\[i\]\] \= 1

f\[i\]\[-nums2\[i\]\] \= 1

2、也可以考虑在f[i - 1]的基础上进行运算，因此可以所有j，要求f[i - 1][j] > 0，那么就有

f\[i\]\[j\] +\= f\[i - 1\]\[j + nums1\[i\]\]

f\[i\]\[j\] +\= f\[i - 1\]\[j - nums2\[i\]\]

计算完毕后，将每一个i对应的f[i][0]累加到答案中即可。

具体实现上，为了避免负值的下标，那么可以在累加和的基础上额外加上一个10000的offset。

最后附上python代码：

```python
class Solution(object):
    def countSubranges(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        f = [0] * 20001
        res = 0
        mod = 10 ** 9 + 7
        for v1, v2 in zip(nums1, nums2):
            g = f[:]
            f = [0] * 20001
            f[v1 + 10000] += 1
            f[-v2 + 10000] += 1
            for v, cnt in enumerate(g):
                if cnt == 0:
                    continue

                f[v + v1] += cnt
                if f[v + v1] >= mod:
                    f[v + v1] -= mod

                f[v - v2] += cnt
                if f[v - v2] >= mod:
                    f[v - v2] -= mod
            
            res += f[10000]
            if res >= mod:
                res -= mod
        
        return res
```
