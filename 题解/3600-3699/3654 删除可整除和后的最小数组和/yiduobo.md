---
title: "3654. 删除可整除和后的最小数组和"
aliases: ["yiduobo的每日leetcode 3654.删除可整除和后的最小数组和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/prefix-sum", "题单/动态规划", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1948925375485809852"
zhihu_id: "1948925375485809852"
zhihu_title: "yiduobo的每日leetcode 3654.删除可整除和后的最小数组和"
question_id: "3654"
question: "删除可整除和后的最小数组和"
problem_url: "https://leetcode.cn/problems/minimum-sum-after-divisible-sum-deletions/"
difficulty: "Medium"
rating: 2039
created: "2025-09-13T00:49:18+08:00"
updated: "2025-09-13T00:49:20+08:00"
upvotes: 1
comments: 0
---

# 3654. 删除可整除和后的最小数组和

> **[yiduobo的每日leetcode 3654.删除可整除和后的最小数组和](https://zhuanlan.zhihu.com/p/1948925375485809852) · 知乎 · 2025-09-13 · 赞同 1**
> 力扣：[3654. 删除可整除和后的最小数组和](https://leetcode.cn/problems/minimum-sum-after-divisible-sum-deletions/) · Medium · 灵茶山艾府：[动态规划 + 前缀和（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3654.删除可整除和后的最小数组和

[3654. 删除可整除和后的最小数组和 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-sum-after-divisible-sum-deletions/description/)

给你一个整数数组nums和一个整数k。

可以从中多次选择和为k的倍数的子数组，并将这个子数组删除。删除后，后续的元素将填补空缺。问执行任意次删除操作后nums的最小可能和。

直观感觉上并没有什么特别好的删除策略，不过本题也可以往区间划分的问题上去靠拢，因此可以尝试使用动态规划进行求解。具体来说，令f[index]表示对nums[0]到nums[index]进行操作后可以得到的最小可能和，那么对于f[index]，如果保留nums[index]，那么就有f[index] \= f[index - 1]；反之，则需要遍历所有满足nums[p: index + 1]之和为k的倍数的下标p，然后使用其中最小的f[p - 1]来更新f[index]。

对于上面的区间和模k等于0的这一条件，可以转化为前缀和模k是否相等，也就是说对于f[index]，不妨设当前的前缀和为s[index]，那么在这里就只需要找出所有满足s[p - 1] % k等于s[index] % k的下标p，然后使用其中最小的f[p - 1]来更新f[index]。

基于这一点，就可以使用一个数组best，记录每种前缀模k的余数对应的最优的f，这样一来就可以直接使用best[s[index] % k]来更新f[index]了。在更新完f[index]之后，再使用f[index]更新best[s[index] % k]即可。

另外，在这里的f每一轮之和上一轮有关，而s则只会在计算f时使用一次，因此可以使用变量迭代省去这两个数组，只保留best数组就行了。

最后附上python代码：

```python
class Solution(object):
    def minArraySum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        best = [None] * k
        best[0] = 0
        f = [0]
        s = 0
        res = 0
        for v in nums:
            res += v
            s += v
            s %= k
            if best[s] is not None:
                res = min(res, best[s])
            
            if best[s] is None or best[s] > res:
                best[s] = res
        
        return res
```
