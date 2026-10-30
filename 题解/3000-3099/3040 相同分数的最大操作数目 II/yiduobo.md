---
title: "3040. 相同分数的最大操作数目II"
aliases: ["yiduobo的每日leetcode 3040.相同分数的最大操作数目II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/di-tui", "题单/动态规划", "题单/动态规划/八-区间-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/695832750"
zhihu_id: "695832750"
zhihu_title: "yiduobo的每日leetcode 3040.相同分数的最大操作数目II"
question_id: "3040"
question: "相同分数的最大操作数目 II"
problem_url: "https://leetcode.cn/problems/maximum-number-of-operations-with-the-same-score-ii/"
difficulty: "Medium"
rating: 1709
created: "2024-05-03T22:31:17+08:00"
updated: "2024-05-03T22:31:17+08:00"
upvotes: 1
comments: 0
---

# 3040. 相同分数的最大操作数目II

> **[yiduobo的每日leetcode 3040.相同分数的最大操作数目II](https://zhuanlan.zhihu.com/p/695832750) · 知乎 · 2024-05-03 · 赞同 1**
> 力扣：[3040. 相同分数的最大操作数目 II](https://leetcode.cn/problems/maximum-number-of-operations-with-the-same-score-ii/) · Medium · 灵茶山艾府：[两种方法：记忆化搜索/递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3040.相同分数的最大操作数目II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-number-of-operations-with-the-same-score-ii/description/)

之前3038题的强化版，由于本题的操作可以选取前两个元素、后两个元素、或者一头一尾两个元素，因此在这里只能使用动态规划来求解。

首先，需要从上面三种做法中选取一种，来确定目标值target，接下来就可以用动态规划求解了。令f[left][right]表示区间left到right得到target可以执行的最大操作数，那么：

1、若nums[left] + nums[left + 1]等于target，就有f[left][right] \= max(f[left][right], f[left + 2][right] + 1)

2、若nums[right] + nums[right - 1]等于target，就有f[left][right] \= max(f[left][right], f[left][right - 2] + 1)

3、若nums[left] + nums[right]等于target，就有f[left][right] \= max(f[left][right], f[left + 1][right - 1] + 1)

当选取nums[0] + nums[1]作为target时，需要计算f[2][n - 1]。

当选取nums[-1] + nums[-2]作为target时，需要计算f[0][n - 3]。

当选取nums[0] + nums[-1]作为target时，需要计算f[1][n - 2]。

需要注意上面每次计算之前都需要将f数组重置为0。三种情况都计算完成后，将其中的最大值加上1即为最终答案，这里加1的含义是最初选取target时进行的这次操作。

具体实现上，可以采用枚举区间长度的动态规划，也可以采用记忆化搜索。在这里采用记忆化搜索相对更优，因为本题是从外向内逐步选取数字的，这也就意味着部分中间的状态是不可能遍历到，同时还有部分状态则是因为不够优所以没必要遍历到。虽然两种写法的时间复杂度都是O(n^2)，但是相比递推的写法，在这里使用记忆化搜索可以天然地省去一些不必要的操作，另外还可以额外添加一些剪枝使得性能更优。

最后附上python代码：

```python
class Solution(object):
    def maxOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        if n == 2:
            return 1

        def calc(f, left, right, target):
            if f[left][right] == 0:
                if left == right:
                    f[left][right] = 0
                    return 0
                
                if left == right - 1:
                    if nums[left] + nums[right] == target:
                        f[left][right] = 1
                    else:
                        f[left][right] = 0
                    return f[left][right]
                
                if nums[left] + nums[right] == target:
                    f[left][right] = calc(f, left + 1, right - 1, target) + 1
                    if f[left][right] == (right - left + 1) // 2:
                        return f[left][right]
                
                if nums[left] + nums[left + 1] == target:
                    f[left][right] = max(f[left][right], calc(f, left + 2, right, target) + 1)
                    if f[left][right] == (right - left + 1) // 2:
                        return f[left][right]

                if nums[right] + nums[right - 1] == target:
                    f[left][right] = max(f[left][right], calc(f, left, right - 2, target) + 1)
        

            return f[left][right]
        

        f = [[0] * n for _ in range(n)]
        res = calc(f, 2, n - 1, nums[0] + nums[1])
        f = [[0] * n for _ in range(n)]
        res = max(res, calc(f, 0, n - 3, nums[-1] + nums[-2]))
        f = [[0] * n for _ in range(n)]
        res = max(res, calc(f, 1, n - 2, nums[0] + nums[-1]))
        return res + 1
```
