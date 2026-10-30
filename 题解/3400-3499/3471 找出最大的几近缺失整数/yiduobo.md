---
title: "3471. 找出最大的几近缺失整数"
aliases: ["yiduobo的每日leetcode 3471.找出最大的几近缺失整数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1896747970038318592"
zhihu_id: "1896747970038318592"
zhihu_title: "yiduobo的每日leetcode 3471.找出最大的几近缺失整数"
question_id: "3471"
question: "找出最大的几近缺失整数"
problem_url: "https://leetcode.cn/problems/find-the-largest-almost-missing-integer/"
difficulty: "Easy"
created: "2025-04-19T02:22:22+08:00"
updated: "2025-04-19T02:22:22+08:00"
upvotes: 0
comments: 0
---

# 3471. 找出最大的几近缺失整数

> **[yiduobo的每日leetcode 3471.找出最大的几近缺失整数](https://zhuanlan.zhihu.com/p/1896747970038318592) · 知乎 · 2025-04-19 · 赞同 0**
> 力扣：[3471. 找出最大的几近缺失整数](https://leetcode.cn/problems/find-the-largest-almost-missing-integer/) · Easy · 灵茶山艾府：[O(n) 做法，脑筋急转弯（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3471.找出最大的几近缺失整数

[3471. 找出最大的几近缺失整数 - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-largest-almost-missing-integer/description/)

题目给出一个整数数组nums以及一个整数k，k的取值范围在1到nums的长度之间。若某个整数x恰好仅出现在nums的一个大小为k的子数组中，则认为x是nums中几近缺失整数。

问nums中最大的几近缺失整数是什么，若不存在，则返回-1。

当k等于nums的长度len(nums)时，nums中只有一个大小为k的子数组，也就是nums自身，那么nums中的所有元素都仅出现在nums的一个大小为k的子数组中，因此其中的最大值，也就是max(nums)即为最终答案。

当k等于1时，nums中的每个元素都将单独形成一个大小为k的子数组。为了保证最终答案仅在nums的一个大小为1的子数组中出现，那么其在nums中出现的次数必须是恰好1次。于是可以一趟遍历，统计每种元素在nums中出现的次数，其中仅出现1次的元素的最大值即为最终答案。若不存在仅出现1次的元素，答案就为-1。

最后，当k的值在2到len(nums) - 1之间时，除了nums[0]以及nums[-1]这两个元素之外，其他所有元素都至少出现在两个子数组中，因此这些元素都不可能是最终答案。于是只需检测nums[0]以及nums[-1]是否在nums中仅出现1次，若满足，则使用nums[0]或者nums[-1]来更新答案。

最后附上python代码：

```python
class Solution(object):
    def largestInteger(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        if k == len(nums):
            return max(nums)

        cnt = Counter(nums)
        if k == 1:
            res = -1
            for v in cnt:
                if cnt[v] == 1:
                    res = max(res, v)
            return res
        
        res = -1
        if cnt[nums[0]] == 1:
            res = max(res, nums[0])
        if cnt[nums[-1]] == 1:
            res = max(res, nums[-1])
        return res
```
