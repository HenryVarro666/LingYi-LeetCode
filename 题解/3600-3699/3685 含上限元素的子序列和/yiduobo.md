---
title: "3685. 含上限元素的子序列和"
aliases: ["yiduobo的每日leetcode 3685.含上限元素的子序列和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/two-pointers", "leetcode/dynamic-programming", "leetcode/sorting", "题单/动态规划", "题单/动态规划/三-背包"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1953255519230861397"
zhihu_id: "1953255519230861397"
zhihu_title: "yiduobo的每日leetcode 3685.含上限元素的子序列和"
question_id: "3685"
question: "含上限元素的子序列和"
problem_url: "https://leetcode.cn/problems/subsequence-sum-after-capping-elements/"
difficulty: "Medium"
rating: 2073
created: "2025-09-27T01:28:55+08:00"
updated: "2025-09-27T01:28:57+08:00"
upvotes: 1
comments: 0
---

# 3685. 含上限元素的子序列和

> **[yiduobo的每日leetcode 3685.含上限元素的子序列和](https://zhuanlan.zhihu.com/p/1953255519230861397) · 知乎 · 2025-09-27 · 赞同 1**
> 力扣：[3685. 含上限元素的子序列和](https://leetcode.cn/problems/subsequence-sum-after-capping-elements/) · Medium · 灵茶山艾府：[0-1 背包 + 双指针，附 bitset 优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3685.含上限元素的子序列和

<https://leetcode.cn/problems/subsequence-sum-after-capping-elements/description/>

题目给出一个大小为n的整数数组nums，以及一个正整数k，数组的长度以及k的大小都不超过4000。

如果将nums中每个大于x的元素都替换为x，那么就可以得到一个由值x限制的数组。

现在要求对于1到n中的每个数x，确定能否有从x限制的数组中选出一个子序列，这个子序列中的元素之和恰好为k。返回一个下标从0开始的布尔数组answer，其大小为n，其中answer[x]为true，表示可以从x + 1限制的数组中选出满足要求的子序列，否则为false。

选出一个子序列使子序列之和等于k，是非常明显的背包问题，可以使用动态规划进行求解，因此一个直观的思路就是对于每种x，先计算限制后的数组，然后使用动态规划计算能否选出可用的子序列。这个算法的时间复杂度为O(n^2 \* k)，需要想办法进行优化。

注意到随着x的逐渐增大，相当于原始nums中被x卡住的元素重新被解禁了。如果在这里想将nums从小到大进行排序，那么随着x的增大，nums中可用的原始元素就是一个逐渐变成的前缀。更进一步的，如果只对这个前缀执行动态规划，那么对于每个x，都可以在x - 1的基础上，将恰好等于x - 1的元素解禁出来然后继续更新动态规划的数组。计算完成后，若当前被x限制的数组中有t个x，那么只需从k开始向下，逐个检测k、k - x、k - 2x、...、k - tx中是否有一个可以在动态规划中被达成就行了。

这样一来，动态规划的整体复杂度就变成了O(nk)，再加上排序以及枚举x的复杂度，最终的时间复杂度就是O(nk + klogn)，其中的O(klogn)是因为从k开始，以x \= 1向下枚举，一共k / 1次，当x \= 2时则为k / 2次，以此类推，也就是k + k / 2 + k / 3 + ... + k / n，这是经典的调和级数，时间复杂度为O(klogn)。

最后附上python代码：

```python
class Solution(object):
    def subsequenceSumAfterCapping(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[bool]
        """
        
        nums.sort()
        p = 0
        res = []
        f = [False] * (k + 1)
        f[0] = True
        for x in range(1, len(nums) + 1):
            q = p
            while q < len(nums) and nums[q] < x:
                q += 1
            
            for v in nums[p: q]:
                for index in range(k, v - 1, -1):
                    if f[index - v]:
                        f[index] = True
            p = q

            m = len(nums) - q
            v = k
            flag = False
            for index in range(m + 1):
                if f[v]:
                    flag = True
                    break
                v -= x
                if v < 0:
                    break

            res.append(flag)
        
        return res
```
