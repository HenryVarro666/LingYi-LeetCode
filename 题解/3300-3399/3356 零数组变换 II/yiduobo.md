---
title: "3356. 零数组变换II"
aliases: ["yiduobo的每日leetcode 3356.零数组变换II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/segment-tree", "leetcode/two-pointers", "leetcode/binary-search", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/二-差分"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/26924595406"
zhihu_id: "26924595406"
zhihu_title: "yiduobo的每日leetcode 3356.零数组变换II"
question_id: "3356"
question: "零数组变换 II"
problem_url: "https://leetcode.cn/problems/zero-array-transformation-ii/"
difficulty: "Medium"
rating: 1913
created: "2025-02-28T01:02:49+08:00"
updated: "2025-02-28T01:02:49+08:00"
upvotes: 1
comments: 0
---

# 3356. 零数组变换II

> **[yiduobo的每日leetcode 3356.零数组变换II](https://zhuanlan.zhihu.com/p/26924595406) · 知乎 · 2025-02-28 · 赞同 1**
> 力扣：[3356. 零数组变换 II](https://leetcode.cn/problems/zero-array-transformation-ii/) · Medium · 灵茶山艾府：[三种方法：二分答案+差分数组 / Lazy 线段树 / 双指针（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3356.零数组变换II

[3356. 零数组变换 II - 力扣（LeetCode）](https://leetcode.cn/problems/zero-array-transformation-ii/description/)

题目给出一个长度为n的整数数组nums，以及一个二维数组queries，其中queries\[i\] \= \[l\[i\], r\[i\], val\[i\]\]。

对于每个查询queries\[i\]，可以在下标范围\[l\[i\], r\[i\]\]中选择一个下标子集，将这些下标对应的元素最多减去val\[i\]，每个下标减去的值都可以独立选择。

现在要求找出一个最小的k，使得在执行queries中的前k个查询后，nums将全变为0。

之前3356题的升级版

[yiduobo：yiduobo的每日leetcode 3355.零数组变换I](https://zhuanlan.zhihu.com/p/26921398165)

每次操作多出了一个val。但是根据题目的描述可以发现，由于每个下标减去的值都可以独立选择，那么实际上这里的queries[i]就可以认为是执行了val[i]次3355题中的操作，换言之，在这里依然可以利用差分数组来计算是否能够覆盖。

另一方面，对于某次操作，如果不选择任何下标进行操作的话并不会影响nums数组，也就是说题目中的操作没有负面效果，操作的数量越多就越有可能让nums变为全0，符合单调性。于是在这里可以二分操作的数量k，接下来针对前k个queries，使用之前3355题中的方法检测通过这k次查询能否使得nums变为全0，根据对应的结果修正二分的上下边界即可。

具体实现上，二分的下界自然是0，而上界则可以设置为queries的长度再加上1，用来表示不存在k的情况。

最后附上python代码：

```python
class Solution(object):
    def minZeroArray(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: int
        """
        
        n = len(nums)

        def check(mid):
            f = [0] * n
            for x, y, v in queries[:mid]:
                f[x] += v
                if y + 1 < n:
                    f[y + 1] -= v
        
            now = 0
            for index in range(n):
                now += f[index]
                if now < nums[index]:
                    return False
            return True
        
        left = 0
        right = len(queries) + 1
        while left < right:
            mid = (left + right) // 2
            if check(mid):
                right = mid
            else:
                left = mid + 1
        
        if left == len(queries) + 1:
            return -1
        return left
```
