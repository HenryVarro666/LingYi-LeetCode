---
title: "2488. 统计中位数为K的子数组"
aliases: ["yiduobo的每日leetcode 2488.统计中位数为K的子数组"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/array", "leetcode/hash-table", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/590101487"
zhihu_id: "590101487"
zhihu_title: "yiduobo的每日leetcode 2488.统计中位数为K的子数组"
question_id: "2488"
question: "统计中位数为 K 的子数组"
problem_url: "https://leetcode.cn/problems/count-subarrays-with-median-k/"
difficulty: "Hard"
rating: 1999
created: "2022-12-08T02:03:00+08:00"
updated: "2022-12-08T02:03:00+08:00"
upvotes: 0
comments: 0
---

# 2488. 统计中位数为K的子数组

> **[yiduobo的每日leetcode 2488.统计中位数为K的子数组](https://zhuanlan.zhihu.com/p/590101487) · 知乎 · 2022-12-08 · 赞同 0**
> 力扣：[2488. 统计中位数为 K 的子数组](https://leetcode.cn/problems/count-subarrays-with-median-k/) · Hard · 灵茶山艾府：[转化成 560 题，一次遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2488.统计中位数为K的子数组

[力扣](https://leetcode.cn/problems/count-subarrays-with-median-k/)

题目给出的数组中各个数字都互不相同，而对于偶数长度的子数组，并不是按照取平均，而是直接取中间较小的那个数作为中位数，这也就意味着题目要找的子数组中必须包含数字K。

不妨设K的下标为p，那么合法的子数组有两种可能：

1、子数组[l, r]满足l \<\= p \<\= r，且l到r之间恰好有m个大于K的数以及m个小于K的数

2、子数组[l, r]满足l \< p \< r，且l到r之间恰好有m + 1个大于K的数以及m个小于K的数

也就是说，如果以p为右边界的某个子数组，其包含的数字中比K大的数字的数量与比K小的数字的数量之差为cnt的话，那么如果存在另一个以p为左边界，且比K小的数字的数量与比K大的数字的数量之差为-cnt或者-cnt + 1的子数组，这两个子数组拼起来就可以得到一个中位数为K的子数组。

于是可以从p开始分别向两侧遍历，计算以p为右边界和以p为左边界的子数组中，比K大的数的数量和比K小的数的数量之差cnt，并使用两个哈希表left和right分别记录下来，然后就只需遍历所有的cnt，使用left[cnt] \* (right[-cnt] + right[1 - cnt])来更新答案即可。

在枚举cnt时需要注意不要忘了cnt等于0的情况。

最后附上python代码：

```python
class Solution(object):
    def countSubarrays(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        p = None
        for index, num in enumerate(nums):
            if num == k:
                p = index
                break
        
        left_cnt = {0 : 1}
        now = 0
        for index in range(p - 1, -1, -1):
            if nums[index] < k:
                now -= 1
            else:
                now += 1
            left_cnt[now] = left_cnt.get(now, 0) + 1
        
        right_cnt = {0 : 1}
        now = 0
        for index in range(p + 1, len(nums)):
            if nums[index] < k:
                now -= 1
            else:
                now += 1
            right_cnt[now] = right_cnt.get(now, 0) + 1

        res = left_cnt.get(0, 0) * right_cnt.get(0, 0)
        for cnt in left_cnt:
            if cnt > 0:
                res += left_cnt[cnt] * (right_cnt.get(-cnt, 0) + right_cnt.get(1 - cnt, 0))
        
        for cnt in right_cnt:
            if cnt > 0:
                res += right_cnt[cnt] * (left_cnt.get(-cnt, 0) + left_cnt.get(1 - cnt, 0))
        
        return res
```
