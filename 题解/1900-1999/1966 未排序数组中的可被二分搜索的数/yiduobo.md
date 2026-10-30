---
title: "1966. 未排序数组中的可被二分搜索的数"
aliases: ["yiduobo的每日leetcode 1966.未排序数组中的可被二分搜索的数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/624090380"
zhihu_id: "624090380"
zhihu_title: "yiduobo的每日leetcode 1966.未排序数组中的可被二分搜索的数"
question_id: "1966"
question: "未排序数组中的可被二分搜索的数"
problem_url: "https://leetcode.cn/problems/binary-searchable-numbers-in-an-unsorted-array/"
created: "2023-04-23T04:15:49+08:00"
updated: "2023-04-23T04:15:49+08:00"
upvotes: 0
comments: 0
---

# 1966. 未排序数组中的可被二分搜索的数

> **[yiduobo的每日leetcode 1966.未排序数组中的可被二分搜索的数](https://zhuanlan.zhihu.com/p/624090380) · 知乎 · 2023-04-23 · 赞同 0**
> 力扣：[1966. 未排序数组中的可被二分搜索的数](https://leetcode.cn/problems/binary-searchable-numbers-in-an-unsorted-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1966.未排序数组中的可被二分搜索的数

[力扣](https://leetcode.cn/problems/binary-searchable-numbers-in-an-unsorted-array/)

观察题目中给出的代码可以发现，若某一轮选择的pivot位于target右侧，且pivot \< target，或者pivot位于target左侧，且pivot > target，那么target就会被误删。

换言之，只有一个数v左侧存在比v更大的数，或者右侧存在比v更小的数，那么v就无法被搜索到，于是只需正反两趟遍历就可以确定数组中的每个数是否可以被搜索到了。

最后附上python代码：

```python
class Solution(object):
    def binarySearchableNumbers(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        remove = [False] * n
        ma = nums[0]
        for index in range(1, n):
            if nums[index] < ma:
                remove[index] = True
            ma = max(ma, nums[index])
        
        mi = nums[-1]
        for index in range(n - 2, -1, -1):
            if nums[index] > mi:
                remove[index] = True
            mi = min(mi, nums[index])
        
        res = n
        for index in range(n):
            if remove[index]:
                res -= 1
        
        return res
```
