---
title: "2025. 分割数组的最多方案数"
aliases: ["yiduobo的每日leetcode 2025.分割数组的最多方案数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/enumeration", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/507469036"
zhihu_id: "507469036"
zhihu_title: "yiduobo的每日leetcode 2025.分割数组的最多方案数"
question_id: "2025"
question: "分割数组的最多方案数"
problem_url: "https://leetcode.cn/problems/maximum-number-of-ways-to-partition-an-array/"
difficulty: "Hard"
rating: 2218
created: "2022-04-29T22:06:21+08:00"
updated: "2022-04-29T22:06:21+08:00"
upvotes: 0
comments: 0
---

# 2025. 分割数组的最多方案数

> **[yiduobo的每日leetcode 2025.分割数组的最多方案数](https://zhuanlan.zhihu.com/p/507469036) · 知乎 · 2022-04-29 · 赞同 0**
> 力扣：[2025. 分割数组的最多方案数](https://leetcode.cn/problems/maximum-number-of-ways-to-partition-an-array/) · Hard · 灵茶山艾府：[前缀和+双哈希表+枚举修改元素](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2025.分割数组的最多方案数

[力扣](https://leetcode-cn.com/problems/maximum-number-of-ways-to-partition-an-array/)

首先不妨考虑最简单的情况，即不对任何数字进行替换。

对于这种情况，符合条件的pivot需要满足

nums[0] + nums[1] + ... + nums[pivot - 1] \= nums[pivot] + nums[pivot + 1] + ... + nums[n - 1]

注意到等号的左侧是一个前缀和的形式，又由于

nums[0] + nums[1] + ... + nums[n - 1] \= sum(nums)

那么实际上就是要找出所有的pivot，满足

s[pivot - 1] \= sum(nums) / 2

这里的s[pivot - 1]表示到pivot - 1为止的前缀和。当然，这里有一个隐藏条件就是sum(nums)必须为偶数，否则此时无解。

对于上面这个问题，一趟遍历，计算出前缀和s，判断其中sum(nums) / 2出现了多少次即可。

接下来考虑修改一个数字为k的情况的。

同样还是上面的前缀和与总和来进行求解。不妨设当前修改的是nums[index]，那么最终的总和就变成了sum(nums) - nums[index] + k，因此前缀和相应的目标就是target \= (sum(nums) - nums[index] + k) / 2。除此之外，前缀和本身也会发生变化。对于index - 1以及之前的所有位置，对应的前缀和都不会发生变化。而对于s[index]以及之后的s，则都会在原始s的基础上加上k - nums[index]。

综合上面的结论，此时的答案就是s[0]到s[index - 1]之间等于target的前缀和数目，再加上s[index]到s[-1]之间等于target - k + nums[index]的前缀和数目。

对于这个问题，则可以使用遍历每个index，并使用两个哈希表left和right，分别维护index - 1之前所有前缀和出现的次数，以及index之后所有原始前缀和出现的次数。

对于当前遍历到的index，首先将s[index]从left中移除，将其加入到right中，同时还需要更新此时的target。接下来从left中查找target出现的次数，从right中查找target - k + nums[index]出现的次数，并使用这两个次数之和来更新答案。

最后附上python代码：

```python
class Solution(object):
    def waysToPartition(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        s = [nums[0]]
        n = len(nums)
        for num in nums[1:]:
            s.append(s[-1] + num)
        
        left_cnt = {}
        for index in range(n - 1):
            left_cnt[s[index]] = left_cnt.get(s[index], 0) + 1
        
        if s[-1] % 2 == 0:
            res = left_cnt.get(s[-1] / 2, 0)
        else:
            res = 0
        
        if (s[-1] + k - nums[-1]) % 2 == 0:
            res = max(res, left_cnt.get((s[-1] + k - nums[-1]) / 2, 0))

        right_cnt = {}
        for index in range(n - 2, -1, -1):
            left_cnt[s[index]] -= 1
            right_cnt[s[index]] = right_cnt.get(s[index], 0) + 1
            delta = k - nums[index]

            if (s[-1] + delta) % 2 == 0:
                res = max(res, left_cnt.get((s[-1] + delta) / 2, 0) + right_cnt.get((s[-1] + delta) / 2 - delta, 0))
        
        return res
```
