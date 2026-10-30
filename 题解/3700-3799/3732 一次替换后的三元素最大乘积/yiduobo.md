---
title: "3732. 一次替换后的三元素最大乘积"
aliases: ["yiduobo的每日leetcode 3732.一次替换后的三元素最大乘积"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1968506700198830200"
zhihu_id: "1968506700198830200"
zhihu_title: "yiduobo的每日leetcode 3732.一次替换后的三元素最大乘积"
question_id: "3732"
question: "一次替换后的三元素最大乘积"
problem_url: "https://leetcode.cn/problems/maximum-product-of-three-elements-after-one-replacement/"
difficulty: "Medium"
rating: 1529
created: "2025-11-03T19:39:17+08:00"
updated: "2025-11-03T19:39:20+08:00"
upvotes: 2
comments: 0
---

# 3732. 一次替换后的三元素最大乘积

> **[yiduobo的每日leetcode 3732.一次替换后的三元素最大乘积](https://zhuanlan.zhihu.com/p/1968506700198830200) · 知乎 · 2025-11-03 · 赞同 2**
> 力扣：[3732. 一次替换后的三元素最大乘积](https://leetcode.cn/problems/maximum-product-of-three-elements-after-one-replacement/) · Medium · 灵茶山艾府：[O(n) 求绝对值前二大（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3732.一次替换后的三元素最大乘积

[3732. 一次替换后的三元素最大乘积 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-product-of-three-elements-after-one-replacement/description/)

题目给出一个整数数组nums，其中的元素都在-10^5到10^5之间。

现在要求将其中某个元素替换为-10^5到10^5之间的某个整数，在替换后，需要从nums中选出三个下标互不相同的整数，并计算这三个元素的乘积。

问可能得到的最大乘积是多少。

由于nums中元素大小的绝对值都不超过10^5，因此最终的结果一定是nums中的某两个元素，再配合上被替换后的10^5或者-10^5。若选出的这两个元素之积小于0，就替换另一个元素为-10^5，否则替换另一个元素为10^5。更进一步的，对于nums中选出的两个元素，应该让它们乘积的绝对值最大，这样一来配合上替换的元素才能使得乘积最大。

基于上面的结论，只需一趟遍历，找出nums中绝对值最大的两个元素，分别记它们的绝对值为first以及second，那么最终答案就是first \* second \* 10^5。

最后附上python代码：

```python
class Solution(object):
    def maxProduct(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        first, second = None, None
        for v in nums:
            v = abs(v)
            if first is None or v > first:
                first, second = v, first
            elif second is None or v > second:
                second = v
        
        return first * second * 100000
```
