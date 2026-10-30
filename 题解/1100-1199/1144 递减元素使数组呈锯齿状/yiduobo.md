---
title: "1144. 递减元素使数组呈锯齿状"
aliases: ["yiduobo的每日leetcode 1144.递减元素使数组呈锯齿状"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/377446518"
zhihu_id: "377446518"
zhihu_title: "yiduobo的每日leetcode 1144.递减元素使数组呈锯齿状"
question_id: "1144"
question: "递减元素使数组呈锯齿状"
problem_url: "https://leetcode.cn/problems/decrease-elements-to-make-array-zigzag/"
difficulty: "Medium"
rating: 1559
created: "2021-06-02T23:18:04+08:00"
updated: "2021-06-02T23:18:04+08:00"
upvotes: 0
comments: 0
---

# 1144. 递减元素使数组呈锯齿状

> **[yiduobo的每日leetcode 1144.递减元素使数组呈锯齿状](https://zhuanlan.zhihu.com/p/377446518) · 知乎 · 2021-06-02 · 赞同 0**
> 力扣：[1144. 递减元素使数组呈锯齿状](https://leetcode.cn/problems/decrease-elements-to-make-array-zigzag/) · Medium · 灵茶山艾府：[没有思路？一步步提示你思考！（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1144.递减元素使数组呈锯齿状

[力扣](https://leetcode-cn.com/problems/decrease-elements-to-make-array-zigzag/)

题目给出了两种可能的答案，仔细观察二者只有在奇偶性上有差别，那么我们不妨讨论

A[0] > A[1] \< A[2] > A[3] \< A[4] > ...

主题到题目只能使用递减操作，因此对于这种情况，偶数下标的A[0]、A[2]、A[4]、...等我们都不应该对其进行操作，而对于奇数下标的A[1]、A[3]、A[5]、...这些，我们就可以通过判断其与两侧偶数下标的数的大小来进行操作。

具体来说对于A[index]，其中index为奇数，由于需要使得

A[index - 1] > A[index] \< A[index + 1]

同时A[index - 1]以及A[index + 1]的值是不变的，因此只有当A[index] >\= A[index - 1]或者A[index] >\= A[index + 1]时我们才有必要对A[index]进行操作。

操作的最终目标为min(A[index - 1] - 1, A[index + 1] - 1)，因此最小的操作次数就是A[index] - min(A[index - 1] - 1, A[index + 1] - 1)

遍历所有的奇数下标，计算操作次数然后求和即可求出这种情况的最少操作次数。对于另一种情况，则只需要将下标的奇偶性反过来，按同样的方法遍历求解即可。

最后附上python代码：

```python
class Solution(object):
    def movesToMakeZigzag(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        p1 = 0
        for index in range(0, n, 2):
            left = right = 0
            if index > 0 and nums[index] >= nums[index - 1]:
                left = nums[index] - nums[index - 1] + 1
            if index < n - 1 and nums[index] >= nums[index + 1]:
                right = nums[index] - nums[index + 1] + 1
            p1 += max(left, right)

        p2 = 0
        for index in range(1, n, 2):
            left = right = 0
            if index > 0 and nums[index] >= nums[index - 1]:
                left = nums[index] - nums[index - 1] + 1
            if index < n - 1 and nums[index] >= nums[index + 1]:
                right = nums[index] - nums[index + 1] + 1
            p2 += max(left, right)

        return min(p1, p2)
```
