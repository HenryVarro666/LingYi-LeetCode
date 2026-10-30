---
title: "3852. 不同频率的最小数对"
aliases: ["yiduobo的每日leetcode 3852.不同频率的最小数对"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2011511171493155572"
zhihu_id: "2011511171493155572"
zhihu_title: "yiduobo的每日leetcode 3852.不同频率的最小数对"
question_id: "3852"
question: "不同频率的最小数对"
problem_url: "https://leetcode.cn/problems/smallest-pair-with-different-frequencies/"
difficulty: "Easy"
created: "2026-03-04T21:26:56+08:00"
updated: "2026-03-04T21:26:57+08:00"
upvotes: 1
comments: 0
---

# 3852. 不同频率的最小数对

> **[yiduobo的每日leetcode 3852.不同频率的最小数对](https://zhuanlan.zhihu.com/p/2011511171493155572) · 知乎 · 2026-03-04 · 赞同 1**
> 力扣：[3852. 不同频率的最小数对](https://leetcode.cn/problems/smallest-pair-with-different-frequencies/) · Easy · 灵茶山艾府：[O(n) 做法，脑筋急转弯（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3852.不同频率的最小数对

<https://leetcode.cn/problems/smallest-pair-with-different-frequencies/description/>

题目给出一个整数数组nums，现在要求从nums中找出一组x和y，满足x \< y，且x和y在nums中的频率不同。

要求找出的数对[x, y]中，x尽量的小，若x相同，则选择y最小的那一组。

若不存在合法的数对，则返回[-1, -1]。

由于题目要求选取的数对在nums中的频率不同，又要求选取的数对最小，那么就可以对每种频率都维护一个具有对应频率的最小值，然后取这些最小值中最小的两个作为最终答案。

于是可以先对nums进行一趟遍历，计算其中每种元素的频率，记为freq。接下来再对freq进行一趟遍历，使用其中所有的(v, f)来更新哈希表freq_mi，其中freq_mi[f]记录的是频率f对应的最小值。最后，从freq_mi中取出最小的两个值作为最终答案即可。若freq_mi中的元素不足两个，则返回[-1, -1]。

最后附上python代码：

```python
class Solution(object):
    def minDistinctFreqPair(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        
        freq = {}
        for v in nums:
            freq[v] = freq.get(v, 0) + 1
        
        freq_mi = {}
        for v, f in freq.items():
            if f not in freq_mi:
                freq_mi[f] = v
            else:
                freq_mi[f] = min(freq_mi[f], v)
        
        x, y = -1, -1
        for mi in freq_mi.values():
            if x == -1 or x > mi:
                x, y = mi, x
            elif y == -1 or y > mi:
                y = mi
        
        if y == -1:
            return [-1, -1]
        else:
            return [x, y]
```
