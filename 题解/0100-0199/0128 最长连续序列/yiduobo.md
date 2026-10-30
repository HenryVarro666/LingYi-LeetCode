---
title: "128. 最长连续序列"
aliases: ["yiduobo的每日leetcode 128.最长连续序列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/LeetCode-热题-100/哈希", "题单/面试经典-150-题/哈希表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/140537474"
zhihu_id: "140537474"
zhihu_title: "yiduobo的每日leetcode 128.最长连续序列"
question_id: "128"
question: "最长连续序列"
problem_url: "https://leetcode.cn/problems/longest-consecutive-sequence/"
difficulty: "Medium"
created: "2020-05-13T22:45:58+08:00"
updated: "2020-05-13T22:45:58+08:00"
upvotes: 1
comments: 4
---

# 128. 最长连续序列

> **[yiduobo的每日leetcode 128.最长连续序列](https://zhuanlan.zhihu.com/p/140537474) · 知乎 · 2020-05-13 · 赞同 1**
> 力扣：[128. 最长连续序列](https://leetcode.cn/problems/longest-consecutive-sequence/) · Medium · 灵茶山艾府：[两个关键优化，O(n) 时间复杂度（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

128.最长连续序列<https://leetcode-cn.com/problems/longest-consecutive-sequence/>

哈希表的题目。

这里O(nlogn)的算法很容易想到，先排好序然后从头开始往后扫描判断相邻两数是否连续。

线性的算法这里需要利用哈希表。

那么对于数组中的某个数x，我们可以一次判断x+1, x+2, x+3, ...与x - 1, x - 2, x - 3, ...是否也在数组中，这个判断通过哈希表可以在常数时间内完成。这样一来，对于每个数可以在O(n)的时间内判断出其所在连续序列的长度，最终时间复杂度则需要O(n^2)。但是对于同一序列中的数，进行多次判断实际上是浪费了。

样例中，对于2，我们判断了1、3、4是否存在，对于3，我们又判断了1、2、4是否存在，实际上是非常浪费的。那么，我们需要想办法对每个序列只进行一次判断。

一个很自然的想法就是从序列的最大数开始判断，若x不是序列中的最大数，那么跳过，否则逐个判断x - 1, x - 2, x - 3, ...是否存在。

那么应该如何判断x不是序列中的最大数呢？做法也很简单，检测x + 1是否存在即可。如果x + 1存在，说明x并不是序列中的最大数，那么跳过x，否则就开始逐个执行检测。

由于每个数最多只会被检测一遍，因此最终的时间复杂度就优化到了O(n)。

最后附上python代码：

```python
class Solution(object):
    def longestConsecutive(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        num_set = set(nums)
        res = 0
        for num in num_set:
            if num + 1 not in num_set:
                x = num
                tmp = 0
                while x in num_set:
                    tmp += 1
                    x -= 1
                res = max(res, tmp)
        return res
```
