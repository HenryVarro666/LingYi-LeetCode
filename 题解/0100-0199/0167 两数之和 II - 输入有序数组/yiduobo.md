---
title: "167. 两数之和II - 输入有序数组"
aliases: ["yiduobo的每日leetcode 167.两数之和II - 输入有序数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/shi-pin", "题单/滑动窗口与双指针", "题单/面试经典-150-题", "题单/滑动窗口与双指针/三-单序列双指针", "题单/面试经典-150-题/双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/144614658"
zhihu_id: "144614658"
zhihu_title: "yiduobo的每日leetcode 167.两数之和II - 输入有序数组"
question_id: "167"
question: "两数之和 II - 输入有序数组"
problem_url: "https://leetcode.cn/problems/two-sum-ii-input-array-is-sorted/"
difficulty: "Medium"
created: "2020-05-29T23:17:55+08:00"
updated: "2020-05-29T23:17:55+08:00"
upvotes: 0
comments: 0
---

# 167. 两数之和II - 输入有序数组

> **[yiduobo的每日leetcode 167.两数之和II - 输入有序数组](https://zhuanlan.zhihu.com/p/144614658) · 知乎 · 2020-05-29 · 赞同 0**
> 力扣：[167. 两数之和 II - 输入有序数组](https://leetcode.cn/problems/two-sum-ii-input-array-is-sorted/) · Medium · 灵茶山艾府：[【视频】双指针想不明白？一个视频讲透！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

167.两数之和II - 输入有序数组<https://leetcode-cn.com/problems/two-sum-ii-input-array-is-sorted/>

与第一题相同（传送门在这里[yiduobo：yiduobo的每日leetcode 1.两数之和](https://zhuanlan.zhihu.com/p/112037601)），这里已经排好序了，依然是双指针从两端往中间扫即可。

需要注意python数组下标从0，但是题目这里面是从1开始的。

最后附上python代码：

```python
class Solution(object):
    def twoSum(self, numbers, target):
        """
        :type numbers: List[int]
        :type target: int
        :rtype: List[int]
        """

        l = 0
        r = len(numbers) - 1

        while l < r:
            now = numbers[l] + numbers[r]
            if now == target:
                return l + 1, r + 1
            elif now > target:
                r -= 1
            else:
                l += 1
```
