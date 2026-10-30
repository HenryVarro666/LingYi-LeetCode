---
title: "3837. 相等元素的延迟计数"
aliases: ["yiduobo的每日leetcode 3837.相等元素的延迟计数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2010123890790254098"
zhihu_id: "2010123890790254098"
zhihu_title: "yiduobo的每日leetcode 3837.相等元素的延迟计数"
question_id: "3837"
question: "相等元素的延迟计数"
problem_url: "https://leetcode.cn/problems/delayed-count-of-equal-elements/"
created: "2026-02-25T22:55:54+08:00"
updated: "2026-02-25T22:55:55+08:00"
upvotes: 2
comments: 0
---

# 3837. 相等元素的延迟计数

> **[yiduobo的每日leetcode 3837.相等元素的延迟计数](https://zhuanlan.zhihu.com/p/2010123890790254098) · 知乎 · 2026-02-25 · 赞同 2**
> 力扣：[3837. 相等元素的延迟计数](https://leetcode.cn/problems/delayed-count-of-equal-elements/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3837.相等元素的延迟计数

<https://leetcode.cn/problems/delayed-count-of-equal-elements/description/>

题目给出一个长度为n的整数数组nums以及一个整数k。

要求对于0到n - 1之间的每个下标index，要求找出所有下标严格大于index + k的元素中，恰好等于nums[index]的元素数目。

可以发现，题目实际上是要对每个下标，都计算一个特定的后缀中恰好等于当前下标元素的元素数目。

随着需要计算的下标向前移动，其对应的后缀起点也跟着向前移动，于是可以从后往前一趟遍历，使用一个下标p记录当前下标对应的特定后缀的起点位置，另外使用一个哈希表freq记录从p开始的后缀中每种元素出现的次数。对于当前遍历到的下标index，先根据index更新p，在p移动时同步更新freq，然后利用freq查找后缀中等于nums[index]的元素数目即可。

最后附上python代码：

```python
class Solution(object):
    def delayedCount(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        
        freq = {}
        n = len(nums)
        res = [0] * n
        
        p = n - 1
        for index in range(n - 1, -1, -1):
            while p > index + k:
                freq[nums[p]] = freq.get(nums[p], 0) + 1
                p -= 1
            
            res[index] = freq.get(nums[index], 0)
        
        return res
```
