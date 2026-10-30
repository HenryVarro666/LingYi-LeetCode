---
title: "2770. 达到末尾下标所需的最大跳跃次数"
aliases: ["yiduobo的每日leetcode 2770.达到末尾下标所需的最大跳跃次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/segment-tree", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/八-树状数组和线段树", "题单/动态规划/十一-优化-DP", "题单/动态规划/专题-跳跃游戏"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/655332129"
zhihu_id: "655332129"
zhihu_title: "yiduobo的每日leetcode 2770.达到末尾下标所需的最大跳跃次数"
question_id: "2770"
question: "达到末尾下标所需的最大跳跃次数"
problem_url: "https://leetcode.cn/problems/maximum-number-of-jumps-to-reach-the-last-index/"
difficulty: "Medium"
rating: 1533
created: "2023-09-09T23:55:11+08:00"
updated: "2023-09-09T23:55:11+08:00"
upvotes: 0
comments: 0
---

# 2770. 达到末尾下标所需的最大跳跃次数

> **[yiduobo的每日leetcode 2770.达到末尾下标所需的最大跳跃次数](https://zhuanlan.zhihu.com/p/655332129) · 知乎 · 2023-09-09 · 赞同 0**
> 力扣：[2770. 达到末尾下标所需的最大跳跃次数](https://leetcode.cn/problems/maximum-number-of-jumps-to-reach-the-last-index/) · Medium · 灵茶山艾府：[两种方法：普通 DP / 值域线段树优化 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2770.到达末尾下标所需的最大跳跃次数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximum-number-of-jumps-to-reach-the-last-index/description/)

经典的动态规划问题。令f[i]表示跳到位置i时的最大跳跃次数，那么对于f[i]，首先初始化f[i] \= -1，表示无法到达。接下来从0到i - 1枚举上一跳的终点j，若abs(nums[i] - nums[j]) \<\= target，那么就说明可以从j跳到i，因此就有f[i] \= max(f[i], f[j] + 1)。

全部计算完成后，f[-1]即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def maximumJumps(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """

        f = [0]
        for i in range(1, len(nums)):
            f.append(-1)
            for j in range(i):
                if f[j] != -1 and abs(nums[i] - nums[j]) <= target:
                    f[i] = max(f[i], f[j] + 1)
        
        return f[-1]
```
