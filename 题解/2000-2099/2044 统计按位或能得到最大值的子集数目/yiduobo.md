---
title: "2044. 统计按位或能得到最大值的子集数目"
aliases: ["yiduobo的每日leetcode 2044.统计按位或能得到最大值的子集数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/backtracking", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/链表-二叉树与回溯/四-回溯", "题单/动态规划/九-状态压缩-DP-状压-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/510874596"
zhihu_id: "510874596"
zhihu_title: "yiduobo的每日leetcode 2044.统计按位或能得到最大值的子集数目"
question_id: "2044"
question: "统计按位或能得到最大值的子集数目"
problem_url: "https://leetcode.cn/problems/count-number-of-maximum-bitwise-or-subsets/"
difficulty: "Medium"
rating: 1568
created: "2022-05-07T19:17:29+08:00"
updated: "2022-05-07T19:17:29+08:00"
upvotes: 1
comments: 0
---

# 2044. 统计按位或能得到最大值的子集数目

> **[yiduobo的每日leetcode 2044.统计按位或能得到最大值的子集数目](https://zhuanlan.zhihu.com/p/510874596) · 知乎 · 2022-05-07 · 赞同 1**
> 力扣：[2044. 统计按位或能得到最大值的子集数目](https://leetcode.cn/problems/count-number-of-maximum-bitwise-or-subsets/) · Medium · 灵茶山艾府：[子集型回溯 + 剪枝（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2044.统计按位或能得到最大值的子集数目

[力扣](https://leetcode-cn.com/problems/count-number-of-maximum-bitwise-or-subsets/)

对于这类问题，通常的做法是从位的角度出发，设法通过动态规划或者贪心来求解。对于本题，状态压缩动态规划也是可行的，不过注意题目的数据范围，最多只有16个数，且数组最大值为10^5，二进制表示下有17位，那么在这里使用暴力dfs枚举每种组合反而比状态压缩动态规划更快一点。

具体实现上就是最常规不带任何剪枝的dfs，在这里就不展开了。

最后附上python代码：

```python
class Solution(object):
    def countMaxOrSubsets(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        self.max_num = 0
        self.res = 0
        self.dfs(0, 0, nums)

        return self.res

    def dfs(self, level, now, nums):
        if level == len(nums):
            if now > self.max_num:
                self.max_num = now
                self.res = 1
            elif now == self.max_num:
                self.res += 1
            return
        
        self.dfs(level + 1, now | nums[level], nums)
        self.dfs(level + 1, now, nums)
```
