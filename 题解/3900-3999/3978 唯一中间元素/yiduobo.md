---
title: "3978. 唯一中间元素"
aliases: ["yiduobo的每日leetcode 3978.唯一中间元素"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2057145253526869700"
zhihu_id: "2057145253526869700"
zhihu_title: "yiduobo的每日leetcode 3978.唯一中间元素"
question_id: "3978"
question: "唯一中间元素"
problem_url: "https://leetcode.cn/problems/unique-middle-element/"
difficulty: "Easy"
created: "2026-07-05T16:56:35+08:00"
updated: "2026-07-05T16:56:35+08:00"
upvotes: 0
comments: 0
---

# 3978. 唯一中间元素

> **[yiduobo的每日leetcode 3978.唯一中间元素](https://zhuanlan.zhihu.com/p/2057145253526869700) · 知乎 · 2026-07-05 · 赞同 0**
> 力扣：[3978. 唯一中间元素](https://leetcode.cn/problems/unique-middle-element/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3978.唯一中间元素

<https://leetcode.cn/problems/unique-middle-element/description/>

题目给出一个长度为奇数n的整数数组nums。

若nums的下标中间元素在数组中恰好出现一次，则返回true，否则返回false。

中间元素恰好出现一次，就意味着除了正中间这个位置，其他位置上的元素都和这个中间元素不同。于是只需要一趟遍历，对于当前遍历到的元素，若其不处于正中间，且元素值等于中间元素，则返回false。若成功遍历完成，则返回true。

最后附上python代码：

```python
class Solution(object):
    def isMiddleElementUnique(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        
        m = len(nums) // 2
        for index, v in enumerate(nums):
            if v == nums[m] and index != m:
                return False
        
        return True
```
