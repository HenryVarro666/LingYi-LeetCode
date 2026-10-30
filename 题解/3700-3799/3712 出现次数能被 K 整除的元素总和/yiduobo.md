---
title: "3712. 出现次数能被k整除的元素总和"
aliases: ["yiduobo的每日leetcode 3712.出现次数能被k整除的元素总和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1961548007871866572"
zhihu_id: "1961548007871866572"
zhihu_title: "yiduobo的每日leetcode 3712.出现次数能被k整除的元素总和"
question_id: "3712"
question: "出现次数能被 K 整除的元素总和"
problem_url: "https://leetcode.cn/problems/sum-of-elements-with-frequency-divisible-by-k/"
difficulty: "Easy"
created: "2025-10-14T21:47:51+08:00"
updated: "2025-10-14T21:47:52+08:00"
upvotes: 0
comments: 0
---

# 3712. 出现次数能被k整除的元素总和

> **[yiduobo的每日leetcode 3712.出现次数能被k整除的元素总和](https://zhuanlan.zhihu.com/p/1961548007871866572) · 知乎 · 2025-10-14 · 赞同 0**
> 力扣：[3712. 出现次数能被 K 整除的元素总和](https://leetcode.cn/problems/sum-of-elements-with-frequency-divisible-by-k/) · Easy · 灵茶山艾府：[统计每个元素的出现次数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3712.出现次数能被K整除的元素总和

[3712. 出现次数能被 K 整除的元素总和 - 力扣（LeetCode）](https://leetcode.cn/problems/sum-of-elements-with-frequency-divisible-by-k/description/)

题目给出一个整数数组nums以及一个整数k。现在要求返回一个整数，表示nums中所有出现次数能被k整除的元素之和，若不存在这样的元素，则返回0。

一趟遍历，使用哈希表freq记录每种元素出现的次数，然后再对freq进行一趟遍历，对于其中的元素v，若v出现次数freq[v]为k的倍数，那么就将v \* freq[v]累加到答案中。

最后附上python代码：

```python
class Solution(object):
    def sumDivisibleByK(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        freq = {}
        for v in nums:
            freq[v] = freq.get(v, 0) + 1
        
        res = 0
        for v in freq:
            if freq[v] % k == 0:
                res += v * freq[v]
        
        return res
```
