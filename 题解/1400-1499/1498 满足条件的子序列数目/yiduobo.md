---
title: "1498. 满足条件的子序列数目"
aliases: ["yiduobo的每日leetcode 1498.满足条件的子序列数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/sorting", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/416796738"
zhihu_id: "416796738"
zhihu_title: "yiduobo的每日leetcode 1498.满足条件的子序列数目"
question_id: "1498"
question: "满足条件的子序列数目"
problem_url: "https://leetcode.cn/problems/number-of-subsequences-that-satisfy-the-given-sum-condition/"
difficulty: "Medium"
rating: 2276
created: "2021-10-06T21:30:39+08:00"
updated: "2021-10-06T21:30:39+08:00"
upvotes: 0
comments: 0
---

# 1498. 满足条件的子序列数目

> **[yiduobo的每日leetcode 1498.满足条件的子序列数目](https://zhuanlan.zhihu.com/p/416796738) · 知乎 · 2021-10-06 · 赞同 0**
> 力扣：[1498. 满足条件的子序列数目](https://leetcode.cn/problems/number-of-subsequences-that-satisfy-the-given-sum-condition/) · Medium · 灵茶山艾府：[排序+相向双指针（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1498.满足条件的子序列数目

[力扣](https://leetcode-cn.com/problems/number-of-subsequences-that-satisfy-the-given-sum-condition/)

题目要找的是子序列，同时又对子序列中的最大值和最小值颇为关心，那么一个自然的想法就是将整个数组排序之后，使用双指针来确定当前满足条件的子序列数目。

那么先将数组从小到大进行排序，然后从左向右枚举区间右边界r。

首先，若当前nums[r] + nums[r] \<\= target，那么说明以r为右边界，以0到r中任意位置为左边界的子序列都是满足题目要求的。

当r等于0时，这种子序列只有一个，即nums[0]这一个数。

当r等于1时，nums[1]必选，而nums[0]可选可不选，因此有两个符合条件的子序列。

更进一步的，对于任意满足nums[r] + nums[r] \<\= target的r而言，除了nums[r]必选之外，其他的nums[0]到nums[r - 1]共r个数都是可选可不选的，因此这里一共就有2^r种合法的子序列。

接下来，随着r的向后移动，可能出现某一时刻nums[r] + nums[r] > target的情况。此时首先需要确定子序列的最大左边界l的位置。初始情况下，l应该从r - 1开始向左扫描，找到第一个满足nums[l] + nums[r] \<\= target的位置l。往后的每一轮，随着r的向后移动，nums[r]都是单调不减的，因此nums[l]必须保持单调不增，因此往后每一轮的l都只需在上一轮l的基础上向左移动即可。

若某一时刻l移出了边界，说明此时已经找不到一个合法的左边界，那么就无须考察后续的r，直接返回答案即可。

若成功找到了左边界l，那么在确定了子序列右边界为r的情况下，考察左边界为l的合法子序列的数目。此时nums[l]以及nums[r]必选，而l + 1到r - 1之间的这些数都是可选可不选的，一共为r - l - 1个数，因此可以形成2^(r - l - 1)种合法的子序列。

更一般的情况，对于左边界为p的情况，此时的方案数应该是2^(r - p - 1)，而这里p的取值为0到l，于是选择r作为右边界的所有合法子序列的数目就是

2^(r - l - 1) + 2^(r - l) + 2^(r - l + 1) + ... + 2^(r - 1)

将2^(r - l - 1)提出来，就有

2^(r - l - 1) \* (1 + 2 + 4 + ... + 2^l) \= 2^(r - l - 1) \* (2^(l + 1) - 1) \= 2^r - 2^(r - l - 1)

可以发现，无论哪种情况，答案都与2的幂次有关。那么可以先预处理出2的所有幂次，然后再使用上面的双指针法进行求解。

最后附上python代码：

```python
class Solution(object):
    def numSubseq(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """

        n = len(nums)
        mod = 10 ** 9 + 7

        pow2 = [1]
        for index in range(1, n + 1):
            pow2.append(pow2[-1] + pow2[-1])
            if pow2[-1] >= mod:
                pow2[-1] -= mod

        nums = sorted(nums)
        res = 0
        r = 0
        while r < n:
            if nums[r] + nums[r] > target:
                break
            
            res += pow2[r]
            if res >= mod:
                res -= mod
        
            r += 1

        l = r - 1
        while r < n:
            while l >= 0 and nums[l] + nums[r] > target:
                l -= 1
            if l < 0:
                return res
            
            res += pow2[r]
            if res >= mod:
                res -= mod
            res -= pow2[r - l - 1]
            if res < 0:
                res += mod
        
            r += 1

        return res
```
