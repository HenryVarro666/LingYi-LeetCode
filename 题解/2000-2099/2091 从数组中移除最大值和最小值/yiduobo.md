---
title: "2091. 从数组中移除最大值和最小值"
aliases: ["yiduobo的每日leetcode 2091.从数组中移除最大值和最小值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/519995679"
zhihu_id: "519995679"
zhihu_title: "yiduobo的每日leetcode 2091.从数组中移除最大值和最小值"
question_id: "2091"
question: "从数组中移除最大值和最小值"
problem_url: "https://leetcode.cn/problems/removing-minimum-and-maximum-from-array/"
difficulty: "Medium"
rating: 1384
created: "2022-05-25T23:56:12+08:00"
updated: "2022-05-25T23:56:12+08:00"
upvotes: 0
comments: 0
---

# 2091. 从数组中移除最大值和最小值

> **[yiduobo的每日leetcode 2091.从数组中移除最大值和最小值](https://zhuanlan.zhihu.com/p/519995679) · 知乎 · 2022-05-25 · 赞同 0**
> 力扣：[2091. 从数组中移除最大值和最小值](https://leetcode.cn/problems/removing-minimum-and-maximum-from-array/) · Medium · 灵茶山艾府：[三种情况（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2091.从数组中移除最大值和最小值

[力扣](https://leetcode.cn/problems/removing-minimum-and-maximum-from-array/)

首先考虑边界情况。当数组长度为1时，只需要移除一次，因此答案就是1。

接下来对于一般情况，由于数组中每个数都不一样，因此当数组长度大于等于2时，最大值和最小值必然是不同的。不妨设这两个数的下标分别为p1和p2，对于p1和p2的求解，一趟遍历就能找出来。

由于题目对数字的移除规则与数字的大小无关，因此在这里p1和p2是可以互换的，那么不妨只考虑p1 \< p2的情况。此时要移除p1这个位置的数，可以选择先移除0到p1 - 1这些数，或者先移除p1 + 1到n - 1这些数，然后再移除p1。对于p2同样是可以选择先移除0到p2 - 1或者p2 + 1到n - 1这些数，然后再移除p2。

在这里规定了p1 \< p2，那么对于上面这些操作，综合起来就有三种较优的移除方案：

1、移除0到p2

这个方案显式地移除了p2，同时由于0 \<\= p1 \< p2，因此这种方案也能移除p1。一共需要p2 + 1次操作

2、移除p1到n - 1

这个方案显式地移除了p1，同时由于p1 \< p2 \<\= n - 1，因此这种方案也能移除p2。一共需要n - p1次操作

3、分别移除0到p1以及p2到n - 1

这个方案显式地移除了p1和p2。一共需要p1 + 1 + n - p2次操作

只需要从这三种方案中选择操作次数最少的方案即可。

最后附上python代码：

```python
class Solution(object):
    def minimumDeletions(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        if len(nums) == 1:
            return 1
        
        ma = mi = None
        for index, num in enumerate(nums):
            if ma is None or ma < num:
                p1 = index
                ma = num
            if mi is None or mi > num:
                p2 = index
                mi = num
        
        if p1 > p2:
            p1, p2 = p2, p1
        
        return min(p2 + 1, len(nums) - p1, p1 + 1 + len(nums) - p2)
```
