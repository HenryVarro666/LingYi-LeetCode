---
title: "3002. 移除后集合的最多元素数"
aliases: ["yiduobo的每日leetcode 3002.移除后集合的最多元素数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/hash-table", "题单/贪心算法", "题单/贪心算法/八-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/693275657"
zhihu_id: "693275657"
zhihu_title: "yiduobo的每日leetcode 3002.移除后集合的最多元素数"
question_id: "3002"
question: "移除后集合的最多元素数"
problem_url: "https://leetcode.cn/problems/maximum-size-of-a-set-after-removals/"
difficulty: "Medium"
rating: 1917
created: "2024-04-18T22:11:41+08:00"
updated: "2024-04-18T22:11:41+08:00"
upvotes: 1
comments: 0
---

# 3002. 移除后集合的最多元素数

> **[yiduobo的每日leetcode 3002.移除后集合的最多元素数](https://zhuanlan.zhihu.com/p/693275657) · 知乎 · 2024-04-18 · 赞同 1**
> 力扣：[3002. 移除后集合的最多元素数](https://leetcode.cn/problems/maximum-size-of-a-set-after-removals/) · Medium · 灵茶山艾府：[两种思考问题的角度：移除元素/添加元素（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3002.移除后集合的最多元素数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-size-of-a-set-after-removals/description/)

题目要求从两个数组中各移除一半的元素，因此单个数组中剩余不重复元素的上限显然就是n除以2，但是单个数组中可能有很多重复的元素，因此单个数组中剩余不重复元素也不可能超过其原始不重复元素的数量。这两个值的较小值就是单个数组最大剩余元素数量。

得到单个数组的剩余元素数量的最大值后，将两个数组剩余元素的最大值相加就是最终答案的上限，但是同样的，两个数组合并后也可能有很多重复的元素，因此还需要取合并后数组中不同元素的数量，然后计算二者的较小值作为最终答案。

最后附上python代码：

```python
class Solution(object):
    def maximumSetSize(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        n = len(nums1)
        s1 = set(nums1)
        s2 = set(nums2)
        res = min(len(s1), n // 2) + min(len(s2), n // 2)
        s1.update(s2)
        return min(len(s1), res)
```
