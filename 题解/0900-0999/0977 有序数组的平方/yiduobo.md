---
title: "977. 有序数组的平方"
aliases: ["yiduobo的每日leetcode 977.有序数组的平方"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/362769934"
zhihu_id: "362769934"
zhihu_title: "yiduobo的每日leetcode 977.有序数组的平方"
question_id: "977"
question: "有序数组的平方"
problem_url: "https://leetcode.cn/problems/squares-of-a-sorted-array/"
difficulty: "Easy"
created: "2021-04-06T22:41:55+08:00"
updated: "2021-04-06T22:41:55+08:00"
upvotes: 0
comments: 0
---

# 977. 有序数组的平方

> **[yiduobo的每日leetcode 977.有序数组的平方](https://zhuanlan.zhihu.com/p/362769934) · 知乎 · 2021-04-06 · 赞同 0**
> 力扣：[977. 有序数组的平方](https://leetcode.cn/problems/squares-of-a-sorted-array/) · Easy · 灵茶山艾府：[相向双指针：从大到小合并（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

977.有序数组的平方

[力扣](https://leetcode-cn.com/problems/squares-of-a-sorted-array/)

题目要求按平方大小排序后输出，对于一个数而言，其绝对值越大平方就越大。在这里，nums是呈现出一个绝对值单调递减然后再单调递增的过程，因此当前nums中平方最大的数必然出现在头部或者尾部，于是可以使用两个指针l和r从两端开始向中间扫描。若此时nums[l]的平方大于nums[r]的平方，那么就将nums[l]的平方加入答案，同时将l向后移动一位；反之则将nums[r]的平方加入答案，同时将r向前移动一位。当l大于r时扫描结束，此时得到的答案就是从大到小排列的平方，于是只需将答案倒转后返回即可。

最后附上python代码：

```python
class Solution(object):
    def sortedSquares(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        l = 0
        r = len(nums) - 1
        res = []
        while l <= r:
            if nums[l] ** 2 > nums[r] ** 2:
                res.append(nums[l] ** 2)
                l += 1
            else:
                res.append(nums[r] ** 2)
                r -= 1
        
        return res[::-1]
```
