---
title: "2111. 使数组K递增的最少操作次数"
aliases: ["yiduobo的每日leetcode 2111.使数组K递增的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-search", "leetcode/dynamic-programming", "leetcode/dp", "题单/动态规划", "题单/动态规划/四-经典线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/523727990"
zhihu_id: "523727990"
zhihu_title: "yiduobo的每日leetcode 2111.使数组K递增的最少操作次数"
question_id: "2111"
question: "使数组 K 递增的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-the-array-k-increasing/"
difficulty: "Hard"
rating: 1941
created: "2022-06-02T21:11:05+08:00"
updated: "2022-06-02T21:11:05+08:00"
upvotes: 0
comments: 0
---

# 2111. 使数组K递增的最少操作次数

> **[yiduobo的每日leetcode 2111.使数组K递增的最少操作次数](https://zhuanlan.zhihu.com/p/523727990) · 知乎 · 2022-06-02 · 赞同 0**
> 力扣：[2111. 使数组 K 递增的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-make-the-array-k-increasing/) · Hard · 灵茶山艾府：[最长不降子序列，附进阶问题](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2111.使数组K递增的最少操作次数

[力扣](https://leetcode.cn/problems/minimum-operations-to-make-the-array-k-increasing/)

首先，不同K递增数组之间是互不影响的，因此可以先按间隔K将数组拆开得到若干个子序列，然后对每个子序列分别操作。

接下来对于单个子序列，需要将其变成递增的子序列。由于题目中的递增比较宽松，包含了等于的情况，那么就可以先找出子序列中的最长上升子序列，这些数保持不变，然后将其他剩下的数修改到满足递增。最长上升子序列这个经典的问题则可以通过贪心法在O(nlogn)的时间内求解。

最后附上python代码：

```python
class Solution(object):
    def kIncreasing(self, arr, k):
        """
        :type arr: List[int]
        :type k: int
        :rtype: int
        """

        res = 0
        for start in range(k):
            f = [arr[start]]
            for index in range(start + k, len(arr), k):
                if arr[index] >= f[-1]:
                    f.append(arr[index])
                else:
                    l = 0
                    r = len(f) - 1
                    while l < r:
                        mid = (l + r) >> 1
                        if arr[index] >= f[mid]:
                            l = mid + 1
                        else:
                            r = mid
                    f[l] = arr[index]
                    res += 1

        return res
```
