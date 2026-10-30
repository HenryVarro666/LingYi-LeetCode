---
title: "1403. 非递增顺序的最小子序列"
aliases: ["yiduobo的每日leetcode 1403.非递增顺序的最小子序列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/405206014"
zhihu_id: "405206014"
zhihu_title: "yiduobo的每日leetcode 1403.非递增顺序的最小子序列"
question_id: "1403"
question: "非递增顺序的最小子序列"
problem_url: "https://leetcode.cn/problems/minimum-subsequence-in-non-increasing-order/"
created: "2021-08-30T23:28:43+08:00"
updated: "2021-08-30T23:28:43+08:00"
upvotes: 0
comments: 0
---

# 1403. 非递增顺序的最小子序列

> **[yiduobo的每日leetcode 1403.非递增顺序的最小子序列](https://zhuanlan.zhihu.com/p/405206014) · 知乎 · 2021-08-30 · 赞同 0**
> 力扣：[1403. 非递增顺序的最小子序列](https://leetcode.cn/problems/minimum-subsequence-in-non-increasing-order/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1403.非递增顺序的最小子序列

[力扣](https://leetcode-cn.com/problems/minimum-subsequence-in-non-increasing-order/)

比较基础的题目，为了选出值超过一半的子序列，同时要求序列最短，那么显然应该先选择数值较大的元素，于是可以先将数组从大到小进行排序，然后从大到小进行选择，直到数值之和大于所有数之和的一半为止。由于这里的数值最多只有100，因此我选择的是类似桶排序的做法，使用数组下标来帮助排序。

最后附上python代码：

```python
class Solution(object):
    def minSubsequence(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        cnt_list = [0] * 101
        s = 0
        for num in nums:
            cnt_list[num] += 1
            s += num
        
        res = []
        now = 0
        for num in range(100, 0, -1):
            while cnt_list[num] > 0 and now + now <= s:
                now += num
                cnt_list[num] -= 1
                res.append(num)
        
            if now + now > s:
                break

        return res
```
