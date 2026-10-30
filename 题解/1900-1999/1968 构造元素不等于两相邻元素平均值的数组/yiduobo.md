---
title: "1968. 构造元素不等于两相邻元素平均值的数组"
aliases: ["yiduobo的每日leetcode 1968.构造元素不等于两相邻元素平均值的数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/数学算法", "题单/贪心算法", "题单/数学算法/六-随机算法", "题单/贪心算法/六-构造题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/495432493"
zhihu_id: "495432493"
zhihu_title: "yiduobo的每日leetcode 1968.构造元素不等于两相邻元素平均值的数组"
question_id: "1968"
question: "构造元素不等于两相邻元素平均值的数组"
problem_url: "https://leetcode.cn/problems/array-with-elements-not-equal-to-average-of-neighbors/"
difficulty: "Medium"
rating: 1499
created: "2022-04-08T23:24:19+08:00"
updated: "2022-04-08T23:24:19+08:00"
upvotes: 0
comments: 0
---

# 1968. 构造元素不等于两相邻元素平均值的数组

> **[yiduobo的每日leetcode 1968.构造元素不等于两相邻元素平均值的数组](https://zhuanlan.zhihu.com/p/495432493) · 知乎 · 2022-04-08 · 赞同 0**
> 力扣：[1968. 构造元素不等于两相邻元素平均值的数组](https://leetcode.cn/problems/array-with-elements-not-equal-to-average-of-neighbors/) · Medium · 灵茶山艾府：[排序后从中间分开，错开一位合并](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1968.构造元素不等于相邻元素平均值的数组

[力扣](https://leetcode-cn.com/problems/array-with-elements-not-equal-to-average-of-neighbors/)

题目要求给出任意结果，那么为了满足(nums[i - 1] + nums[i + 1) / 2 !\= nums[i]，一种最简单的构造思路就是按数值大小，一小一大依次混合排布，合法性也很好证明。

对于所有位于1到n - 1之间的位置i，若i为奇数，那么必然有nums[i] > nums[i - 1]，以及nums[i] > nums[i + 1]，因此nums[i]肯定不等于(nums[i - 1] + nums[i + 1]) / 2。同理，若i为偶数，那么必然有nums[i] \< nums[i - 1]，以及nums[i] \< nums[i + 1]，因此nums[i]也不等于(nums[i - 1] + nums[i + 1]) / 2。

另外，需要注意一种特殊情况，就是构造完之后发现与原数组一样，此时则可以选择将数组翻转从而得到不同于原数组的合法构造。

最后附上python代码：

```python
class Solution(object):
    def rearrangeArray(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        sorted_nums = sorted(nums)
        res = []
        l = 0
        r = len(nums) - 1
        while l < r:
            res.append(sorted_nums[l])
            res.append(sorted_nums[r])
            l += 1
            r -= 1
            if l == r:
                res.append(sorted_nums[l])
                
        if res == nums:
            res.reverse()
        
        return res
```
