---
title: "3231. 要删除的递增子序列的最小数量"
aliases: ["yiduobo的每日leetcode 3231.要删除的递增子序列的最小数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/720236814"
zhihu_id: "720236814"
zhihu_title: "yiduobo的每日leetcode 3231.要删除的递增子序列的最小数量"
question_id: "3231"
question: "要删除的递增子序列的最小数量"
problem_url: "https://leetcode.cn/problems/minimum-number-of-increasing-subsequence-to-be-removed/"
created: "2024-09-14T22:02:11+08:00"
updated: "2024-09-14T22:02:11+08:00"
upvotes: 1
comments: 0
---

# 3231. 要删除的递增子序列的最小数量

> **[yiduobo的每日leetcode 3231.要删除的递增子序列的最小数量](https://zhuanlan.zhihu.com/p/720236814) · 知乎 · 2024-09-14 · 赞同 1**
> 力扣：[3231. 要删除的递增子序列的最小数量](https://leetcode.cn/problems/minimum-number-of-increasing-subsequence-to-be-removed/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3231.要删除的递增子序列的最小数量

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-number-of-increasing-subsequence-to-be-removed/description/)

题目给出一个整数数组nums，每一轮可以从中删去一个严格递增的子序列，问将数组情况所需的最少操作次数。

题目实际上就是问nums最少可以拆分成多少个递增子序列，那么在这里不妨设已经将nums[0]到nums[p - 1]按最优的方法划分成了若干个递增子序列，接下来考虑对于nums[p]应该如何处理。

最优的方法值得是在满足划分的子序列数量最少得前提下，每个子序列的最后一个数都尽量的小，这样的话后面的数就更有可能接在之前某个子序列的后面。

那么对于nums[p]：

1、若nums[p]小于等于当前已有递增子序列中最小的最后一个数：

这种情况下，nums[p]无法接在任何一个子序列后面，同时也不应该让nums[p]去替换掉任何一个子序列中的元素，因为替换出来的元素一定大于等于nums[p]，使用替换元素单独形成的子序列并不比使用nums[p]单独构成的子序列更优。

也就是说，这种情况下应该从nums[p]开始另起一个新的子序列。

2、若nums[p]大于某个已有递增子序列中的最后一个数：

此时就应该选择最后一个数最大的那个子序列，将nums[p]接在这个子序列后面，这样一来在保证了子序列总数最小的前提下，还能让已有子序列的最后一项尽量的小。

可以发现，上面这两个过程只需要保证所有子序列的最后一个数是单调递减的，就可以在O(1)和O(logn)的情况下处理nums[p]了。到了这里可以发现，整个处理过程与计算nums的最长不增子序列完全相同，应该是有办法证明这两个问题是完全等价的，不过我在这里没有继续往下想了。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        f = [nums[0]]
        for v in nums[1:]:
            if v <= f[-1]:
                f.append(v)
            else:
                left = 0
                right = len(f) - 1
                while left < right:
                    mid = (left + right) // 2
                    if f[mid] >= v:
                        left = mid + 1
                    else:
                        right = mid
                
                f[left] = v

        return len(f)
```
