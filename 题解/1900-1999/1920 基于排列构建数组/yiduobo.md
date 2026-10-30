---
title: "1920. 基于排列构建数组"
aliases: ["yiduobo的每日leetcode 1920.基于排列构建数组"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/484294622"
zhihu_id: "484294622"
zhihu_title: "yiduobo的每日leetcode 1920.基于排列构建数组"
question_id: "1920"
question: "基于排列构建数组"
problem_url: "https://leetcode.cn/problems/build-array-from-permutation/"
difficulty: "Easy"
created: "2022-03-20T19:50:14+08:00"
updated: "2022-03-20T19:50:14+08:00"
upvotes: 0
comments: 0
---

# 1920. 基于排列构建数组

> **[yiduobo的每日leetcode 1920.基于排列构建数组](https://zhuanlan.zhihu.com/p/484294622) · 知乎 · 2022-03-20 · 赞同 0**
> 力扣：[1920. 基于排列构建数组](https://leetcode.cn/problems/build-array-from-permutation/) · Easy · 灵茶山艾府：[进阶问题解法：数字搬家，O(1) 空间（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1920.基于排列构建数组

[力扣](https://leetcode-cn.com/problems/build-array-from-permutation/)

比较基础的题目，直接一趟遍历，根据题目要求填充答案数组即可。

最后附上python代码：

```python
class Solution(object):
    def buildArray(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        res = []
        for index in range(len(nums)):
            res.append(nums[nums[index]])
        
        return res
```
