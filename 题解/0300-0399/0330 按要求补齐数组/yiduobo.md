---
title: "330. 按要求补齐数组"
aliases: ["yiduobo的每日leetcode 330.按要求补齐数组"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/math", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/161474394"
zhihu_id: "161474394"
zhihu_title: "yiduobo的每日leetcode 330.按要求补齐数组"
question_id: "330"
question: "按要求补齐数组"
problem_url: "https://leetcode.cn/problems/patching-array/"
difficulty: "Hard"
rating: 2952
created: "2020-07-18T14:35:16+08:00"
updated: "2020-07-18T14:35:16+08:00"
upvotes: 0
comments: 0
---

# 330. 按要求补齐数组

> **[yiduobo的每日leetcode 330.按要求补齐数组](https://zhuanlan.zhihu.com/p/161474394) · 知乎 · 2020-07-18 · 赞同 0**
> 力扣：[330. 按要求补齐数组](https://leetcode.cn/problems/patching-array/) · Hard · 灵茶山艾府：[【视频】排序+贪心（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

330.按要求补齐数组

很有意思的题目。不妨设目前数组的前k个数可以覆盖住1到x，那么接下来需要想办法将x + 1也覆盖住。

首先考察数组的第k + 1个数p。已知前k个数可以覆盖住1到x，那么加入p之后，可以覆盖的范围就成了1到x，以及1 + p到x + p。

那么如果这个1 + p \<\= 1 + x，即p \<\= x，那么这两个区间就可以合并成为1到x + p，发现可以覆盖到x + 1，那么此时就变成了前k + 1个数可以覆盖住1到x + p，我们接下来需要继续考察x + p +1的覆盖情况。

否则的话，一定有x \< x + 1 \< 1 + p，此时无法覆盖到x + 1。又因为数组是单调递增的，因此仅依靠数组后面的数也一定覆盖不了x + 1，于是此时我们需要添加一个数来覆盖x + 1。已知可以覆盖住1到x，加入一个数之后需要覆盖x + 1，那么加入的这个数可以是1到x + 1中的任意一个数。在这里，加入x + 1可以将覆盖区间扩展到1到x + x + 1，显然是最优的。于是在这种情况下，选择添加一个额外的x + 1，那么此时就是前k个数加上这个额外的数就可以覆盖1到x + x + 1，接下来继续考察x + x + 2的覆盖情况即可。

最坏情况下需要遍历整个nums数组，且需要执行logn次倍增操作，于是最终的时间复杂度应该是O(len(nums) + logn)。

最后附上python代码：

```
class Solution(object):
    def minPatches(self, nums, n):
        """
        :type nums: List[int]
        :type n: int
        :rtype: int
        """

        x = 1
        res = 0
        k = 0
        if k < len(nums):
            p = nums[k]
        while x <= n:
            if k < len(nums) and p <= x:
                x += p
                k += 1
                if k < len(nums):
                    p = nums[k]
            else:
                x += x
                res += 1

        return res
```
