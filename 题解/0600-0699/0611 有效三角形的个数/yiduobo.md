---
title: "611. 有效三角形的个数"
aliases: ["yiduobo的每日leetcode 611.有效三角形的个数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/数学算法", "题单/滑动窗口与双指针/三-单序列双指针", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/269289897"
zhihu_id: "269289897"
zhihu_title: "yiduobo的每日leetcode 611.有效三角形的个数"
question_id: "611"
question: "有效三角形的个数"
problem_url: "https://leetcode.cn/problems/valid-triangle-number/"
difficulty: "Medium"
created: "2020-10-27T23:15:04+08:00"
updated: "2020-10-27T23:15:04+08:00"
upvotes: 0
comments: 0
---

# 611. 有效三角形的个数

> **[yiduobo的每日leetcode 611.有效三角形的个数](https://zhuanlan.zhihu.com/p/269289897) · 知乎 · 2020-10-27 · 赞同 0**
> 力扣：[611. 有效三角形的个数](https://leetcode.cn/problems/valid-triangle-number/) · Medium · 灵茶山艾府：[三种方法：枚举最长边/枚举最短边/值域卷积（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

611.有效三角形的个数<https://leetcode-cn.com/problems/valid-triangle-number/>

有效三角形需要的是两条短边长度之和大于长边的长度，那么我们可以先将所有边排序，然后从大到小依次枚举长边的长度。确定长边之后，我们则需要在小于长边的其他数中找到所有和大于长边的数对。注意到这里已经拍过序了，因此可以利用单调性，直接使用类似两数之后的双指针法来做。

设长边的长度为l，当前左右指针分别指向left和right，那么有：

1、若nums[left] + nums[right] > l，由于现在nums是单调递增的，因此现在(left, right)，(left + 1, right)，... (right - 1, right)都是可行的组合，因此可以当次长边选择nums[right]时，一共有right - left组可行的答案。此时已经处理完了选择nums[right]作为次长边的所有情况，因此需要将right往左移动。

2、若nums[left] + nums[right] \<\= l，说明当前nums[left]的长度不够长，无法与nums[right]形成可行答案，因此需要将left往右移动。

重复这个过程，直到left和right相遇为止。

最后附上python代码：

```python
class Solution(object):
    def triangleNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        nums = sorted(nums)
        res = 0

        for index in range(len(nums) - 1, 1, -1):
            left = 0
            right = index - 1
            while left < right:
                if nums[left] + nums[right] > nums[index]:
                    res += right - left
                    right -= 1
                else:
                    left += 1
        
        return res
```
