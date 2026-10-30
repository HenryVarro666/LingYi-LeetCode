---
title: "2936. 包含相等值数字块的数量"
aliases: ["yiduobo的每日leetcode 2936.包含相等值数字块的数量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "题单/二分算法", "题单/贪心算法", "题单/二分算法/四-其他", "题单/贪心算法/七-交互题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/690887217"
zhihu_id: "690887217"
zhihu_title: "yiduobo的每日leetcode 2936.包含相等值数字块的数量"
question_id: "2936"
question: "包含相等值数字块的数量"
problem_url: "https://leetcode.cn/problems/number-of-equal-numbers-blocks/"
difficulty: "Medium"
created: "2024-04-06T04:04:34+08:00"
updated: "2024-04-06T04:04:34+08:00"
upvotes: 1
comments: 0
---

# 2936. 包含相等值数字块的数量

> **[yiduobo的每日leetcode 2936.包含相等值数字块的数量](https://zhuanlan.zhihu.com/p/690887217) · 知乎 · 2024-04-06 · 赞同 1**
> 力扣：[2936. 包含相等值数字块的数量](https://leetcode.cn/problems/number-of-equal-numbers-blocks/) · Medium · 灵茶山艾府：[库函数简洁写法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2936.包含相等值数字块的数量

[. - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-equal-numbers-blocks/description/)

题目要求计算给出的数组中包含多少个数字块，那么一个自然的想法就是从左向右逐个进行分离。对于最左侧的数字块，最开始可以确定的就是这个数字块中的数值是多少，也就是剩余数组中最左侧元素的数值。

得到这个数值后，不妨设其为v，那么接下来就是需要找到v在数组中最后一次出现的下标。由于数组是单调不减的，因此可以使用二分法来找到这个下标。这样一来，最左侧的数字块就分离出去了。

而对于剩下的数组，则可以不断使用上面的方法分离最左侧的数字块，直到全部分离为止。

最后附上python代码：

```python
# Definition for BigArray.
# class BigArray:
#     def at(self, index):
#         pass
#     def size(self):
#         pass
class Solution(object):
    def countBlocks(self, nums):
        """
        :type nums: BigArray
        :rtype: int
        """
        
        n = nums.size()
        p = 0
        res = 0
        while p < n:
            left, right = p, n - 1
            v = nums.at(p)
            while left < right:
                mid = (left + right + 1) // 2
                if nums.at(mid) == v:
                    left = mid
                else:
                    right = mid - 1
                
            res += 1
            p = left + 1
        
        return res
```
