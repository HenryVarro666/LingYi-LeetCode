---
title: "2089. 找出数组排序后的目标下标"
aliases: ["yiduobo的每日leetcode 2089.找出数组排序后的目标下标"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/519382994"
zhihu_id: "519382994"
zhihu_title: "yiduobo的每日leetcode 2089.找出数组排序后的目标下标"
question_id: "2089"
question: "找出数组排序后的目标下标"
problem_url: "https://leetcode.cn/problems/find-target-indices-after-sorting-array/"
difficulty: "Easy"
created: "2022-05-24T20:55:40+08:00"
updated: "2022-05-24T20:55:40+08:00"
upvotes: 0
comments: 0
---

# 2089. 找出数组排序后的目标下标

> **[yiduobo的每日leetcode 2089.找出数组排序后的目标下标](https://zhuanlan.zhihu.com/p/519382994) · 知乎 · 2022-05-24 · 赞同 0**
> 力扣：[2089. 找出数组排序后的目标下标](https://leetcode.cn/problems/find-target-indices-after-sorting-array/) · Easy · 灵茶山艾府：[O(n) 做法：统计小于和等于 target 的元素个数](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2089.找出数组排序后的目标下标

[力扣](https://leetcode.cn/problems/find-target-indices-after-sorting-array/)

比较基础的题目。按题目要求将数组排序，然后一趟遍历找到所有等于target的下标即可。

最后附上python代码：

```python
class Solution(object):
    def targetIndices(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """

        res = []
        for index, num in enumerate(sorted(nums)):
            if num == target:
                res.append(index)
        
        return res
```
