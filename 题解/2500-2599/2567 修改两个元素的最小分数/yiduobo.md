---
title: "2567. 修改两个元素的最小分数"
aliases: ["yiduobo的每日leetcode 2567.修改两个元素的最小分数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/641023766"
zhihu_id: "641023766"
zhihu_title: "yiduobo的每日leetcode 2567.修改两个元素的最小分数"
question_id: "2567"
question: "修改两个元素的最小分数"
problem_url: "https://leetcode.cn/problems/minimum-score-by-changing-two-elements/"
difficulty: "Medium"
rating: 1609
created: "2023-07-02T22:06:52+08:00"
updated: "2023-07-02T22:06:52+08:00"
upvotes: 0
comments: 0
---

# 2567. 修改两个元素的最小分数

> **[yiduobo的每日leetcode 2567.修改两个元素的最小分数](https://zhuanlan.zhihu.com/p/641023766) · 知乎 · 2023-07-02 · 赞同 0**
> 力扣：[2567. 修改两个元素的最小分数](https://leetcode.cn/problems/minimum-score-by-changing-two-elements/) · Medium · 灵茶山艾府：[只有三种情况（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2567.修改两个元素的最小分数

[力扣](https://leetcode.cn/problems/minimum-score-by-changing-two-elements/)

题目给出一个数组，要求修改其中的两个数，使得数组中两数之差绝对值的最小值与最大值之和最小。

让两数之差绝对值的最小值最小是很容易的，只需让修改后数组中存在两个相同的数，这样一来两数之差绝对值的最小值就必然为0了。

而对于两数之差绝对值的最大值，则取决于修改后数组中最大值以及最小值。换言之，在这里就应该修改原始数组中的最大值或者最小值。由于只能修改两个数，那么一共只有三种修改方案：

1、修改最大值和次大值。

此时两数之差绝对值的最大值就是原数组中的第三大值减去原数组中的最小值

2、修改最大值和最小值。

此时两数之差绝对值的最大值就是原数组中的第二大值减去原数组中的第二小值

3、修改最小值的次小值。

此时两数之差绝对值的最大值就是原数组中的最大值减去原数组中的第三小值

那么最终答案就是上面这三种情况中的最小值

最后附上python代码：

```python
class Solution(object):
    def minimizeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        nums.sort()

        cand1 = nums[-3] - nums[0]
        cand2 = nums[-2] - nums[1]
        cand3 = nums[-1] - nums[2]
        return min(cand1, cand2, cand3)
```
