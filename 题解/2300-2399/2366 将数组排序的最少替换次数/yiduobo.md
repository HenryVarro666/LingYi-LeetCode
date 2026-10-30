---
title: "2366. 将数组排序的最少替换次数"
aliases: ["yiduobo的每日leetcode 2366.将数组排序的最少替换次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/math", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/563093208"
zhihu_id: "563093208"
zhihu_title: "yiduobo的每日leetcode 2366.将数组排序的最少替换次数"
question_id: "2366"
question: "将数组排序的最少替换次数"
problem_url: "https://leetcode.cn/problems/minimum-replacements-to-sort-the-array/"
difficulty: "Hard"
rating: 2060
created: "2022-09-10T02:23:58+08:00"
updated: "2022-09-10T02:23:58+08:00"
upvotes: 0
comments: 0
---

# 2366. 将数组排序的最少替换次数

> **[yiduobo的每日leetcode 2366.将数组排序的最少替换次数](https://zhuanlan.zhihu.com/p/563093208) · 知乎 · 2022-09-10 · 赞同 0**
> 力扣：[2366. 将数组排序的最少替换次数](https://leetcode.cn/problems/minimum-replacements-to-sort-the-array/) · Hard · 灵茶山艾府：[贪心 + 详细证明（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2366.将数组排序的最少替换次数

[力扣](https://leetcode.cn/problems/minimum-replacements-to-sort-the-array/)

题目要求数组单调不减，因此每个数是否需要拆分取决于其后面那个数的大小，那么不妨从后向前考虑如何拆分。

首先对于数组的最后一个数，显然不应该进行拆分，因为拆分后只会提高数组单调不减的难度。

接下来对于倒数第二个数，若其小于等于最后一个数，那么就无须拆分，理由同上。若其大于最后一个数，就必须将倒数第二个数拆分成一个单调不减的子数组，同时这个子数组中的数需要小于等于原数组中的最后那个数。为了使得拆分次数最少，也就是要求这个子数组尽可能短。另一方面，子数组的首个元素也需要尽可能地大，这样可以使得更前面的数组更容易进行拆分。

简单来说，对于倒数第二个数nums[n - 2]的拆分需要满足两点：

1、拆分出来的子数组的首个元素尽可能大，这样一来既可以使得拆分出来的子数组最短，也就是拆分次数最少，也可以使得更前面位置的拆分会变得更容易

2、拆分出来的子数组的最后一个元素必须小于等于原数组中的最后一个元素nums[n - 1]

可以发现，最理想的拆分方式自然是将nums[n - 2]拆分成若干个nums[n - 1]，但是这里有一个前提是nums[n - 2]是nums[n - 1]的倍数。如果nums[n - 2]不是nums[n - 1]的倍数，那么最理想的拆分方式就是

nums[n - 2] \= x + x + ... + x + (x + 1) + (x + 1) + ... + (x + 1)

这种形式

也就是将nums[n - 2] % x的余数分配给子数组的最后几个数，同时也要求x + 1 \<\= nums[n - 1]。

在这里不妨设有p个x，q个(x + 1)，那么就可以写成nums[n - 2] + p \= (x + 1) \* q。在这里为了使得x尽可能大，就需要使得q尽可能小。但是q如果过小，又会使得x + 1 > nums[n - 1]，所以在这里可以直接使用nums[n - 2] / nums[n - 1]来确定q - 1的下限，然后带入求出x就行了。

对于nums中更前面的数，使用同样的方式处理就行了。在这里需要注意的是，如果在nums[k]被拆分后，与nums[k - 1]比较的应该是拆分出来的子数组的第一个元素x，而不是原始的nums[k]。因此在具体实现时需要使用一个变量x记录用来与当前元素比较的数是什么。

最后附上python代码：

```python
class Solution(object):
    def minimumReplacement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        last = nums[-1]
        res = 0
        for index in range(len(nums) - 2, -1, -1):
            if nums[index] <= last:
                last = nums[index]
            elif nums[index] % last == 0:
                res += nums[index] / last - 1
            else:
                cnt = nums[index] / last
                res += cnt
                last = nums[index] / (cnt + 1)

        return res
```
