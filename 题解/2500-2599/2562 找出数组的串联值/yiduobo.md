---
title: "2562. 找出数组的串联值"
aliases: ["yiduobo的每日leetcode 2562.找出数组的串联值"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/two-pointers"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/640525402"
zhihu_id: "640525402"
zhihu_title: "yiduobo的每日leetcode 2562.找出数组的串联值"
question_id: "2562"
question: "找出数组的串联值"
problem_url: "https://leetcode.cn/problems/find-the-array-concatenation-value/"
difficulty: "Easy"
created: "2023-06-30T02:04:19+08:00"
updated: "2023-06-30T02:04:19+08:00"
upvotes: 0
comments: 0
---

# 2562. 找出数组的串联值

> **[yiduobo的每日leetcode 2562.找出数组的串联值](https://zhuanlan.zhihu.com/p/640525402) · 知乎 · 2023-06-30 · 赞同 0**
> 力扣：[2562. 找出数组的串联值](https://leetcode.cn/problems/find-the-array-concatenation-value/) · Easy · 灵茶山艾府：[O(1) 空间写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2562.找出数组的串联值

[力扣](https://leetcode.cn/problems/find-the-array-concatenation-value/)

按照题目描述，从两侧向中间遍历数组，每一轮都将遍历到的两个数拼接起来累加到最终答案中。需要注意数组长度为奇数的情况，此时需要额外将数组正中间的数也累加到答案中。

最后附上python代码：

```python
class Solution(object):
    def findTheArrayConcVal(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0
        left = 0
        right = len(nums) - 1
        while left < right:
            res += int(str(nums[left]) + str(nums[right]))
            left += 1
            right -= 1
        
        if left == right:
            res += nums[left]
        
        return res
```
