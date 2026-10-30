---
title: "1848. 到目标元素的最小距离"
aliases: ["yiduobo的每日leetcode 1848.到目标元素的最小距离"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/470517564"
zhihu_id: "470517564"
zhihu_title: "yiduobo的每日leetcode 1848.到目标元素的最小距离"
question_id: "1848"
question: "到目标元素的最小距离"
problem_url: "https://leetcode.cn/problems/minimum-distance-to-the-target-element/"
difficulty: "Easy"
created: "2022-02-22T00:45:31+08:00"
updated: "2022-02-22T00:45:31+08:00"
upvotes: 0
comments: 0
---

# 1848. 到目标元素的最小距离

> **[yiduobo的每日leetcode 1848.到目标元素的最小距离](https://zhuanlan.zhihu.com/p/470517564) · 知乎 · 2022-02-22 · 赞同 0**
> 力扣：[1848. 到目标元素的最小距离](https://leetcode.cn/problems/minimum-distance-to-the-target-element/) · Easy · 灵茶山艾府：[两种方法：从左到右遍历 / 从 start 往两侧遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1848.到目标元素的最小距离

[力扣](https://leetcode-cn.com/problems/minimum-distance-to-the-target-element/)

题目要求找出距离start最近且等于target的数在数组中的下标，那么一个自然的想法就是从start开始向左右两侧扫描，找到第一个target时停止，然后对比左右两侧当前位置与start的距离大小决定最终答案。

最后附上python代码：

```python
class Solution(object):
    def getMinDistance(self, nums, target, start):
        """
        :type nums: List[int]
        :type target: int
        :type start: int
        :rtype: int
        """

        now = start
        while now >= 0 and nums[now] != target:
            now -= 1
        
        if now >= 0:
            res = start - now
        else:
            res = len(nums) + 1
        
        now = start + 1
        while now < len(nums) and nums[now] != target:
            now += 1
        
        if now < len(nums):
            res = min(res, now - start)
        
        return res
```
