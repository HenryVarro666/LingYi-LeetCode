---
title: "3018. 可处理的最大删除操作数I"
aliases: ["yiduobo的每日leetcode 3018.可处理的最大删除操作数I"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/694394695"
zhihu_id: "694394695"
zhihu_title: "yiduobo的每日leetcode 3018.可处理的最大删除操作数I"
question_id: "3018"
question: "可处理的最大删除操作数I"
problem_url: "https://leetcode.cn/problems/maximum-number-of-removal-queries-that-can-be-processed-i/"
created: "2024-04-25T02:45:11+08:00"
updated: "2024-04-25T02:45:11+08:00"
upvotes: 1
comments: 0
---

# 3018. 可处理的最大删除操作数I

> **[yiduobo的每日leetcode 3018.可处理的最大删除操作数I](https://zhuanlan.zhihu.com/p/694394695) · 知乎 · 2024-04-25 · 赞同 1**
> 力扣：[3018. 可处理的最大删除操作数I](https://leetcode.cn/problems/maximum-number-of-removal-queries-that-can-be-processed-i/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3018.可处理的最大删除操作数I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-number-of-removal-queries-that-can-be-processed-i/description/)

题目看上去像是很常规的区间动态规划问题，但是在这里是外侧匹配数组的前缀，那么状态的设计和更新的方向就需要反过来。

令f[left][right]表示整个数组删除到剩下left到right这一段时可以匹配的最长前缀，那么对于f[left][right]：

1、如果left > 0，且f[left - 1][right] \< len(queries)：

此时就可以尝试通过保留nums\[left - 1\]，使其匹配queries\[f\[left -1 \]\[right\]\]，然后通过f\[left - 1\]\[right\]来更新f\[left\]\[right\]。

即nums\[left - 1\] >\= queries\[f\[left - 1\]\[right\]\]时，有

f[left][right] \= max(f[left][right], f[left - 1][right] + 1)

反之若不满足，那么也可以删掉nums[left - 1]，那么就有

f[left][right] \= max(f[left][right], f[left - 1][right])

2、如果right \< n - 1，且f[left][right + 1] \< len(queries)：

与情况1对称，此时则需要考察nums\[right + 1\]与queries\[f\[left\]\[right + 1\]\]的大小。

当nums\[right + 1\] >\= queries\[f\[left\]\[right + 1\]\]时，有

f[left][right] \= max(f[left][right], f[left][right + 1] + 1）

反之则有

f[left][right] \= max(f[left][right], f[left][right + 1])

若某一时刻得到了f\[left\]\[right\]等于len(queries)，那么就直接返回len(queries)，否则在全部计算完成后，还需要遍历数组中的每个数nums\[index\]，因为在上面的状态设计中没法表示全部用完了这一状态，因此还需要对比nums\[index\]与queries\[f\[index\]\[index\]\]的大小，如果大于等于，那么最后剩下的nums\[index\]还可以额外多匹配一个，此时就应该用f\[index\]\[index\] + 1来更新答案，否则就只能用f\[index\]\[index\]来更新答案。

与常规的区间动态规划不同，本题由于空间的限制不能将queries中下一个匹配的位置直接表示在状态中，那么就必须将下一个匹配的位置保存在结果数组中。为了适配这一点，状态的设计就必须适配从外向内的转移方式而不是常规区间动态规划的从内向外。

最后附上python代码：

```python
class Solution(object):
    def maximumProcessableQueries(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[int]
        :rtype: int
        """

        n = len(nums)
        f = [[0] * n for _ in range(n)]
        for l in range(n - 1, 0, -1):
            for left in range(n):
                right = left + l - 1
                if right >= n:
                    break
                
                if left > 0:
                    if f[left - 1][right] < len(queries) and nums[left - 1] >= queries[f[left - 1][right]]:
                        delta = 1
                    else:
                        delta = 0
                    
                    f[left][right] = f[left - 1][right] + delta

                if right < n - 1:
                    if f[left][right + 1] < len(queries) and nums[right + 1] >= queries[f[left][right + 1]]:
                        delta = 1
                    else:
                        delta = 0
                    
                    f[left][right] = max(f[left][right], f[left][right + 1] + delta)
                
                if f[left][right] == len(queries):
                    return f[left][right]

        res = 0
        for index in range(n):
            if nums[index] >= queries[f[index][index]]:
                delta = 1
            else:
                delta = 0
            res = max(res, f[index][index] + delta)
        
        return res
```
