---
title: "3232. 判断是否可以赢得数字游戏"
aliases: ["yiduobo的每日leetcode 3232.判断是否可以赢得数字游戏"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/720351872"
zhihu_id: "720351872"
zhihu_title: "yiduobo的每日leetcode 3232.判断是否可以赢得数字游戏"
question_id: "3232"
question: "判断是否可以赢得数字游戏"
problem_url: "https://leetcode.cn/problems/find-if-digit-game-can-be-won/"
difficulty: "Easy"
created: "2024-09-15T21:58:12+08:00"
updated: "2024-09-15T21:58:27+08:00"
upvotes: 0
comments: 0
---

# 3232. 判断是否可以赢得数字游戏

> **[yiduobo的每日leetcode 3232.判断是否可以赢得数字游戏](https://zhuanlan.zhihu.com/p/720351872) · 知乎 · 2024-09-15 · 赞同 0**
> 力扣：[3232. 判断是否可以赢得数字游戏](https://leetcode.cn/problems/find-if-digit-game-can-be-won/) · Easy · 灵茶山艾府：[简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3232.判断是否可以赢得数字游戏

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-if-digit-game-can-be-won/description/)

题目给出一个数组元素大小在1到99之间的数组nums，现在alice可以从中所有的个位数或者两位数，其他的数字归bob所有。若alice所选数字之和严格大于bob的数字之和，那么alice获胜，否则bob获胜。问alice是否能赢。

由于alice可以自由选择，那么当个位数之和更大时，alice可以选择个位数，而两位数之和更大时，alice则可以选择两位数，也就是说alice只输一手个位数之和恰好等于两位数之和。

于是只需一趟遍历，分别计算个位数之和与两位数之和，若二者相等，则bob赢，否则alice赢。

最后附上python代码：

```python
class Solution(object):
    def canAliceWin(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        x = y = 0
        for v in nums:
            if v < 10:
                x += v
            else:
                y += v
        
        return x != y
```
