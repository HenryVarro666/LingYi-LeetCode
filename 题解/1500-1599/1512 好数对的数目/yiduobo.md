---
title: "1512. 好数对的数目"
aliases: ["yiduobo的每日leetcode 1512.好数对的数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/hash-table", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/420378438"
zhihu_id: "420378438"
zhihu_title: "yiduobo的每日leetcode 1512.好数对的数目"
question_id: "1512"
question: "好数对的数目"
problem_url: "https://leetcode.cn/problems/number-of-good-pairs/"
difficulty: "Easy"
rating: 1161
created: "2021-10-11T23:53:10+08:00"
updated: "2021-10-11T23:53:10+08:00"
upvotes: 0
comments: 0
---

# 1512. 好数对的数目

> **[yiduobo的每日leetcode 1512.好数对的数目](https://zhuanlan.zhihu.com/p/420378438) · 知乎 · 2021-10-11 · 赞同 0**
> 力扣：[1512. 好数对的数目](https://leetcode.cn/problems/number-of-good-pairs/) · Easy · 灵茶山艾府：[O(n) 做法：枚举右，维护左（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1512.好数对的数目

[力扣](https://leetcode-cn.com/problems/number-of-good-pairs/)

若某一个数出现了k次，那么可以形成C(k, 2)也就是k \* (k - 1) / 2组好数对，那么可以一趟扫描，统计每个数出现的次数，然后分别计算方案数再求和。

最后附上python代码：

```python
class Solution(object):
    def numIdenticalPairs(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        cnt_list = [0] * 101
        for num in nums:
            cnt_list[num] += 1
        
        res = 0
        for num in range(1, 101):
            if cnt_list[num] >= 2:
                res += cnt_list[num] * (cnt_list[num] - 1) / 2
            
        return res
```
