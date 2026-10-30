---
title: "55. 跳跃游戏"
aliases: ["yiduobo的每日leetcode 55.跳跃游戏"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/bian-li", "题单/贪心算法", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/贪心算法/二-区间贪心", "题单/LeetCode-热题-100/贪心算法", "题单/面试经典-150-题/数组-/-字符串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/127385066"
zhihu_id: "127385066"
zhihu_title: "yiduobo的每日leetcode 55.跳跃游戏"
question_id: "55"
question: "跳跃游戏"
problem_url: "https://leetcode.cn/problems/jump-game/"
difficulty: "Medium"
created: "2020-04-08T23:11:10+08:00"
updated: "2020-04-08T23:11:10+08:00"
upvotes: 0
comments: 0
---

# 55. 跳跃游戏

> **[yiduobo的每日leetcode 55.跳跃游戏](https://zhuanlan.zhihu.com/p/127385066) · 知乎 · 2020-04-08 · 赞同 0**
> 力扣：[55. 跳跃游戏](https://leetcode.cn/problems/jump-game/) · Medium · 灵茶山艾府：[两种理解方式：维护最右可达位置/合并区间（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

55.跳跃游戏<https://leetcode-cn.com/problems/jump-game/>

不是很懂leetcode题目的顺序是怎么排出来的，前面45题是这个55题的升级版（传送门在此[yiduobo：yiduobo的每日leetcode 45.跳跃游戏II](https://zhuanlan.zhihu.com/p/125143085)）

于是沿用45题的思路，从左往右开始，能跳多远就跳多远，直到跳到终点或者发现有位置跳不到为止。

最后附上python代码：

```python
class Solution(object):
    def canJump(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        if not nums:
            return False

        max_bound = 0
        for index, num in enumerate(nums):
            if index > max_bound:
                return False
            if index + nums[index] > max_bound:
                max_bound = index + nums[index]

        return True
```
