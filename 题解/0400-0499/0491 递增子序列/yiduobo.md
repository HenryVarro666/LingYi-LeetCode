---
title: "491. 递增子序列"
aliases: ["yiduobo的每日leetcode 491.递增子序列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/253398551"
zhihu_id: "253398551"
zhihu_title: "yiduobo的每日leetcode 491.递增子序列"
question_id: "491"
question: "递增子序列"
problem_url: "https://leetcode.cn/problems/increasing-subsequences/"
created: "2020-09-18T23:34:10+08:00"
updated: "2020-09-18T23:34:10+08:00"
upvotes: 0
comments: 0
---

# 491. 递增子序列

> **[yiduobo的每日leetcode 491.递增子序列](https://zhuanlan.zhihu.com/p/253398551) · 知乎 · 2020-09-18 · 赞同 0**
> 力扣：[491. 递增子序列](https://leetcode.cn/problems/increasing-subsequences/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

491.递增子序列<https://leetcode-cn.com/problems/increasing-subsequences/>

依然是dfs的题目。

每一轮开始之前，先判断当前子序列的长度是否大于等于2，如果是，将当前子序列加入答案。接下来从当前子序列最后一个数字在原数组中位置的下一个位置开始进行枚举，若当前枚举的数字大于等于现有子序列的最后一个数字，且在这一轮的搜索中没有用过，那么就将其加入到现有子序列中并进行下一轮搜索。其中这一轮没有使用过这个判断的目的是为了去重。

最后附上python代码：

```python
class Solution(object):
    def findSubsequences(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """

        res = []
        used_set = set()
        for index, num in enumerate(nums):
            if num not in used_set:
                self.dfs(nums, index, [num], res)
                used_set.add(num)
        return res

    def dfs(self, nums, pos, now, res):
        if len(now) >= 2:
            res.append(now[:])

        used_set = set()
        for index in range(pos + 1, len(nums)):
            if nums[index] not in used_set and nums[index] >= now[-1]:
                self.dfs(nums, index, now + [nums[index]], res)
                used_set.add(nums[index])
```
