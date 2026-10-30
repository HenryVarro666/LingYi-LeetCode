---
title: "2344. 使数组可以被整除的最少删除次数"
aliases: ["yiduobo的每日leetcode 2344.使数组可以被整除的最少删除次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/math", "leetcode/number-theory", "leetcode/sorting", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/560405623"
zhihu_id: "560405623"
zhihu_title: "yiduobo的每日leetcode 2344.使数组可以被整除的最少删除次数"
question_id: "2344"
question: "使数组可以被整除的最少删除次数"
problem_url: "https://leetcode.cn/problems/minimum-deletions-to-make-array-divisible/"
difficulty: "Hard"
rating: 1641
created: "2022-09-02T02:44:28+08:00"
updated: "2022-09-02T02:44:28+08:00"
upvotes: 0
comments: 0
---

# 2344. 使数组可以被整除的最少删除次数

> **[yiduobo的每日leetcode 2344.使数组可以被整除的最少删除次数](https://zhuanlan.zhihu.com/p/560405623) · 知乎 · 2022-09-02 · 赞同 0**
> 力扣：[2344. 使数组可以被整除的最少删除次数](https://leetcode.cn/problems/minimum-deletions-to-make-array-divisible/) · Hard · 灵茶山艾府：[转换 + 贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2344.使数组可以被整除的最少删除次数

[力扣](https://leetcode.cn/problems/minimum-deletions-to-make-array-divisible/)

虽然按题目的描述可以删除数组中的任意整数，但是再计算整除的时候用到的是数组中的最小值，也就是说实际上每次执行的删除操作都应该删除最小值，或者换句话说就是，找出nums中可以被numsDivide中所有数整除的最小值。

可以明确的是，能被numsDivide中所有数整除的最大整数，必然是numsDivide中所有数的最大公约数，不妨记为g。那么问题就变成了找出nums中最小的，且可以被g整除的数。

于是只需要一趟遍历，找出这个数。若找不到，那么说明无解，直接返回-1，否则再进行一趟遍历，计算出nums中比这个数还要小的数有多少个，这些数就是需要删除的数了。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums, numsDivide):
        """
        :type nums: List[int]
        :type numsDivide: List[int]
        :rtype: int
        """

        g = numsDivide[0]
        for num in numsDivide[1:]:
            x, y = num, g
            while y:
                x, y = y, x % y
            
            g = x
        
        min_num = None
        for num in nums:
            if g % num == 0:
                if min_num is None or min_num > num:
                    min_num = num
        
        if min_num is None:
            return -1
        
        res = 0
        for num in nums:
            if num < min_num:
                res += 1
        
        return res
```
