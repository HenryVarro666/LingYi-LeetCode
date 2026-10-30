---
title: "910. 最小差值II"
aliases: ["yiduobo的每日leetcode 910.最小差值II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/enumeration", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/354688610"
zhihu_id: "354688610"
zhihu_title: "yiduobo的每日leetcode 910.最小差值II"
question_id: "910"
question: "最小差值 II"
problem_url: "https://leetcode.cn/problems/smallest-range-ii/"
difficulty: "Medium"
rating: 2135
created: "2021-03-04T23:21:03+08:00"
updated: "2021-03-04T23:21:03+08:00"
upvotes: 0
comments: 0
---

# 910. 最小差值II

> **[yiduobo的每日leetcode 910.最小差值II](https://zhuanlan.zhihu.com/p/354688610) · 知乎 · 2021-03-04 · 赞同 0**
> 力扣：[910. 最小差值 II](https://leetcode.cn/problems/smallest-range-ii/) · Medium · 灵茶山艾府：[【图】小的变大，大的变小（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

910.最小差值II

[力扣](https://leetcode-cn.com/problems/smallest-range-ii/)

首先，若数组中的所有数都加上K或者都减去K，那么最终的差值就是max - min。

接下来分析数组中部分数加上K，其他数减去K这种情况。直观感觉上显然是小的数加上K，大的数减去K，也可以给出粗略的证明。

对于A[i]以及A[j]，不妨设A[i] \= A[j] - diff，其中diff表示二者差值且大于0。接下来考虑加减K的几种情况：

1、A[i] + K，A[j] - K：

此时有(A[j] - K) - (A[i] + K) \= A[i] + diff - K - A[i] - K \= diff - 2K，需要考察diff与2K的大小关系。

若diff > 2K，now_diff \= diff - 2K \<\= diff

若diff \= 2K，now_diff \= 0 \< diff

若diff \< 2K，now_diff \= 2K - diff，这种情况下无法判断其与diff的大小

2、A[i] + K，A[j] + K，或者A[i] - K，A[j] - K：

此时now_diff \= diff

3、A[i] - K，A[j] + K：

此时有(A[j] + K) - (A[i] - K) \= A[i] + diff + K - A[i] + K \= diff + 2K > diff

根据上面的结论，对于一组A[i]与A[j]，我们要么同时加减K，要么小的加K大的减K。根据这个结论，那么若数组中有部分数加上K，其他数减去K，那么必然是从小到大排序后的前面部分加上K，后面部分减去K，于是我们可以对A进行排序，然后枚举这个分隔点。

对于当前枚举到的A[index]，如果这里就是分隔点，那么此时A[0]到A[index]都加上了K，其中最大的为A[index] + K，而A[index + 1]到A[-1]都减去了K，其中最大的为A[-1] - K，于是数组中的最大值就是max(A[index] + K, A[-1] - K)。同理，数组中的最小值则是min(A[index + 1] - K, A[0] + K)。得到最大值和最下值之后，计算二者差值然后更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def smallestRangeII(self, A, K):
        """
        :type A: List[int]
        :type K: int
        :rtype: int
        """

        A = sorted(A)
        res = A[-1] - A[0]
        for index in range(len(A) - 1):
            res = min(res, max(A[-1] - K, A[index] + K) - min(A[0] + K, A[index + 1] - K))
        
        return res
```
