---
title: "3731. 找出缺失的元素"
aliases: ["yiduobo的每日leetcode 3731.找出缺失的元素"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/enumeration"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1968505745080316178"
zhihu_id: "1968505745080316178"
zhihu_title: "yiduobo的每日leetcode 3731.找出缺失的元素"
question_id: "3731"
question: "找出缺失的元素"
problem_url: "https://leetcode.cn/problems/find-missing-elements/"
difficulty: "Easy"
created: "2025-11-03T02:35:12+08:00"
updated: "2025-11-03T02:35:12+08:00"
upvotes: 2
comments: 4
---

# 3731. 找出缺失的元素

> **[yiduobo的每日leetcode 3731.找出缺失的元素](https://zhuanlan.zhihu.com/p/1968505745080316178) · 知乎 · 2025-11-03 · 赞同 2**
> 力扣：[3731. 找出缺失的元素](https://leetcode.cn/problems/find-missing-elements/) · Easy · 灵茶山艾府：[哈希集合（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3731.找出缺失的元素

[3731. 找出缺失的元素 - 力扣（LeetCode）](https://leetcode.cn/problems/find-missing-elements/description/)

题目给出一个整数数组nums，这个数组由互不相同的整数组成。

nums原本包含了某个范围内的所有整数，但是有些整数可能缺失了。

已知范围内的最小整数和最大整数依然存在于nums中，现在要求返回一个有序列表，其中包含范围内缺失的所有整数。若没有缺失，则返回空列表。

先取出nums中的最小值ma以及最大值ma，然后从mi + 1开始向后遍历，到ma - 1为止，检测目前遍历到的元素是否在nums中即可。

最后附上python代码：

```python
class Solution(object):
    def findMissingElements(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        
        num_set = set(nums)
        mi = min(nums)
        ma = max(nums)
        x = mi + 1
        res = []
        while x < ma:
            if x not in num_set:
                res.append(x)
            x += 1
        
        return res
```
