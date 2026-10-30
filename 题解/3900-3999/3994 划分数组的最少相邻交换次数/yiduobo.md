---
title: "3994. 划分数组的最少相邻交换次数"
aliases: ["yiduobo的每日leetcode 3994.划分数组的最少相邻交换次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2063029918552928619"
zhihu_id: "2063029918552928619"
zhihu_title: "yiduobo的每日leetcode 3994.划分数组的最少相邻交换次数"
question_id: "3994"
question: "划分数组的最少相邻交换次数"
problem_url: "https://leetcode.cn/problems/minimum-adjacent-swaps-to-partition-array/"
difficulty: "Medium"
rating: 1705
created: "2026-07-21T22:55:59+08:00"
updated: "2026-07-21T22:56:03+08:00"
upvotes: 0
comments: 0
---

# 3994. 划分数组的最少相邻交换次数

> **[yiduobo的每日leetcode 3994.划分数组的最少相邻交换次数](https://zhuanlan.zhihu.com/p/2063029918552928619) · 知乎 · 2026-07-21 · 赞同 0**
> 力扣：[3994. 划分数组的最少相邻交换次数](https://leetcode.cn/problems/minimum-adjacent-swaps-to-partition-array/) · Medium · 灵茶山艾府：[计算逆序对的个数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3994.划分数组的最少相邻交换次数

<https://leetcode.cn/problems/minimum-adjacent-swaps-to-partition-array/>

题目给出一个整数数组nums以及两个整数a和b，满足a \< b。

若一个数组可以按顺序分成三个连续的部分，且满足以下条件，则称其为好数组：

- 第一个部分中的所有元素都小于a
- 第二个部分中的所有元素都在闭区间[a, b]之内
- 第三个部分中的所有元素都大于b

这三个部分总的任意一个都可以为空。

在一次相邻交换中，可以交换nums中的两个相邻元素，要求返回使得nums成为好数组所需的最少相邻交换次数，答案对10^9 + 7取模。

首先可以明确的是，基于题目中只能交换相邻元素的交换规则，属于同一个区间中的元素间是不应该进行交换的。更进一步的，这也就意味着同一区间内的元素间的相对顺序将保留原数组中的相对顺序。基于这一点，就可以先通过一趟遍历，计算最终的好数组中每个区间内元素的数量，然后再一趟遍历，构造出最终的好数组。

得到好数组后，需要计算最终的交换次数。为了避免重复，在这里只统计右侧向左侧交换的次数。此时只需再一趟遍，对比每个元素与其在好数组中的位置，若需要向左移动，那么就将当前下标与好数组中的下标之差累加到答案中即可。

在具体实现上，不需要真的构造出好数组，而是可以先一趟遍历，处理掉最左侧区间中的元素。具体来说，使用一个变量p记录最左侧区间中下一个元素应该填充的位置，对于当前遍历到的元素，若其属于最左侧区间，则将当前下标与p之差累加到答案中，然后将p加上1。

遍历完成后，最左侧区间就处理好了。接下来再一趟遍历，处理中间的区间，最右侧区间就会自动处理好。

对于中间区间的处理方式也是类似，不过需要注意的是，当前情况是已经处理好了最左侧区间，因此虽然遍历的是原数组，但是对于属于中间区间的元素，其下标应该从p开始，因此在这里需要额外使用一个变量now记录真实下标，然后p保持之前的含义，一趟遍历进行计算即可。

最后附上python代码：

```python
class Solution(object):
    def minAdjacentSwaps(self, nums, a, b):
        """
        :type nums: List[int]
        :type a: int
        :type b: int
        :rtype: int
        """
        
        p = 0
        res = 0
        mod = 10 ** 9 + 7
        for index, v in enumerate(nums):
            if v < a:
                res += index - p
                if res >= mod:
                    res -= mod
                p += 1
        
        now = p
        for v in nums:
            if v < a:
                continue
            
            if v <= b:
                res += now - p
                if res >= mod:
                    res -= mod
                p += 1
            
            now += 1
        
        return res
```
