---
title: "2519. 统计K-Big索引的数量"
aliases: ["yiduobo的每日leetcode 2519.统计K-Big索引的数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/632917619"
zhihu_id: "632917619"
zhihu_title: "yiduobo的每日leetcode 2519.统计K-Big索引的数量"
question_id: "2519"
question: "统计K-Big索引的数量"
problem_url: "https://leetcode.cn/problems/count-the-number-of-k-big-indices/"
created: "2023-05-29T02:45:16+08:00"
updated: "2023-05-29T02:45:16+08:00"
upvotes: 0
comments: 0
---

# 2519. 统计K-Big索引的数量

> **[yiduobo的每日leetcode 2519.统计K-Big索引的数量](https://zhuanlan.zhihu.com/p/632917619) · 知乎 · 2023-05-29 · 赞同 0**
> 力扣：[2519. 统计K-Big索引的数量](https://leetcode.cn/problems/count-the-number-of-k-big-indices/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2519.统计K-Big索引的数量

[力扣](https://leetcode.cn/problems/count-the-number-of-k-big-indices/)

题目要求找出数组中所有下标i，满足i左侧以及i右侧都有至少k个数小于等于nums[i]。

对于这个问题，可以将左右两侧分开计算，即正反分别遍历，使用树状数组记录前缀或后缀中出现过的数，然后利用树状数组判断左侧或右侧是否至少有k个数小于nums[i]。最后再一趟遍历，统计左右两侧都满足条件的下标位置的数量即可。

最后附上python代码：

```python
class Solution(object):
    def kBigIndices(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        def get(x):
            s = 0
            while x > 0:
                s += f[x]
                x -= x & -x
            return s
        
        def add(x):
            while x <= 100000:
                f[x] += 1
                x += x & -x

        n = len(nums)

        f = [0] * 100001
        left = [False] * 100000
        for index in range(n):
            if get(nums[index] - 1) >= k:
                left[index] = True
            
            add(nums[index])
        
        f = [0] * 100001
        right = [False] * 100000
        for index in range(n - 1, -1, -1):
            if get(nums[index] - 1) >= k:
                right[index] = True
            
            add(nums[index])

        res = 0
        for index in range(n):
            if left[index] and right[index]:
                res += 1
        
        return res
```
