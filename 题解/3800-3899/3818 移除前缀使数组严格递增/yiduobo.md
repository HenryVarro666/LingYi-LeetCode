---
title: "3818. 移除前缀使数组严格递增"
aliases: ["yiduobo的每日leetcode 3818.移除前缀使数组严格递增"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1998860611338121903"
zhihu_id: "1998860611338121903"
zhihu_title: "yiduobo的每日leetcode 3818.移除前缀使数组严格递增"
question_id: "3818"
question: "移除前缀使数组严格递增"
problem_url: "https://leetcode.cn/problems/minimum-prefix-removal-to-make-array-strictly-increasing/"
difficulty: "Medium"
created: "2026-01-25T21:41:33+08:00"
updated: "2026-01-25T21:41:33+08:00"
upvotes: 2
comments: 0
---

# 3818. 移除前缀使数组严格递增

> **[yiduobo的每日leetcode 3818.移除前缀使数组严格递增](https://zhuanlan.zhihu.com/p/1998860611338121903) · 知乎 · 2026-01-25 · 赞同 2**
> 力扣：[3818. 移除前缀使数组严格递增](https://leetcode.cn/problems/minimum-prefix-removal-to-make-array-strictly-increasing/) · Medium · 灵茶山艾府：[倒序遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3818.移除前缀使数组严格递增

<https://leetcode.cn/problems/minimum-prefix-removal-to-make-array-strictly-increasing/description/>

题目给出一个整数数组nums。现在要求从nums中恰好移除一个前缀(可以为空)，使得剩余的数组严格递增。

问被移除的前缀的最小长度是多少。

移除的前缀长度最小，就意味着剩下的单调递增的后缀长度最长。于是只需从后往前一趟遍历，找出第一个满足nums[index] >\= nums[index + 1]的下标，从nums[index + 1]开始的后缀是单调递增的，但是再往前就不行了，因此最优的方案就是删掉nums[0]到nums[index]这个前缀。

最后附上python代码：

```python
class Solution(object):
    def minimumPrefixLength(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        res = len(nums) - 1
        pre = nums[-1]

        for v in nums[-2::-1]:
            if v >= pre:
                break
            res -= 1
            pre = v
        
        return res
```
