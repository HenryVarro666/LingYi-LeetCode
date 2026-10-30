---
title: "45. 跳跃游戏II"
aliases: ["yiduobo的每日leetcode 45.跳跃游戏II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/贪心算法/二-区间贪心", "题单/LeetCode-热题-100/贪心算法", "题单/面试经典-150-题/数组-/-字符串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/125143085"
zhihu_id: "125143085"
zhihu_title: "yiduobo的每日leetcode 45.跳跃游戏II"
question_id: "45"
question: "跳跃游戏 II"
problem_url: "https://leetcode.cn/problems/jump-game-ii/"
difficulty: "Medium"
rating: 1700
created: "2020-04-04T23:00:56+08:00"
updated: "2020-04-04T23:00:56+08:00"
upvotes: 0
comments: 0
---

# 45. 跳跃游戏II

> **[yiduobo的每日leetcode 45.跳跃游戏II](https://zhuanlan.zhihu.com/p/125143085) · 知乎 · 2020-04-04 · 赞同 0**
> 力扣：[45. 跳跃游戏 II](https://leetcode.cn/problems/jump-game-ii/) · Medium · 灵茶山艾府：[【图解】一张图秒懂跳跃游戏！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

45.跳跃游戏II<https://leetcode-cn.com/problems/jump-game-ii/>

乍一看是动态规划的题目，仔细看确发现是贪心。

因为nums代表的是可以跳跃的最大长度，那么对于nums[k]，实际上下一步可以跳到的区域为k + 1到k + nums[k]。

不妨设这次起跳可以跳到位置i与位置j，其中i \< j，且i + nums[i] >\= j + nums[j]， 那么这一步应该跳到i，因为从j起跳能到的位置从i起跳都能到，反之则不一定。例如样例中的2，3，1，1，4，从位置0开始起跳，可以跳到位置1和位置2，有：

1 + nums[1] \= 1 + 3 \= 4，即从位置1起跳可以跳到位置2到位置4

2 + nums[2] \= 2 + 1 \= 3，即从位置2起跳可以跳到位置3

那么我们从位置0开始跳时，应该跳到位置1，因为从位置2开始跳的所有位置都能被位置1覆盖掉。可以得出，除非当前这一跳就能直接跳到结束位置，否则我们在每一步起跳时应该跳到下一步能跳得最远的那个位置。

具体实现时可以从头开始扫描，维护当前这次起跳的位置中，能够到的最右边界，然后逐步往后更新到尾部即可。总的时间复杂度为O(n)。

最后附上python代码：

```python
class Solution(object):
    def jump(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        right_bound = 0
        max_right_bound = 0
        res = 0

        for index in range(0, len(nums)):
            max_right_bound = max(max_right_bound, nums[index] + index)
            if index == right_bound:
                right_bound = max_right_bound
                if index != len(nums) - 1:
                    res += 1

        return res
```
