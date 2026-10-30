---
title: "2563. 统计公平数对的数目"
aliases: ["yiduobo的每日leetcode 2563.统计公平数对的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/binary-search", "题单/滑动窗口与双指针", "题单/二分算法", "题单/滑动窗口与双指针/三-单序列双指针", "题单/滑动窗口与双指针/五-三指针", "题单/二分算法/一-二分查找"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/640771625"
zhihu_id: "640771625"
zhihu_title: "yiduobo的每日leetcode 2563.统计公平数对的数目"
question_id: "2563"
question: "统计公平数对的数目"
problem_url: "https://leetcode.cn/problems/count-the-number-of-fair-pairs/"
difficulty: "Medium"
rating: 1721
created: "2023-07-01T02:11:00+08:00"
updated: "2023-07-01T02:11:00+08:00"
upvotes: 0
comments: 0
---

# 2563. 统计公平数对的数目

> **[yiduobo的每日leetcode 2563.统计公平数对的数目](https://zhuanlan.zhihu.com/p/640771625) · 知乎 · 2023-07-01 · 赞同 0**
> 力扣：[2563. 统计公平数对的数目](https://leetcode.cn/problems/count-the-number-of-fair-pairs/) · Medium · 灵茶山艾府：[三种方法：二分查找 / 相向三指针 / 两次相向双指针（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2563.统计公平数对的数目

[力扣](https://leetcode.cn/problems/count-the-number-of-fair-pairs/)

题目要求找出lower \<\= nums[i] + nums[j] \<\= upper的数对的数目，那么可以将其转化为nums[i] + nums[j] \<\= upper的数对数目减去nums[i] + nums[j] \<\= lower - 1的数对数目。

对于单个问题，可以直接套用与第一题两数之和类似的双指针法来求解。

具体实现上，可以逐位向右遍历左指针，同时维护两个右指针，分别适配upper以及lower - 1。随着左指针的增大，只需将两个右指针在上一轮的基础上分别向左移动到合适的位置即可。

最后附上python代码：

```python
class Solution(object):
    def countFairPairs(self, nums, lower, upper):
        """
        :type nums: List[int]
        :type lower: int
        :type upper: int
        :rtype: int
        """

        nums.sort()
        right_low = right_high = len(nums) - 1
        res = 0
        for left in range(len(nums)):
            while right_low > left and nums[left] + nums[right_low] > lower - 1:
                right_low -= 1
            while right_high > left and nums[left] + nums[right_high] > upper:
                right_high -= 1
            
            if right_high > left:
                res += right_high - left
            if right_low > left:
                res -= right_low - left
        
        return res
```
