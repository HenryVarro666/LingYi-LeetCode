---
title: "905. 按奇偶排序数组"
aliases: ["yiduobo的每日leetcode 905.按奇偶排序数组"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/353865346"
zhihu_id: "353865346"
zhihu_title: "yiduobo的每日leetcode 905.按奇偶排序数组"
question_id: "905"
question: "按奇偶排序数组"
problem_url: "https://leetcode.cn/problems/sort-array-by-parity/"
difficulty: "Easy"
created: "2021-03-01T22:23:51+08:00"
updated: "2021-03-01T22:23:51+08:00"
upvotes: 0
comments: 0
---

# 905. 按奇偶排序数组

> **[yiduobo的每日leetcode 905.按奇偶排序数组](https://zhuanlan.zhihu.com/p/353865346) · 知乎 · 2021-03-01 · 赞同 0**
> 力扣：[905. 按奇偶排序数组](https://leetcode.cn/problems/sort-array-by-parity/) · Easy · 灵茶山艾府：[相向双指针（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

905.按奇偶排序数组

[力扣](https://leetcode-cn.com/problems/sort-array-by-parity/)

题目要求将数组中的所有偶数排到所有奇数的前面，可以使用两个指针l和r分别从左右两侧开始向另一侧扫描。

1、若当前l小于r，且A[l]为偶数，那么将l向右移动直到l等于r或A[l]为奇数；同样地，若当前r大于l，且A[r]为奇数，那么将r向左移动直到等于l或者A[r]为偶数

2、若此时的l小于r，那么说明A[l]为奇数，A[r]为偶数，于是应该将其进行交换，同时l往右移动，r往左移动

3、重复上面的过程直到l大于等于r为止

最后附上python代码：

```python
class Solution(object):
    def sortArrayByParity(self, A):
        """
        :type A: List[int]
        :rtype: List[int]
        """

        l = 0
        r = len(A) - 1
        while l < r:
            while l < r and A[l] % 2 == 0:
                l += 1
            while r > l and A[r] % 2 == 1:
                r -= 1
            if l < r:
                A[l], A[r] = A[r], A[l]
                l += 1
                r -= 1
        
        return A
```
