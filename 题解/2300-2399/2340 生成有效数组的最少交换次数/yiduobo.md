---
title: "2340. 生成有效数组的最少交换次数"
aliases: ["yiduobo的每日leetcode 2340.生成有效数组的最少交换次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/629920277"
zhihu_id: "629920277"
zhihu_title: "yiduobo的每日leetcode 2340.生成有效数组的最少交换次数"
question_id: "2340"
question: "生成有效数组的最少交换次数"
problem_url: "https://leetcode.cn/problems/minimum-adjacent-swaps-to-make-a-valid-array/"
created: "2023-05-16T23:08:17+08:00"
updated: "2023-05-16T23:08:17+08:00"
upvotes: 1
comments: 0
---

# 2340. 生成有效数组的最少交换次数

> **[yiduobo的每日leetcode 2340.生成有效数组的最少交换次数](https://zhuanlan.zhihu.com/p/629920277) · 知乎 · 2023-05-16 · 赞同 1**
> 力扣：[2340. 生成有效数组的最少交换次数](https://leetcode.cn/problems/minimum-adjacent-swaps-to-make-a-valid-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2340.生成有效数组的最少交换次数

[力扣](https://leetcode.cn/problems/minimum-adjacent-swaps-to-make-a-valid-array/)

为了使得交换次数最少，就应该将首次出现的最小值以及最后一次出现的最大值分别移动到数组的首部和尾部。不妨设二者的下标位置分别为mi和ma，那么所需的移动次数就是mi + (n - 1 - ma)。另外需要特别注意的是，若初始情况下mi > ma，那么在交换过程中这两个数会生成一次交换，而这次交换被计算在了mi和(n - 1 - ma)内，因此在这种情况下应该将答案再减去1。

最后附上python代码：

```python
class Solution(object):
    def minimumSwaps(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        ma = mi = 0
        n = len(nums)
        for index in range(1, n):
            if nums[index] < nums[mi]:
                mi = index
            if nums[index] >= nums[ma]:
                ma = index
        
        res = mi + len(nums) - 1 - ma
        if ma < mi:
            res -= 1
        return res
```
