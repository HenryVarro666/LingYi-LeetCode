---
title: "283. 移动零"
aliases: ["yiduobo的每日leetcode 283.移动零"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/stack", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/LeetCode-热题-100", "题单/滑动窗口与双指针/三-单序列双指针", "题单/LeetCode-热题-100/双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/154599342"
zhihu_id: "154599342"
zhihu_title: "yiduobo的每日leetcode 283.移动零"
question_id: "283"
question: "移动零"
problem_url: "https://leetcode.cn/problems/move-zeroes/"
difficulty: "Easy"
created: "2020-07-03T22:32:43+08:00"
updated: "2020-07-03T22:32:43+08:00"
upvotes: 0
comments: 0
---

# 283. 移动零

> **[yiduobo的每日leetcode 283.移动零](https://zhuanlan.zhihu.com/p/154599342) · 知乎 · 2020-07-03 · 赞同 0**
> 力扣：[283. 移动零](https://leetcode.cn/problems/move-zeroes/) · Easy · 灵茶山艾府：[两种方法：原地栈 / 交换元素（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

283.移动零<https://leetcode-cn.com/problems/move-zeroes/>

比较基础的题目。对于数组中X，0，0，0，...，0，Y的形式，我们需要将Y移动到这一串0的左侧，变成X，Y，0，0，...，0。可以发现，只需要将Y与最左侧的0交换即可。

于是在这里就只需要从左往右一趟扫描，维护住第一个零的位置。若当前数不为零，且存在第一个零，说明当前数前方必然存在一段零，于是将当前数与第一个零互换即可。交换后，第一个零的位置也需要对应地往后移动一位。

最后附上python代码：

```python
class Solution(object):
    def moveZeroes(self, nums):
        """
        :type nums: List[int]
        :rtype: None Do not return anything, modify nums in-place instead.
        """

        fisrt_zero = None
        for index, num in enumerate(nums):
            if num == 0:
                if fisrt_zero is None:
                    fisrt_zero = index
            else:
                if fisrt_zero is not None:
                    nums[fisrt_zero], nums[index] = nums[index], nums[fisrt_zero]
                    fisrt_zero += 1
```
