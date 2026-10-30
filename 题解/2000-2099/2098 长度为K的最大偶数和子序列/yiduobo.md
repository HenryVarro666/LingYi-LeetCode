---
title: "2098. 长度为K的最大偶数和子序列"
aliases: ["yiduobo的每日leetcode 2098.长度为K的最大偶数和子序列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/626225702"
zhihu_id: "626225702"
zhihu_title: "yiduobo的每日leetcode 2098.长度为K的最大偶数和子序列"
question_id: "2098"
question: "长度为K的最大偶数和子序列"
problem_url: "https://leetcode.cn/problems/subsequence-of-size-k-with-the-largest-even-sum/"
created: "2023-05-02T04:54:07+08:00"
updated: "2023-05-02T04:54:07+08:00"
upvotes: 0
comments: 0
---

# 2098. 长度为K的最大偶数和子序列

> **[yiduobo的每日leetcode 2098.长度为K的最大偶数和子序列](https://zhuanlan.zhihu.com/p/626225702) · 知乎 · 2023-05-02 · 赞同 0**
> 力扣：[2098. 长度为K的最大偶数和子序列](https://leetcode.cn/problems/subsequence-of-size-k-with-the-largest-even-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2098.长度为K的最大偶数和

[力扣](https://leetcode.cn/problems/subsequence-of-size-k-with-the-largest-even-sum/)

题目要求子序列的和为偶数，那么其中必然包含偶数个奇数，而剩下则由偶数来填充。另一方面，为了使得子序列之和最大，在这里选取的必然是最大的奇数和偶数。于是可以先将数组按照奇数和偶数区分开来，接下来枚举最终选择奇数的数量odd_cnt，这里的odd_cnt必须为偶数，那么剩下偶数的数量even_cnt就必然是k - odd_cnt，此时则可以用最大的odd_cnt个奇数以及最大的even_cnt个偶数之和来更新答案了。

为了提高效率，在这里可以先将区分开的奇数和偶数分别排序，那么最大的若干个奇数以及最大的若干个偶数就变成了前缀和的问题，可以提前一趟遍历预处理出来。

最后附上python代码：

```python
class Solution(object):
    def largestEvenSum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        odd = []
        even = []
        for v in nums:
            if v % 2 == 0:
                even.append(v)
            else:
                odd.append(v)
        
        odd.sort(reverse=True)
        even.sort(reverse=True)

        odd_s = [0]
        for v in odd:
            odd_s.append(odd_s[-1] + v)
        
        even_s = [0]
        for v in even:
            even_s.append(even_s[-1] + v)
        
        res = -1
        for odd_cnt in range(0, min(len(odd), k) + 1, 2):
            if odd_cnt + len(even) < k:
                continue
            
            res = max(res, odd_s[odd_cnt] + even_s[k - odd_cnt])
        
        return res
```
