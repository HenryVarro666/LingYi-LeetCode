---
title: "2786. 访问数组中的位置使分数最大"
aliases: ["yiduobo的每日leetcode 2786.访问数组中的位置使分数最大"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/di-tui", "题单/动态规划", "题单/动态规划/六-状态机-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/656578287"
zhihu_id: "656578287"
zhihu_title: "yiduobo的每日leetcode 2786.访问数组中的位置使分数最大"
question_id: "2786"
question: "访问数组中的位置使分数最大"
problem_url: "https://leetcode.cn/problems/visit-array-positions-to-maximize-score/"
difficulty: "Medium"
rating: 1733
created: "2023-09-16T05:22:48+08:00"
updated: "2023-09-16T05:22:48+08:00"
upvotes: 1
comments: 0
---

# 2786. 访问数组中的位置使分数最大

> **[yiduobo的每日leetcode 2786.访问数组中的位置使分数最大](https://zhuanlan.zhihu.com/p/656578287) · 知乎 · 2023-09-16 · 赞同 1**
> 力扣：[2786. 访问数组中的位置使分数最大](https://leetcode.cn/problems/visit-array-positions-to-maximize-score/) · Medium · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推到空间优化！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2786.访问数组中的位置使分数最大

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/visit-array-positions-to-maximize-score/)

首先，注意到题目中数组的元素值都是正数，这也就意味对于数组中所有同奇偶的子数组，这些子数组要么全要，要么全都不要。因为对于这类子数组而言，如果选择了其中的某个数，那么将选择的方案改成选择这个子数组中的所有数并不会产生额外的惩罚，但是却可以将子数组中的其他数加入到答案中，显然是更优的。

基于这一点，就可以先通过一趟遍历，找出所有同奇偶的子数组，并将这些子数组收缩成子数组之和，得到一个奇数和偶数间隔出现的新数组merged_nums。

接下来，若这个merged_nums长度为1，说明原数组中所有数都同奇偶，那么直接返回原数组之和，也就是merged_nums[0]即可。否则，就需要尝试以奇数或偶数开头，执行动态规划。

动态规划的状态表示为f[i]和g[i]分别表示对于merged_nums中的前i + 1个数，以不同奇偶性结尾的选择方案所能得到的最大值。这里并不需要对奇数和偶数进行详细分类，只需使用一种和另一种来进行表达就行了。

首先初始化f[1]为merged_nums[0]，g[1]为merged_nums[1] + merged_nums[0] - x，理由是对于f[1]，有f[0] \= merged_nums[0]，但是merged_nums[1]是不可选的，因此f[1]也等于merged_nums[0]。而对于g[1]，则必须选merged_nums[1]，同时题目要求从0开始向后跳跃，也就意味着merged_nums[0]也要选，于是就有g[1] \= merged_nums[1] + merged_nums[0] - x。

接下来遍历i >\= 2的所有位置求解f[i]和g[i]。

若i是偶数，那么意味着当前merged_nums[i]的奇偶性与merged_nums[0]相同，因此在这里只能更新f，g[i]则只能沿用g[i - 1]。对于f[i]，则可以选择从之前的f[i - 1]或者g[i - 1]转移过来，于是就有f[i] \= max(f[i - 1] + merged_nums[i]，g[i - 1] + merged_nums[i] - x)

反过来，若i是奇数，则只能更新g，f[i]则沿用f[i - 1]。g的更新方法与f对称，也是分选不选上一个不同奇偶的元素，于是就有g[i] \= max(g[i - 1] + merged_nums[i], f[i - 1] + merged_nums[i] - x)

全部计算完成后，max(f[-1], g[-1])即为最终答案。

另外，注意到这里f和g每一轮都只和上一轮有关，因此可以使用变量迭代来省去数组。

最后附上python代码：

```python
class Solution(object):
    def maxScore(self, nums, x):
        """
        :type nums: List[int]
        :type x: int
        :rtype: int
        """

        merged_nums = []
        left = 0
        while left < len(nums):
            now = nums[left]
            right = left + 1
            while right < len(nums) and (nums[left] + nums[right]) % 2 == 0:
                now += nums[right]
                right += 1
            
            merged_nums.append(now)
            left = right
        
        if len(merged_nums) == 1:
            return merged_nums[0]
        
        a, b = merged_nums[0], merged_nums[0] + merged_nums[1] - x
        for index in range(2, len(merged_nums)):
            v = merged_nums[index]
            if index % 2 == 0:
                a, b = max(a + v, b + v - x), b
            else:
                a, b = a, max(a + v - x, b + v)

        return max(a, b)
```
