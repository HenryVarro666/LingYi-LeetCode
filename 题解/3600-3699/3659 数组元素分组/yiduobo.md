---
title: "3659. 数组元素分组"
aliases: ["yiduobo的每日leetcode 3659.数组元素分组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/array", "leetcode/hash-table", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1950220787375125802"
zhihu_id: "1950220787375125802"
zhihu_title: "yiduobo的每日leetcode 3659.数组元素分组"
question_id: "3659"
question: "数组元素分组"
problem_url: "https://leetcode.cn/problems/partition-array-into-k-distinct-groups/"
difficulty: "Medium"
rating: 1440
created: "2025-09-14T15:48:15+08:00"
updated: "2025-09-14T15:48:17+08:00"
upvotes: 1
comments: 0
---

# 3659. 数组元素分组

> **[yiduobo的每日leetcode 3659.数组元素分组](https://zhuanlan.zhihu.com/p/1950220787375125802) · 知乎 · 2025-09-14 · 赞同 1**
> 力扣：[3659. 数组元素分组](https://leetcode.cn/problems/partition-array-into-k-distinct-groups/) · Medium · 灵茶山艾府：[结论题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3659.数组元素分组

[3659. 数组元素分组 - 力扣（LeetCode）](https://leetcode.cn/problems/partition-array-into-k-distinct-groups/description/)

题目给出一个整数数组nums以及一个整数k，问能否将nums中的所有元素分成一个或多个组，使得每个组中恰好包含k个元素，所有的元素都必须被分配到恰好一个组中，且每个组中的元组互不相同。

首先可以明确的是，nums中元素的总数n必须是k的倍数，否则按k个一组来分的话必然有剩下的。

接下来，可以通过n // k计算出最终得到的组数，而根据鸽笼原理，单个元素出现的次数也不能大于n // k，否则必然有至少一组中有两个相同的元素。

那么是否只需要满足以上两个条件就必然可以完成分组呢？答案是肯定的。一种可行的构造方案是将所有元素从小到大进行排序，然后依次分配到各个组中。由于每个元素出现的次数都不超过组数，因此每一组中都不会出现相同的元素，同时每个元素都可以完成分配。

最后附上python代码：

```python
class Solution(object):
    def partitionArray(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: bool
        """
        
        n = len(nums)
        if n % k != 0:
            return False
        
        cnt = {}
        for v in nums:
            cnt[v] = cnt.get(v, 0) + 1
            if cnt[v] > n // k:
                return False
        return True
```
