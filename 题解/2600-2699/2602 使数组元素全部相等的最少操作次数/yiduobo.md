---
title: "2602. 使数组元素全部相等的最小操作次数"
aliases: ["yiduobo的每日leetcode 2602.使数组元素全部相等的最小操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "leetcode/prefix-sum", "leetcode/sorting", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/644679312"
zhihu_id: "644679312"
zhihu_title: "yiduobo的每日leetcode 2602.使数组元素全部相等的最小操作次数"
question_id: "2602"
question: "使数组元素全部相等的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-all-array-elements-equal/"
difficulty: "Medium"
rating: 1903
created: "2023-07-20T03:37:11+08:00"
updated: "2023-07-20T03:37:11+08:00"
upvotes: 0
comments: 0
---

# 2602. 使数组元素全部相等的最小操作次数

> **[yiduobo的每日leetcode 2602.使数组元素全部相等的最小操作次数](https://zhuanlan.zhihu.com/p/644679312) · 知乎 · 2023-07-20 · 赞同 0**
> 力扣：[2602. 使数组元素全部相等的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-make-all-array-elements-equal/) · Medium · 灵茶山艾府：[【一图秒懂】排序+前缀和+二分查找（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2602.使数组元素全部相等的最小操作次数

[力扣](https://leetcode.cn/problems/minimum-operations-to-make-all-array-elements-equal/)

对于一个询问q，需要将数组中所有小于等于q的数通过若干次加1操作变为q，将所有大于q的通过若干次减1操作变为q。不妨设小于等于q的数的总和为s1，数量为cnt1，大于q的数的总和为s2，数量为cnt2，那么最终的代价就是q \* cnt1 - s1 + s2 - q \* cnt2

另一方面，由于s1与s2之和就是数组总和，而cnt1与cnt2之和则是数组长度，那么在这里实际上只需要对于每个q计算出对应的s1以及cnt1就行了。对于这个问题，一个很自然的想法就是将数组从小到大进行排序并预处理出前缀和数组，接下来对于每个q，都可以二分这个q在数组中的位置，然后利用这个位置对应的前缀和以及前缀长度计算出其对应的操作数。

另外，也可以将询问数组同样从小到大进行排序，然后利用单调性一边遍历q一边计算其对应的s1以及cnt1。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[int]
        :rtype: List[int]
        """

        nums.sort()
        res = [0] * len(queries)
        p = 0
        s = sum(nums)
        prefix = 0
        for index, k in sorted(enumerate(queries), key=lambda d:d[1]):
            while p < len(nums) and nums[p] < k:
                prefix += nums[p]
                p += 1
            
            res[index] = k * p - prefix + s - prefix - (len(nums) - p) * k
        
        return res
```
