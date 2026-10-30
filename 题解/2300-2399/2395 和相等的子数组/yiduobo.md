---
title: "2395. 和相等的子数组"
aliases: ["yiduobo的每日leetcode 2395.和相等的子数组"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/566152123"
zhihu_id: "566152123"
zhihu_title: "yiduobo的每日leetcode 2395.和相等的子数组"
question_id: "2395"
question: "和相等的子数组"
problem_url: "https://leetcode.cn/problems/find-subarrays-with-equal-sum/"
difficulty: "Easy"
created: "2022-09-20T02:27:25+08:00"
updated: "2022-09-20T02:27:25+08:00"
upvotes: 0
comments: 0
---

# 2395. 和相等的子数组

> **[yiduobo的每日leetcode 2395.和相等的子数组](https://zhuanlan.zhihu.com/p/566152123) · 知乎 · 2022-09-20 · 赞同 0**
> 力扣：[2395. 和相等的子数组](https://leetcode.cn/problems/find-subarrays-with-equal-sum/) · Easy · 灵茶山艾府：[简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2395.和相等的子数组

[力扣](https://leetcode.cn/problems/find-subarrays-with-equal-sum/)

题目只需要找出长度为2的和相等的子数组，而长度为n的数组最多也就只有n - 1组长度为2的子数组，因此可以直接暴力枚举。

从下标1开始向后遍历，使用哈希表维护已经出现过的子数组和。对于当前元素，计算其与上一个元素之和。若这个和在哈希表中出现过，那么说明找到了一组解，否则就将这个和加入到哈希表中。若遍历完后依然没有出现重复，那么说明不存在要求的子数组。

最后附上python代码：

```python
class Solution(object):
    def findSubarrays(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        sum_set = set()
        for index in range(1, len(nums)):
            s = nums[index - 1] + nums[index]
            if s in sum_set:
                return True
            sum_set.add(s)
        
        return False
```
