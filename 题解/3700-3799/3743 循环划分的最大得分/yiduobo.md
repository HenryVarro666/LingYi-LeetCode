---
title: "3743. 循环划分的最大得分"
aliases: ["yiduobo的每日leetcode 3743.循环划分的最大得分"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/六-状态机-DP", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1970894098668975518"
zhihu_id: "1970894098668975518"
zhihu_title: "yiduobo的每日leetcode 3743.循环划分的最大得分"
question_id: "3743"
question: "循环划分的最大得分"
problem_url: "https://leetcode.cn/problems/maximize-cyclic-partition-score/"
difficulty: "Hard"
rating: 3125
created: "2025-11-11T22:56:04+08:00"
updated: "2025-11-11T22:56:05+08:00"
upvotes: 1
comments: 0
---

# 3743. 循环划分的最大得分

> **[yiduobo的每日leetcode 3743.循环划分的最大得分](https://zhuanlan.zhihu.com/p/1970894098668975518) · 知乎 · 2025-11-11 · 赞同 1**
> 力扣：[3743. 循环划分的最大得分](https://leetcode.cn/problems/maximize-cyclic-partition-score/) · Hard · 灵茶山艾府：[找到最佳断环位置，转化成买卖股票问题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3743.循环划分的最大得分

[3743. 循环划分的最大得分 - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-cyclic-partition-score/description/)

题目给出一个循环数组nums，其长度不超过1000。另外给出一个整数k，k不超过nums的长度。

现在要求将nums划分为最多k个子数组，由于nums是循环数组，这些子数组可以从数组末尾环绕回起点。

子数组的范围定义为其中最大值与最小值之差，而一个划分的得分则定义为其划分出来的所有子数组的范围之和。问最大的划分得分是多少。

如果不考虑循环数组这一条件，那么就可以使用f[index][t]表示将前index个元素划分为t个子数组可以得到的最大得分。对于f[index][t]，则需要寻找一个最优的p，使得f[p][t - 1] + max(nums[p + 1: index + 1]) - min(nums[p + 1: index + 1])最大。即使使用线段树或者st算法计算区间最大值和最小值，以上算法的时间复杂度也是O(n^2 \* k \* log(n))，已经不成立了，而且还没有考虑循环数组这一条件，必须想办法进行优化。

由于最终决定得分的是子数组中的最大值和最小值，那么不妨从最值出发来考虑。对于当前子数组中的最小值，不妨设其下标为index，那么当与其配对的最大值出现在index左侧时，子数组中所有处于index右侧的部分就应该全部留给下一个子数组，因为划分到当前子数组中并不会影响当前子数组的得分，但是有可能使得下一个子数组的得分更优。同样的，若这个最大值出现在index右侧时，子数组中所有处于index左侧的部分则应该全部留给上一个子数组。更进一步的，最大值也应该遵循这个规则，那么就可以发现，本题实际上就要要找出k组配对的最大值和最小值，而对于没被划分到子数组中的部分，则可以自由合并到相邻的子数组中，这些元素不影响最终答案。

可以发现，这就是之前遇到过的，可以买卖k次，且可以做多也可以做空的股票问题，于是可以通过一趟遍历，使用动态规划进行求解。令f[index][t]表示前index个元素，已经完成了t次划分且当前还没有选取下一次划分的最大值或者最小值时的最优得分，g[index][t]则表示选取了下一次划分中的最小值时的最优得分，h[index][t]则表示选择了下一次划分中的最大值时的最优得分，那么：

1、对于f[index - 1][t]，若其非空，就可以使用f[index - 1][t] - nums[index]来更新g[index][t]，使用f[index - 1][t] + nums[index]来更新h[index][t]

2、若g[index - 1][t - 1]非空，则可以使用g[index - 1][t - 1] + nums[index]来更新f[index][t]

3、若h[index - 1][t - 1]非空，则可以使用h[index - 1][t - 1] + nums[index]来更新f[index][t]

由于每一轮的状态只与上一轮有关，在这里可以通过倒序遍历t省去index这一维，而最终的最大得分就是max(f)

到了这里，就可以在O(nk)的时间内解决非循环数组的问题了。

而对于循环数组的问题，则可以按相同的思路进行优化。对于nums中的最小值，不妨设其下标为index，那么与其有关的划分要么让nums[index]作为划分的左边界，要么让nums[index]作为划分的右边界，也就是说让nums在index这个位置断开必然可以达成最优解，于是只需要考虑nums[index:] + nums[:index]以及nums[index + 1:] + nums[:index + 1]这两个非循环数组的最优划分的得分，取其中的较大值即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def maximumScore(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        p = 0
        n = len(nums)
        for index in range(1, n):
            if nums[index] < nums[p]:
                p = index
        
        def calc(nums):
            f = [None] * (k + 1)
            g = [None] * (k + 1)
            h = [None] * (k + 1)
            f[0] = 0
            for v in nums:
                for t in range(k, -1, -1):
                    if f[t] is not None:
                        if g[t] is None or g[t] < f[t] - v:
                            g[t] = f[t] - v
                        if h[t] is None or h[t] < f[t] + v:
                            h[t] = f[t] + v

                    if t > 0 and g[t - 1] is not None and (f[t] is None or f[t] < g[t - 1] + v):
                        f[t] = g[t - 1] + v
                    if t > 0 and h[t - 1] is not None and (f[t] is None or f[t] < h[t - 1] - v):
                        f[t] = h[t - 1] - v
            
            return max(f)

        nums1 = nums[p:] + nums[:p]
        nums2 = nums[p + 1:] + nums[:p + 1]
        return max(calc(nums1), calc(nums2))
```
