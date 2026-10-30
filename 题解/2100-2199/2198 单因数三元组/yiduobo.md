---
title: "2198. 单因数三元组"
aliases: ["yiduobo的每日leetcode 2198.单因数三元组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/627557479"
zhihu_id: "627557479"
zhihu_title: "yiduobo的每日leetcode 2198.单因数三元组"
question_id: "2198"
question: "单因数三元组"
problem_url: "https://leetcode.cn/problems/number-of-single-divisor-triplets/"
created: "2023-05-07T23:10:32+08:00"
updated: "2023-05-07T23:10:32+08:00"
upvotes: 0
comments: 0
---

# 2198. 单因数三元组

> **[yiduobo的每日leetcode 2198.单因数三元组](https://zhuanlan.zhihu.com/p/627557479) · 知乎 · 2023-05-07 · 赞同 0**
> 力扣：[2198. 单因数三元组](https://leetcode.cn/problems/number-of-single-divisor-triplets/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2198.单因数三元组

[力扣](https://leetcode.cn/problems/number-of-single-divisor-triplets/)

本题给出的数组长度比较大，但是具体数值的取值范围仅在1到100之间，因此可以通过数值而不是下标来考虑。

首先使用哈希表统计每种数值出现的次数，接下来三重循环，直接枚举三元组中的三个数值，同时记录在枚举时该数值的剩余可用次数。若这三个数值满足题目的要求，那么就将记录的可用次数相乘并累加到答案中。

在这里记录可用次数的理由是这些数值可能相同，那么当枚举到相同数值时，可用次数产生了变化，因此必须记录枚举时的可用次数，而不是直接使用哈希表中的可用次数。

最后附上python代码：

```python
class Solution(object):
    def singleDivisorTriplet(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        cnt = [0] * 101
        for v in nums:
            cnt[v] += 1
        
        res = 0
        for i in range(1, 101):
            if cnt[i] > 0:
                cnt_i = cnt[i]
                cnt[i] -= 1
            else:
                continue

            for j in range(1, 101):
                if cnt[j] > 0:
                    cnt_j = cnt[j]
                    cnt[j] -= 1
                else:
                    continue

                for k in range(1, 101):
                    if cnt[k] == 0:
                        continue
                    
                    s = i + j + k
                    i_flag = j_flag = k_flag = 1
                    if s % i == 0:
                        i_flag = 0
                    if s % j == 0:
                        j_flag = 0
                    if s % k == 0:
                        k_flag = 0
                    
                    if i_flag + j_flag + k_flag == 2:
                        res += cnt_i * cnt_j * cnt[k]

                cnt[j] += 1
            
            cnt[i] += 1

        return res
```
