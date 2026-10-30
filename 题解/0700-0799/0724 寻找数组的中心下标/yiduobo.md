---
title: "724. 寻找数组的中心索引"
aliases: ["yiduobo的每日leetcode 724.寻找数组的中心索引"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/bian-li", "题单/动态规划", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/333979247"
zhihu_id: "333979247"
zhihu_title: "yiduobo的每日leetcode 724.寻找数组的中心索引"
question_id: "724"
question: "寻找数组的中心下标"
problem_url: "https://leetcode.cn/problems/find-pivot-index/"
difficulty: "Easy"
created: "2020-12-07T23:05:57+08:00"
updated: "2020-12-07T23:05:57+08:00"
upvotes: 1
comments: 0
---

# 724. 寻找数组的中心索引

> **[yiduobo的每日leetcode 724.寻找数组的中心索引](https://zhuanlan.zhihu.com/p/333979247) · 知乎 · 2020-12-07 · 赞同 1**
> 力扣：[724. 寻找数组的中心下标](https://leetcode.cn/problems/find-pivot-index/) · Easy · 灵茶山艾府：[简洁写法，O(1) 额外空间（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

724.寻找数组的中心索引

[力扣](https://leetcode-cn.com/problems/find-pivot-index/)

比较基础的题目，首先计算出数组中元素的总和，然后从头开始往后遍历同时进行累加，若当前的累加和乘以2等于元素总和减去当前元素值，那么当前下标即为答案，否则将当前元素累加进累加和。

最后附上python代码：

```python
class Solution(object):
    def pivotIndex(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        if not nums:
            return -1

        s = sum(nums)
        now = 0
        for index, num in enumerate(nums):
            if s - num == now + now:
                return index
            now += num
        
        return -1
```
