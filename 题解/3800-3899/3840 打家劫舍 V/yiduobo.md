---
title: "3840. 打家劫舍V"
aliases: ["yiduobo的每日leetcode 3840.打家劫舍V"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/一-入门-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2010132142882054967"
zhihu_id: "2010132142882054967"
zhihu_title: "yiduobo的每日leetcode 3840.打家劫舍V"
question_id: "3840"
question: "打家劫舍 V"
problem_url: "https://leetcode.cn/problems/house-robber-v/"
difficulty: "Medium"
rating: 1619
created: "2026-02-26T21:56:43+08:00"
updated: "2026-02-26T21:56:44+08:00"
upvotes: 1
comments: 0
---

# 3840. 打家劫舍V

> **[yiduobo的每日leetcode 3840.打家劫舍V](https://zhuanlan.zhihu.com/p/2010132142882054967) · 知乎 · 2026-02-26 · 赞同 1**
> 力扣：[3840. 打家劫舍 V](https://leetcode.cn/problems/house-robber-v/) · Medium · 灵茶山艾府：[在 198 题的基础上添加颜色判断（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3840.打家劫舍V

<https://leetcode.cn/problems/house-robber-v/>

题目给出两个长度为n的整数数组nums以及colors，其中nums[index]和colors[index]分别表示第index间房屋中的金额，以及这间房屋的颜色代码。

若两间相邻的房屋具有相同的颜色代码，则不能同时偷窃它们。

问最大可以偷窃到的金额。

经典的动态规划问题的改版，做法也大差不差。令f[index]表示对于第0到第index间房屋，偷窃了第index间房屋的最大收益，而g[index]则表示不偷窃第index间房屋的最大收益，那么对于f[index]与g[index]：

1、首先是边界情况。当index \= 0时，有

f[index] \= nums[0]

g[index] \= 0

2、接下来对于一般情况：

2-1）若colors[index]与colors[index - 1]相同，那么就不能同时偷窃index与index - 1

对于f[index]，根据f的定义，需要偷窃index，因此不能偷窃index - 1，也就是说此时的f[index]只能通过g[index - 1] + nums[index]得到

对于g[index]则没有影响，index - 1可偷可不偷，于是有g[index] \= max(f[index - 1], g[index - 1])

2-2）若colors[index]与colors[index - 1]不同，那么可以同时偷窃index与index - 1。

对于f[index]，此时就不受限制了，即f[index] \= max(f[index - 1], g[index - 1]) + nums[index]

对于g[index]则保持不变，有g[index] \= max(f[index - 1], g[index - 1])

计算完成后，max(f[-1], g[-1])即为最终答案。

另外注意到f和g都只与上一轮的f和g有关，因此可以使用变量迭代省去数组的开销。

最后附上python代码：

```python
class Solution(object):
    def rob(self, nums, colors):
        """
        :type nums: List[int]
        :type colors: List[int]
        :rtype: int
        """
        
        f, g = nums[0], 0
        for index in range(1, len(nums)):
            if colors[index] != colors[index - 1]:
                f, g = max(f, g) + nums[index], max(f, g)
            else:
                f, g = g + nums[index], max(f, g)
        
        return max(f, g)
```
