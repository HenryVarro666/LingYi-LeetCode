---
title: "2176. 统计数组中相等且可以被整除的数对"
aliases: ["yiduobo的每日leetcode 2176.统计数组中相等且可以被整除的数对"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/math", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/534637738"
zhihu_id: "534637738"
zhihu_title: "yiduobo的每日leetcode 2176.统计数组中相等且可以被整除的数对"
question_id: "2176"
question: "统计数组中相等且可以被整除的数对"
problem_url: "https://leetcode.cn/problems/count-equal-and-divisible-pairs-in-an-array/"
difficulty: "Easy"
rating: 2200
created: "2022-06-28T00:12:35+08:00"
updated: "2022-06-28T00:12:35+08:00"
upvotes: 0
comments: 0
---

# 2176. 统计数组中相等且可以被整除的数对

> **[yiduobo的每日leetcode 2176.统计数组中相等且可以被整除的数对](https://zhuanlan.zhihu.com/p/534637738) · 知乎 · 2022-06-28 · 赞同 0**
> 力扣：[2176. 统计数组中相等且可以被整除的数对](https://leetcode.cn/problems/count-equal-and-divisible-pairs-in-an-array/) · Easy · 灵茶山艾府：[O(nlogn) 数学做法，枚举右维护左（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2176.统计数组中相等且可以被整除的数对

[力扣](https://leetcode.cn/problems/count-equal-and-divisible-pairs-in-an-array/)

由于题目的数据规模很小，因此可以直接暴力枚举每一组i和j，若满足nums[i] \= nums[j]且i \* j是k的倍数，那么就将答案加上1。

除此之外，也存在更好的做法。如果先将数组中的数按数值收集到一起，那么问题就变成了给出一个数组，问数组中有多少组数对的乘积为k的倍数，这个问题恰好就是之后的2183题，到时候再按较大数据规模下的做法来做。

最后附上python代码：

```python
class Solution(object):
    def countPairs(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        res = 0
        for i in range(len(nums) - 1):
            for j in range(i + 1, len(nums)):
                if nums[i] == nums[j] and i * j % k == 0:
                    res += 1
        
        return res
```
