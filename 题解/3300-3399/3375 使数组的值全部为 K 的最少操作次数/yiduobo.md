---
title: "3375. 使数组的值全部为k的最少操作次数"
aliases: ["yiduobo的每日leetcode 3375.使数组的值全部为k的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/hash-table", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/28752012820"
zhihu_id: "28752012820"
zhihu_title: "yiduobo的每日leetcode 3375.使数组的值全部为k的最少操作次数"
question_id: "3375"
question: "使数组的值全部为 K 的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-array-values-equal-to-k/"
difficulty: "Easy"
rating: 1383
created: "2025-03-08T00:35:24+08:00"
updated: "2025-03-08T00:35:24+08:00"
upvotes: 4
comments: 0
---

# 3375. 使数组的值全部为k的最少操作次数

> **[yiduobo的每日leetcode 3375.使数组的值全部为k的最少操作次数](https://zhuanlan.zhihu.com/p/28752012820) · 知乎 · 2025-03-08 · 赞同 4**
> 力扣：[3375. 使数组的值全部为 K 的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-make-array-values-equal-to-k/) · Easy · 灵茶山艾府：[本质是计算不同元素个数（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3375.使数组的值全部为k的最少操作次数

[3375. 使数组的值全部为 K 的最少操作次数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-make-array-values-equal-to-k/description/)

题目给出一个整数数组nums以及一个整数k。若数组中所有严格大于h的整数都相等，那么就称h是合法的。例如nums \= [10, 8, 10, 8]，那么h \= 9是合法的，但是5不是合法的。

接下来对于nums，可以选择一个合法的整数h，将nums中所有大于h的元素都变为h。问至少要多少次操作才能将nums中的所有元素都变为k，若无法达成，则返回-1。

首先考虑特殊情况，若nums中的最小值小于k，那么这个值必然无法变成k，此时返回-1。

接下来对于一般情况，若nums中有两个或以上的不同元素，那么每次选择的h就必须大于等于数组中第二大的元素。为了使得操作的次数最少，每一轮操作都应该选择数组中第二大的元素值作为h，这样就可以将数组中最大的元素都变为h。更进一步的，若nums中有m种不同的元素，那么可以在m - 1轮操作后将nums中的所有元素都变为nums中的最小值。接下来，若k小于这个最小值，那么还需要一次操作将nums都变为k；若k等于这个最小值，那么就无需额外操作了。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        mi = min(nums)
        if mi < k:
            return -1

        res = len(set(nums)) - 1
        if k < mi:
            res += 1
        return res
```
