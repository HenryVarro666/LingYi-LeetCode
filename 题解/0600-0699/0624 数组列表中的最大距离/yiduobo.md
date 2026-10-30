---
title: "624. 数组列表中的最大距离"
aliases: ["yiduobo的每日leetcode 624.数组列表中的最大距离"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/零-常用枚举技巧", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/602097584"
zhihu_id: "602097584"
zhihu_title: "yiduobo的每日leetcode 624.数组列表中的最大距离"
question_id: "624"
question: "数组列表中的最大距离"
problem_url: "https://leetcode.cn/problems/maximum-distance-in-arrays/"
difficulty: "Medium"
created: "2023-01-31T00:12:45+08:00"
updated: "2023-01-31T00:12:45+08:00"
upvotes: 0
comments: 0
---

# 624. 数组列表中的最大距离

> **[yiduobo的每日leetcode 624.数组列表中的最大距离](https://zhuanlan.zhihu.com/p/602097584) · 知乎 · 2023-01-31 · 赞同 0**
> 力扣：[624. 数组列表中的最大距离](https://leetcode.cn/problems/maximum-distance-in-arrays/) · Medium · 灵茶山艾府：[枚举右，维护左（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

624.数组列表中的最大距离

[力扣](https://leetcode.cn/problems/maximum-distance-in-arrays/)

题目要求的最大距离实际上就是某个数组的最大值减去另一个数组的最小值。由于题目给出的数组列表中的数组都已经排好序了，因此最小值必然是数组的头一个元素，而最大值则是数组的最后一个元素。于是可以一趟遍历，使用两个遍历mi和ma记录当前遍历过数组中的最小值和最大值，二者分别初始化为arrays[0][0]以及arrays[0][-1]。接下来，对于遍历到的arrays[index]，首先使用arrays[index][-1] - mi以及ma - arrays[index][0]来更新最终答案，然后再使用arrays[index][0]来更新mi，arrays[index][-1]来更新ma即可。

最后附上python代码：

```python
class Solution(object):
    def maxDistance(self, arrays):
        """
        :type arrays: List[List[int]]
        :rtype: int
        """

        res = None
        mi = arrays[0][0]
        ma = arrays[0][-1]

        for arr in arrays[1:]:
            res = max(res, arr[-1] - mi, ma - arr[0])
            mi = min(mi, arr[0])
            ma = max(ma, arr[-1])
        
        return res
```
