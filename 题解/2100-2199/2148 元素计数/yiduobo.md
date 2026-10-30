---
title: "2148. 元素计数"
aliases: ["yiduobo的每日leetcode 2148.元素计数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/530369631"
zhihu_id: "530369631"
zhihu_title: "yiduobo的每日leetcode 2148.元素计数"
question_id: "2148"
question: "元素计数"
problem_url: "https://leetcode.cn/problems/count-elements-with-strictly-smaller-and-greater-elements/"
difficulty: "Easy"
created: "2022-06-17T21:44:36+08:00"
updated: "2022-06-17T21:44:36+08:00"
upvotes: 0
comments: 0
---

# 2148. 元素计数

> **[yiduobo的每日leetcode 2148.元素计数](https://zhuanlan.zhihu.com/p/530369631) · 知乎 · 2022-06-17 · 赞同 0**
> 力扣：[2148. 元素计数](https://leetcode.cn/problems/count-elements-with-strictly-smaller-and-greater-elements/) · Easy · 灵茶山艾府：[O(n) 一次遍历](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2148.元素计数

[力扣](https://leetcode.cn/problems/count-elements-with-strictly-smaller-and-greater-elements/)

题目要求找出数组中同时具有至少一个严格较大值和至少一个严格较小值的元素个数，换言之就是问数组中不等于最大值和最小值的元素个数有多少，那么可以一趟遍历，找出数组中等于最大值和最小值的元素个数，然后用数组长度减去这两种数的个数即为最终答案。

另外需要注意一种特殊情况是数组中所有元素都一样，此时答案为0。

最后附上python代码：

```python
class Solution(object):
    def countElements(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        min_num = max_num = nums[0]
        min_cnt = max_cnt = 1
        for num in nums[1:]:
            if num < min_num:
                min_num = num
                min_cnt = 1
            elif num == min_num:
                min_cnt += 1
            
            if num > max_num:
                max_num = num
                max_cnt = 1
            elif num == max_num:
                max_cnt += 1
                
        if min_num == max_num:
            return 0
        else:
            return len(nums) - min_cnt - max_cnt
```
