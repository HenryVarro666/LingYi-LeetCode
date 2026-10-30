---
title: "3397. 执行操作后不同元素的最大数量"
aliases: ["yiduobo的每日leetcode 3397.执行操作后不同元素的最大数量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/30647282645"
zhihu_id: "30647282645"
zhihu_title: "yiduobo的每日leetcode 3397.执行操作后不同元素的最大数量"
question_id: "3397"
question: "执行操作后不同元素的最大数量"
problem_url: "https://leetcode.cn/problems/maximum-number-of-distinct-elements-after-operations/"
difficulty: "Medium"
rating: 1687
created: "2025-03-16T22:31:42+08:00"
updated: "2025-03-16T22:31:42+08:00"
upvotes: 0
comments: 0
---

# 3397. 执行操作后不同元素的最大数量

> **[yiduobo的每日leetcode 3397.执行操作后不同元素的最大数量](https://zhuanlan.zhihu.com/p/30647282645) · 知乎 · 2025-03-16 · 赞同 0**
> 力扣：[3397. 执行操作后不同元素的最大数量](https://leetcode.cn/problems/maximum-number-of-distinct-elements-after-operations/) · Medium · 灵茶山艾府：[从小到大贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3397.执行操作后不同元素的最大数量

[3397. 执行操作后不同元素的最大数量 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-number-of-distinct-elements-after-operations/description/)

题目给出一个整数数组nums以及一个非负整数k，对于nums中的每个元素，最多可以执行一次以下操作：将一个在大小在-k到k之间的整数累加到该元素上。问执行操作后，nums中可能拥有的不同元素的最大数量是多少。

题目要求不同元素的数量最多，那么不妨从边界情况开始考虑。

对于nums中的最小值first，很明显应该让first减去k，这样一来留给其他元素的操作空间会更大。另一方面，由于nums中剩余的元素都大于等于first，因此构造出来的元素值也必然大于等于first - k，也就是说下一个元素最理想的构造值target为first - k + 1。

接下来对于次小值second，其目标构造值为target \= first - k + 1，那么second与target的大小关系就有三种可能性：

1、second \< target - k：

这种情况下second无法达成target，也无法进行构造，因为可用的目标值都已经被用完了，因此只能跳过second

2、target - k \<\= second \<\= target + k：

这种情况下可以将second变为target，那么将变为target后，下一个值的目标就应该是target + 1。

对于这种情况，应该将答案和target都加上1。

3、target + k \< second：

这种情况下second最多变为second - k，虽然不及预期，但是second - k目前是没人用过的，因此可以将second变为second - k。另一方面，由于后续元素都大于等于second，因此后续元素操作后的结果也必然大于等于second - k，因此下一个值的目标就应该是second - k + 1。

对于这种情况，应该将答案加上1，然后将target变为second - k + 1。

以上的过程可以直接向后推广，具体来说，就是已经对nums中最小的前index个数进行操作后，若此时的目标值为target，那么对于剩余元素中的最小值，也就是nums中第index + 1小的值v，只需按照上面的描述对比v和target的大小关系，然后更新target以及答案即可。

于是只需对nums从小到大排序，然后初始化target为nums[0] - k + 1，并初始化答案为1，然后从下标1开始向后遍历，根据当前遍历到的v与target的大小关系更新target以及答案就行了。

最后附上python代码：

```python
class Solution(object):
    def maxDistinctElements(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        nums.sort()
        res = 1
        target = nums[0] - k + 1
        for v in nums[1:]:
            if abs(v - target) <= k:
                target += 1
                res += 1
            elif v > target:
                target = v - k + 1
                res += 1
        
        return res
```
