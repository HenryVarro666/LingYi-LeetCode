---
title: "1909. 删除一个元素使数组严格递增"
aliases: ["yiduobo的每日leetcode 1909.删除一个元素使数组严格递增"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/482248210"
zhihu_id: "482248210"
zhihu_title: "yiduobo的每日leetcode 1909.删除一个元素使数组严格递增"
question_id: "1909"
question: "删除一个元素使数组严格递增"
problem_url: "https://leetcode.cn/problems/remove-one-element-to-make-the-array-strictly-increasing/"
difficulty: "Easy"
created: "2022-03-17T00:29:20+08:00"
updated: "2022-03-17T00:29:20+08:00"
upvotes: 0
comments: 0
---

# 1909. 删除一个元素使数组严格递增

> **[yiduobo的每日leetcode 1909.删除一个元素使数组严格递增](https://zhuanlan.zhihu.com/p/482248210) · 知乎 · 2022-03-17 · 赞同 0**
> 力扣：[1909. 删除一个元素使数组严格递增](https://leetcode.cn/problems/remove-one-element-to-make-the-array-strictly-increasing/) · Easy · 灵茶山艾府：[O(n) 做法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1909.删除一个元素使数组严格递增

[力扣](https://leetcode-cn.com/problems/remove-one-element-to-make-the-array-strictly-increasing/)

题目有一次删除元素的机会，那么必然要用到第一次出现非递增的地方。对于这两个数，不妨记为nums[index]和nums[index + 1]，那么在这里有nums[index] >\= nums[index + 1]。从贪心的角度来说，为了继续适配后面的数字，这里显然就应该删去nums[index]，但是这里有一种可能的情况是nums[index - 1] \< nums[index]，且nums[index - 1] >\= nums[index + 1]。对于这种情况，如果删去nums[index]将导致新的非递增出现，此时就必须删去nums[index + 1]。其他情况下，还是应该删去nums[index]。

删除之后，继续向后遍历，若再次出现非递增，那么就返回false。如果能走完遍历，那么答案就是true。

最后附上python代码：

```python
class Solution(object):
    def canBeIncreasing(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        n = len(nums)
        cnt = 0
        last = nums[0]
        for index in range(1, n):
            if nums[index] <= last:
                cnt += 1
                if cnt == 2:
                    return False
                if index > 1 and nums[index - 2] >= nums[index]:
                    last = nums[index - 1]
                else:
                    last = nums[index]
            else:
                last = nums[index]

        return True
```
