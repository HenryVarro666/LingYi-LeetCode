---
title: "3028. 边界上的蚂蚁"
aliases: ["yiduobo的每日leetcode 3028.边界上的蚂蚁"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/prefix-sum"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/695360296"
zhihu_id: "695360296"
zhihu_title: "yiduobo的每日leetcode 3028.边界上的蚂蚁"
question_id: "3028"
question: "边界上的蚂蚁"
problem_url: "https://leetcode.cn/problems/ant-on-the-boundary/"
difficulty: "Easy"
created: "2024-04-30T02:36:56+08:00"
updated: "2024-04-30T02:36:56+08:00"
upvotes: 1
comments: 0
---

# 3028. 边界上的蚂蚁

> **[yiduobo的每日leetcode 3028.边界上的蚂蚁](https://zhuanlan.zhihu.com/p/695360296) · 知乎 · 2024-04-30 · 赞同 1**
> 力扣：[3028. 边界上的蚂蚁](https://leetcode.cn/problems/ant-on-the-boundary/) · Easy · 灵茶山艾府：[统计前缀和中的 0 的个数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3028.边界上的蚂蚁

[. - 力扣（LeetCode）](https://leetcode.cn/problems/ant-on-the-boundary/description/)

由于只需要计算刚好停留在边界上的次数，那么只需一趟遍历，计算当前蚂蚁所处的位置并判断是否处于边界上就行了。

最后附上python代码：

```python
class Solution(object):
    def returnToBoundaryCount(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        s = 0
        res = 0
        for v in nums:
            s += v
            if s == 0:
                res += 1
        
        return res
```
