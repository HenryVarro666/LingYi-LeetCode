---
title: "2221. 数组的三角和"
aliases: ["yiduobo的每日leetcode 2221.数组的三角和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/combinatorics", "leetcode/number-theory", "leetcode/simulation", "题单/数学算法", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/542196418"
zhihu_id: "542196418"
zhihu_title: "yiduobo的每日leetcode 2221.数组的三角和"
question_id: "2221"
question: "数组的三角和"
problem_url: "https://leetcode.cn/problems/find-triangular-sum-of-an-array/"
difficulty: "Medium"
created: "2022-07-15T23:55:40+08:00"
updated: "2022-07-15T23:55:40+08:00"
upvotes: 0
comments: 0
---

# 2221. 数组的三角和

> **[yiduobo的每日leetcode 2221.数组的三角和](https://zhuanlan.zhihu.com/p/542196418) · 知乎 · 2022-07-15 · 赞同 0**
> 力扣：[2221. 数组的三角和](https://leetcode.cn/problems/find-triangular-sum-of-an-array/) · Medium · 灵茶山艾府：[两种方法：O(n^2) 模拟 / O(n) 组合数学（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2221.数组的三角和

[力扣](https://leetcode.cn/problems/find-triangular-sum-of-an-array/)

看上去应该可以利用组合数学在O(n)的时间内求出结果，但是这里n的规模比较小，我就直接从上到下一层一层模拟计算了。

具体实现没有什么特殊的地方，就按照题目中描述的做法一步步来就行了。

最后附上python代码：

```python
class Solution(object):
    def triangularSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        for i in range(n - 1):
            new_nums = []
            for j in range(1, len(nums)):
                new_nums.append((nums[j] + nums[j - 1]) % 10)
            nums = new_nums[:]
        
        return nums[0]
```
