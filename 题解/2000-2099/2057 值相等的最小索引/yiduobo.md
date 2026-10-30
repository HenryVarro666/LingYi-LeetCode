---
title: "2057. 值相等的最小索引"
aliases: ["yiduobo的每日leetcode 2057.值相等的最小索引"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/513562335"
zhihu_id: "513562335"
zhihu_title: "yiduobo的每日leetcode 2057.值相等的最小索引"
question_id: "2057"
question: "值相等的最小索引"
problem_url: "https://leetcode.cn/problems/smallest-index-with-equal-value/"
difficulty: "Easy"
created: "2022-05-12T23:41:56+08:00"
updated: "2022-05-12T23:41:56+08:00"
upvotes: 0
comments: 0
---

# 2057. 值相等的最小索引

> **[yiduobo的每日leetcode 2057.值相等的最小索引](https://zhuanlan.zhihu.com/p/513562335) · 知乎 · 2022-05-12 · 赞同 0**
> 力扣：[2057. 值相等的最小索引](https://leetcode.cn/problems/smallest-index-with-equal-value/) · Easy · 灵茶山艾府：[Go 模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2057.值相等的最小索引

[力扣](https://leetcode.cn/problems/smallest-index-with-equal-value/)

比较基础的题目，只需一趟遍历，检测当前下标index是否满足index % 10 \= nums[index]，若等于，那么答案就是index。若遍历完整个数组都没找到合法的index，那么答案就是-1。

最后附上python代码：

```python
class Solution(object):
    def smallestEqual(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        for index in range(len(nums)):
            if index % 10 == nums[index]:
                return index
        
        return -1
```
