---
title: "2784. 检查数组是否是好的"
aliases: ["yiduobo的每日leetcode 2784.检查数组是否是好的"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/656363008"
zhihu_id: "656363008"
zhihu_title: "yiduobo的每日leetcode 2784.检查数组是否是好的"
question_id: "2784"
question: "检查数组是否是好的"
problem_url: "https://leetcode.cn/problems/check-if-array-is-good/"
difficulty: "Easy"
created: "2023-09-15T04:08:52+08:00"
updated: "2023-09-15T04:08:52+08:00"
upvotes: 0
comments: 0
---

# 2784. 检查数组是否是好的

> **[yiduobo的每日leetcode 2784.检查数组是否是好的](https://zhuanlan.zhihu.com/p/656363008) · 知乎 · 2023-09-15 · 赞同 0**
> 力扣：[2784. 检查数组是否是好的](https://leetcode.cn/problems/check-if-array-is-good/) · Easy · 灵茶山艾府：[两种方法：辅助数组 / O(1) 空间（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2784.检查数组是否是好的

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/check-if-array-is-good/description/)

使用集合为数组去重，同时记录下数组中的最小值和最大值。

若存在最小值小于1、最大值大于数组长度减1、集合中出现元素的个数不等于数组长度减1、除了数组长度减1之外的数出现了多次这四种情况之一，那么就说明数组不是好数组。

最后附上python代码：

```python
class Solution(object):
    def isGood(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        if len(nums) == 1:
            return False

        vis = set()
        max_v = len(nums) - 1
        for v in nums:
            if v < 1 or v > max_v:
                return False
            if v in vis and v != max_v:
                return False
            vis.add(v)
        
        return len(vis) == max_v
```
