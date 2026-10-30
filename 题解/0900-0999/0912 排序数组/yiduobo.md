---
title: "912. 排序数组"
aliases: ["yiduobo的每日leetcode 912.排序数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/divide-and-conquer", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/五-其他递归/分治"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/354962400"
zhihu_id: "354962400"
zhihu_title: "yiduobo的每日leetcode 912.排序数组"
question_id: "912"
question: "排序数组"
problem_url: "https://leetcode.cn/problems/sort-an-array/"
difficulty: "Medium"
created: "2021-03-05T23:32:59+08:00"
updated: "2021-03-05T23:32:59+08:00"
upvotes: 0
comments: 0
---

# 912. 排序数组

> **[yiduobo的每日leetcode 912.排序数组](https://zhuanlan.zhihu.com/p/354962400) · 知乎 · 2021-03-05 · 赞同 0**
> 力扣：[912. 排序数组](https://leetcode.cn/problems/sort-an-array/) · Medium · 灵茶山艾府：[O(nlogn) 快速排序+有序优化，附常见问题解答（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

912.排序数组

[力扣](https://leetcode-cn.com/problems/sort-an-array/)

基础的排序问题，使用常见的O(nlogn)的排序都是可以做的。不过注意到这里每个数的范围在-50000到50000之间，那么完全可以开一个大小为100001的数组来进行计数排序。当n为50000时计数排序的时间复杂度显然是更好的。

需要特别注意python没有常规意义下的负数下标，因此需要先将每个数加上50000，最后输出结果时再减去50000。

最后附上python代码：

```python
class Solution(object):
    def sortArray(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        num_cnt = [0] * 100001
        for num in nums:
            num_cnt[num + 50000] += 1
        
        res = []
        for num in range(0, 100001):
            if num_cnt[num] > 0:
                res.extend([num - 50000] * num_cnt[num])
        
        return res
```
