---
title: "2210. 统计数组中峰和谷的数量"
aliases: ["yiduobo的每日leetcode 2210.统计数组中峰和谷的数量"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/540433236"
zhihu_id: "540433236"
zhihu_title: "yiduobo的每日leetcode 2210.统计数组中峰和谷的数量"
question_id: "2210"
question: "统计数组中峰和谷的数量"
problem_url: "https://leetcode.cn/problems/count-hills-and-valleys-in-an-array/"
difficulty: "Easy"
created: "2022-07-11T23:49:21+08:00"
updated: "2022-07-11T23:49:21+08:00"
upvotes: 0
comments: 0
---

# 2210. 统计数组中峰和谷的数量

> **[yiduobo的每日leetcode 2210.统计数组中峰和谷的数量](https://zhuanlan.zhihu.com/p/540433236) · 知乎 · 2022-07-11 · 赞同 0**
> 力扣：[2210. 统计数组中峰和谷的数量](https://leetcode.cn/problems/count-hills-and-valleys-in-an-array/) · Easy · 灵茶山艾府：[两种方法：去重 / 状态机，四种写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2210.统计数组中峰和谷的数量

[力扣](https://leetcode.cn/problems/count-hills-and-valleys-in-an-array/)

题目中的峰和谷只涉及到相邻的位置，因此不需要什么复杂的处理，直接一趟遍历就行了。需要注意的是，相同值将被算成同一个峰或者谷，因此在判断时如果出现了相同值，应该只利用最外侧的两个值进行峰和谷的判断，略过中部的相同值。

最后附上python代码：

```python
class Solution(object):
    def countHillValley(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0
        last = nums[0]
        for index in range(1, len(nums) - 1):
            if nums[index] == last or nums[index] == nums[index + 1]:
                continue
            if (last < nums[index] and nums[index] > nums[index + 1]) or (last > nums[index] and nums[index] < nums[index + 1]):
                res += 1
            
            last = nums[index]
                
        
        return res
```
