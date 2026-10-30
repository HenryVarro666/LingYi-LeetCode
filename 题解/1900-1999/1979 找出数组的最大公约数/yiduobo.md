---
title: "1979. 找出数组的最大公约数"
aliases: ["yiduobo的每日leetcode 1979.找出数组的最大公约数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/497534733"
zhihu_id: "497534733"
zhihu_title: "yiduobo的每日leetcode 1979.找出数组的最大公约数"
question_id: "1979"
question: "找出数组的最大公约数"
problem_url: "https://leetcode.cn/problems/find-greatest-common-divisor-of-array/"
difficulty: "Easy"
rating: 1184
created: "2022-04-13T00:57:08+08:00"
updated: "2022-04-13T00:57:09+08:00"
upvotes: 0
comments: 0
---

# 1979. 找出数组的最大公约数

> **[yiduobo的每日leetcode 1979.找出数组的最大公约数](https://zhuanlan.zhihu.com/p/497534733) · 知乎 · 2022-04-13 · 赞同 0**
> 力扣：[1979. 找出数组的最大公约数](https://leetcode.cn/problems/find-greatest-common-divisor-of-array/) · Easy · 灵茶山艾府：[只需约 1.5n 次比较，就能找到最小值和最大值（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1979.找出数组的最大公约数

[力扣](https://leetcode-cn.com/problems/find-greatest-common-divisor-of-array/)

比较基础的题目，按照题目要求一趟遍历，找出数组中的最大值和最小值，然后求二者的最大公约数即可。

最后附上python代码：

```python
class Solution(object):
    def findGCD(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        ma = mi = nums[0]
        for num in nums[1:]:
            ma = max(ma, num)
            mi = min(mi, num)

        while mi:
            ma, mi = mi, ma % mi
        
        return ma
```
