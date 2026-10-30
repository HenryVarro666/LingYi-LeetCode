---
title: "3759. 统计合格元素的数目"
aliases: ["yiduobo的每日leetcode 3759.统计合格元素的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "leetcode/quickselect", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1978544750270375212"
zhihu_id: "1978544750270375212"
zhihu_title: "yiduobo的每日leetcode 3759.统计合格元素的数目"
question_id: "3759"
question: "统计合格元素的数目"
problem_url: "https://leetcode.cn/problems/count-elements-with-at-least-k-greater-values/"
difficulty: "Medium"
created: "2025-11-30T19:35:00+08:00"
updated: "2025-11-30T19:35:00+08:00"
upvotes: 2
comments: 0
---

# 3759. 统计合格元素的数目

> **[yiduobo的每日leetcode 3759.统计合格元素的数目](https://zhuanlan.zhihu.com/p/1978544750270375212) · 知乎 · 2025-11-30 · 赞同 2**
> 力扣：[3759. 统计合格元素的数目](https://leetcode.cn/problems/count-elements-with-at-least-k-greater-values/) · Medium · 灵茶山艾府：[排序+二分查找 / 快速选择（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3759.统计合格元素的数目

[3759. 统计合格元素的数目 - 力扣（LeetCode）](https://leetcode.cn/problems/count-elements-with-at-least-k-greater-values/description/)

题目给出一个长度为n的整数数组nums，以及一个整数k。

对于nums中的某个元素，若nums中存在至少k个元素严格大于它，那么这个元素就是合格元素。问nums中合格元素的总数。

题目实际上就是要从nums中排除掉前k大的元素，因此在这里可以先将nums按从大到小的顺序排序，接下来一趟遍历。

对于当前遍历到的nums[index]，若其严格小于上一个元素，那么就说明之前的nums[0]到nums[index - 1]这一共index个元素都严格大于nums[index]。若此时的index >\= k，那么从nums[index]开始的后续所有元素都是合格元素，那么答案就是len(nums) - index。反之，若index \< k，或者nums[index]与前一个元素相同，则需要继续向后遍历。

若遍历完都没找到符合条件的nums[index]，那么答案就为0。

```python
class Solution(object):
    def countElements(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        nums.sort(reverse=True)
        pre = nums[0] + 1
        for index, v in enumerate(nums):
            if v < pre:
                if index >= k:
                    return len(nums) - index
        
            pre = v

        return 0
```
