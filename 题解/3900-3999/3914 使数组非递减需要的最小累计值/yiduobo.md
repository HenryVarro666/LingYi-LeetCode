---
title: "3914. 使数组非递减需要的最小累计值"
aliases: ["yiduobo的每日leetcode 3914.使数组非递减需要的最小累计值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/常用数据结构", "题单/常用数据结构/二-差分"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2032960118501921647"
zhihu_id: "2032960118501921647"
zhihu_title: "yiduobo的每日leetcode 3914.使数组非递减需要的最小累计值"
question_id: "3914"
question: "使数组非递减需要的最小累计值"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-array-non-decreasing/"
difficulty: "Medium"
rating: 1662
created: "2026-04-29T23:24:23+08:00"
updated: "2026-04-29T23:24:24+08:00"
upvotes: 0
comments: 0
---

# 3914. 使数组非递减需要的最小累计值

> **[yiduobo的每日leetcode 3914.使数组非递减需要的最小累计值](https://zhuanlan.zhihu.com/p/2032960118501921647) · 知乎 · 2026-04-29 · 赞同 0**
> 力扣：[3914. 使数组非递减需要的最小累计值](https://leetcode.cn/problems/minimum-operations-to-make-array-non-decreasing/) · Medium · 灵茶山艾府：[差分思想，简洁写法，附相似题目（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3914.使数组非递减需要的最小累计值

<https://leetcode.cn/problems/minimum-operations-to-make-array-non-decreasing/description/>

题目给出一个长度为n的整数数组nums。

在一次操作中，可以选择nums中的任意一个子数组，将子数组中所有元素都加上x，这里的x可以是任意的正整数。问要将nums变为非递减所需的所有操作中，每次操作的x之和的最小值是多少。

题目要求计算所有操作对应的x的最小值，那么在这里不妨先考虑单次操作应该如何进行。

对于某次修改，假设将nums[left]到nums[right]之间的所有元素都增加了x，那么对于nums[right]右侧的所有元素来说，这些元素比nums[left]到nums[right]之间的元素更小的可能性就增加了。由于每次操作可以任意选择操作的子数组，那么为了规避操作对后续元素的影响，在这里就应该一同修改nums[right + 1]到nums[n - 1]。更一般的，每次修改就应该修改nums中的一个后缀。

基于上面的结论，在这里就只需一趟遍历，对于当前元素nums[index]，若其小于nums[index - 1]，那么就将nums[index - 1] - nums[index]累积到答案中即可。

这样做的理由是每次的修改都是修改整个后缀，因此对于nums[index]而言，前面所有的修改都修改到了nums[index - 1]以及nums[index]，在比大小的语境下相当于没有进行修改。因此在这里只需要对比这两个元素并计算是否需要修改即可。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        res = 0
        for index in range(1, len(nums)):
            if nums[index] < nums[index - 1]:
                res += nums[index - 1] - nums[index]
        
        return res
```
