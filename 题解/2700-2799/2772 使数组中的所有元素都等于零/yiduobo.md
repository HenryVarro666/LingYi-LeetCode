---
title: "2772. 使数组中的所有元素都等于零"
aliases: ["yiduobo的每日leetcode 2772.使数组中的所有元素都等于零"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/常用数据结构", "题单/常用数据结构/二-差分"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/655463992"
zhihu_id: "655463992"
zhihu_title: "yiduobo的每日leetcode 2772.使数组中的所有元素都等于零"
question_id: "2772"
question: "使数组中的所有元素都等于零"
problem_url: "https://leetcode.cn/problems/apply-operations-to-make-all-array-elements-equal-to-zero/"
difficulty: "Medium"
rating: 2029
created: "2023-09-11T05:11:14+08:00"
updated: "2023-09-11T05:11:14+08:00"
upvotes: 0
comments: 0
---

# 2772. 使数组中的所有元素都等于零

> **[yiduobo的每日leetcode 2772.使数组中的所有元素都等于零](https://zhuanlan.zhihu.com/p/655463992) · 知乎 · 2023-09-11 · 赞同 0**
> 力扣：[2772. 使数组中的所有元素都等于零](https://leetcode.cn/problems/apply-operations-to-make-all-array-elements-equal-to-zero/) · Medium · 灵茶山艾府：[差分数组（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2772.使数组中的所有元素都等于零

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/apply-operations-to-make-all-array-elements-equal-to-zero/)

题目每次只能将长度为k的一个子数组中的数同时减去1，那么对于数组中最左侧的非0元素，就只能选择以该元素为左边界的长度为k的子数组来执行若干次减法，而这个次数就是这个元素的值。当这个值为0后，只需继续向后找到下一个非0的值重复该操作。若过程中遇到了某个值为负数的元素，或者最后k - 1个元素中存在值不为0的元素，那么就说明无解。

到了这里，问题就转化成了一个区间修改，单点求值的问题。不过需要注意的是，由于每个位置值在求解之前的修改都来自于其左侧某个位置求解后为了变为0所做的操作，也就是说每个位置的修改都必然出现在求解该位置的值之前，因此在这里不需要使用logn的数据结构，只需要使用常规的差分数组就行了。

最后附上python代码：

```python
class Solution(object):
    def checkArray(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: bool
        """

        n = len(nums)
        f = [0] * n
        now = 0

        for index, v in enumerate(nums):
            now += f[index]
            if v < now:
                return False
            
            delta = v - now
            if delta > 0 and index + k > n:
                return False
            
            now = v
            if index + k < n:
                f[index + k] -= delta

        return True
```
