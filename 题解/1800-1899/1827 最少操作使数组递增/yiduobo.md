---
title: "1827. 最少操作使数组递增"
aliases: ["yiduobo的每日leetcode 1827.最少操作使数组递增"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/466964373"
zhihu_id: "466964373"
zhihu_title: "yiduobo的每日leetcode 1827.最少操作使数组递增"
question_id: "1827"
question: "最少操作使数组递增"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-the-array-increasing/"
created: "2022-02-13T19:19:07+08:00"
updated: "2022-02-13T19:19:07+08:00"
upvotes: 0
comments: 0
---

# 1827. 最少操作使数组递增

> **[yiduobo的每日leetcode 1827.最少操作使数组递增](https://zhuanlan.zhihu.com/p/466964373) · 知乎 · 2022-02-13 · 赞同 0**
> 力扣：[1827. 最少操作使数组递增](https://leetcode.cn/problems/minimum-operations-to-make-the-array-increasing/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1827.最少操作使数组递增

[力扣](https://leetcode-cn.com/problems/minimum-operations-to-make-the-array-increasing/)

对于一个数而言，操作次数越少答案越小，同时越有利于后面的数字递增，因此在这里就是要找到每个数字最少操作的次数。由于每个数字的最少操作的次数与前一个数字的最终值有关，因此可以从头开始向后一趟扫描，对于当前数字num，根据上一个数的最终值last决定当前数应该执行多少次操作。

若num \<\= last，那么需要将num变为last + 1，此时操作次数为last + 1 - num，使用这个值更新答案，并将last更新为last + 1。

若num > last，那么此时不需要进行操作，不过last需要更新为num。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        last = nums[0]
        res = 0
        for num in nums[1:]:
            if num < last + 1:
                res += last + 1 - num
                last += 1
            else:
                last = num
        
        return res
```
