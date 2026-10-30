---
title: "2598. 执行操作后的最大MEX"
aliases: ["yiduobo的每日leetcode 2598.执行操作后的最大MEX"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/644194230"
zhihu_id: "644194230"
zhihu_title: "yiduobo的每日leetcode 2598.执行操作后的最大MEX"
question_id: "2598"
question: "执行操作后的最大 MEX"
problem_url: "https://leetcode.cn/problems/smallest-missing-non-negative-integer-after-operations/"
difficulty: "Medium"
rating: 1846
created: "2023-07-18T01:10:18+08:00"
updated: "2023-07-18T01:10:18+08:00"
upvotes: 0
comments: 0
---

# 2598. 执行操作后的最大MEX

> **[yiduobo的每日leetcode 2598.执行操作后的最大MEX](https://zhuanlan.zhihu.com/p/644194230) · 知乎 · 2023-07-18 · 赞同 0**
> 力扣：[2598. 执行操作后的最大 MEX](https://leetcode.cn/problems/smallest-missing-non-negative-integer-after-operations/) · Medium · 灵茶山艾府：[同余分组（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2598.执行操作后的最大MEX

[力扣](https://leetcode.cn/problems/smallest-missing-non-negative-integer-after-operations/)

由于每次操作只能加上或者减去value，那么就意味着操作并不能影响原数对value取模的结果，于是可以先将这些数按照对value取模的余数分为value类。

接下来，需要使用这些数从0开始填充这个数组。如果以value个数为一轮，那么就意味着这value类数都需要出一份力。具体来说，就是第一轮选取0到value - 1，第二轮选取value到value \* 2 - 1，以此类推。

更进一步的，如果在某一轮某类数用完了，那么此时就产生了缺失的数，也就是题目要求的答案。

根据这个结论，就可以统计每一类中数的个数。令mi_freq表示这个个数的最小值，mi_r表示这一类数对应的余数。若有多个类出现的次数都等于mi_freq，那么就取其中余数最小的那一类作为对应的r。

可以发现，mi_freq就是上面可以完整取出value个数的轮次，因此缺失的数就是mi_freq \* value + mi_r。

最后附上python代码：

```python
class Solution(object):
    def findSmallestInteger(self, nums, value):
        """
        :type nums: List[int]
        :type value: int
        :rtype: int
        """

        cnt = {}
        for v in nums:
            if v >= 0:
                r = v % value
            else:
                r = (-v) % value
                if r > 0:
                    r = value - r
            
            cnt[r] = cnt.get(r, 0) + 1
        
        mi_freq = None
        mi_r = None
        for r in range(value):
            if mi_freq is None or cnt.get(r, 0) < mi_freq:
                mi_freq = cnt.get(r, 0)
                mi_r = r

        return mi_freq * value + mi_r
```
