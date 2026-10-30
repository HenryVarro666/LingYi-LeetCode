---
title: "2811. 判断是否能拆分数组"
aliases: ["yiduobo的每日leetcode 2811.判断是否能拆分数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/658058529"
zhihu_id: "658058529"
zhihu_title: "yiduobo的每日leetcode 2811.判断是否能拆分数组"
question_id: "2811"
question: "判断是否能拆分数组"
problem_url: "https://leetcode.cn/problems/check-if-it-is-possible-to-split-array/"
difficulty: "Medium"
rating: 1543
created: "2023-09-24T01:20:11+08:00"
updated: "2023-09-24T01:20:11+08:00"
upvotes: 0
comments: 0
---

# 2811. 判断是否能拆分数组

> **[yiduobo的每日leetcode 2811.判断是否能拆分数组](https://zhuanlan.zhihu.com/p/658058529) · 知乎 · 2023-09-24 · 赞同 0**
> 力扣：[2811. 判断是否能拆分数组](https://leetcode.cn/problems/check-if-it-is-possible-to-split-array/) · Medium · 灵茶山艾府：[脑筋急转弯（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2811.判断是否能拆分数组

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/check-if-it-is-possible-to-split-array/)

题目的数据规模不大，可以允许O(n^3)的算法运行，因此一开始的想法就是通过区间记忆化搜索来尝试构造出一种分离方案，相对比较复杂。但是实际上本题暗藏一个条件，想清楚之后就变得很简单了。

注意到题目要求将长度为n的数组切分若干次，直到得到n个长度为1的子数组，那么无论怎么切分，一定会至少执行一次下面的操作：将一个长度为2的子数组切分成两个长度为1的子数组。这也就意味着这个长度为2的子数组之和必须大于等于m，即原数组中必须要至少存在一组相邻元素之和大于等于m。

另一方面，由于数组元素都是正数，那么包含上面这两个相邻元素的子数组之和也一定大于等于m，于是只需以这两个相邻元素为中心，不断将两侧长度为1的子数组分离出去，直到剩下这两个元素为止。期间每次分离的结果都是一个长度为1的子数组，以及另一个包含这两个相邻元素的子数组，其中后者的数组之和必然大于等于m，因此每一轮都是合法的。到最后剩下这两个元素时，再执行最后这次分离操作就行了。

根据上面的结论，就只需要一趟遍历，寻找数组中是否存在两个相邻元素之和大于等于m，若存在，那么答案就是true，否则就是false。

最后附上python代码：

```python
class Solution(object):
    def canSplitArray(self, nums, m):
        """
        :type nums: List[int]
        :type m: int
        :rtype: bool
        """

        if len(nums) <= 2:
            return True

        for index in range(1, len(nums)):
            if nums[index] + nums[index - 1] >= m:
                return True
        
        return False
```
