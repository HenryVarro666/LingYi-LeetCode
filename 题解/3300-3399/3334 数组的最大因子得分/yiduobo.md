---
title: "3334. 数组的最大因子得分"
aliases: ["yiduobo的每日leetcode 3334.数组的最大因子得分"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "题单/动态规划", "题单/数学算法", "题单/动态规划/专题-前后缀分解", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/24929051195"
zhihu_id: "24929051195"
zhihu_title: "yiduobo的每日leetcode 3334.数组的最大因子得分"
question_id: "3334"
question: "数组的最大因子得分"
problem_url: "https://leetcode.cn/problems/find-the-maximum-factor-score-of-array/"
difficulty: "Medium"
rating: 1519
created: "2025-02-20T00:38:38+08:00"
updated: "2025-02-20T00:38:38+08:00"
upvotes: 1
comments: 0
---

# 3334. 数组的最大因子得分

> **[yiduobo的每日leetcode 3334.数组的最大因子得分](https://zhuanlan.zhihu.com/p/24929051195) · 知乎 · 2025-02-20 · 赞同 1**
> 力扣：[3334. 数组的最大因子得分](https://leetcode.cn/problems/find-the-maximum-factor-score-of-array/) · Medium · 灵茶山艾府：[非暴力做法：前后缀分解（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3334.数组的最大因子得分

[3334. 数组的最大因子得分 - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-maximum-factor-score-of-array/description/)

题目给出一个整数数组nums，接下来定义因子得分为数组所有元素的最小公倍数与最大公约数的乘积，若数组为空数组，那么因子得分为0。在最多移除一个元素的情况下，返回nums的最大因子得分。

由于题目的数据规模比较小，因此可以先计算不移除任意元素时的因子得分，接下来再一趟遍历，枚举移除掉的元素，对于剩下的子数组计算因子得分并更新答案。

计算因子得分的方式也比较简单，若数组为空，则得分为0，若不为空，则初始化最小公倍数与最大公约数都为数组的首个元素，接下来一趟遍历，使用当前遍历到的元素更新最小公倍数以及最大公约数即可。

最后附上python代码：

```python
class Solution(object):
    def maxScore(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x

        def calc(nums):
            if not nums:
                return 0
            
            g = nums[0]
            l = nums[0]
            for v in nums[1:]:
                g = gcd(g, v)
                l = l // gcd(l, v) * v
            
            return g * l
        
        res = calc(nums)
        for index in range(len(nums)):
            res = max(res, calc(nums[:index] + nums[index + 1:]))
        
        return res
```
