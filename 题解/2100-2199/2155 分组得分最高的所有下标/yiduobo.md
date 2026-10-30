---
title: "2155. 分组得分最高的所有下标"
aliases: ["yiduobo的每日leetcode 2155.分组得分最高的所有下标"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/array"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/530870457"
zhihu_id: "530870457"
zhihu_title: "yiduobo的每日leetcode 2155.分组得分最高的所有下标"
question_id: "2155"
question: "分组得分最高的所有下标"
problem_url: "https://leetcode.cn/problems/all-divisions-with-the-highest-score-of-a-binary-array/"
difficulty: "Medium"
created: "2022-06-19T13:45:28+08:00"
updated: "2022-06-19T13:45:28+08:00"
upvotes: 1
comments: 0
---

# 2155. 分组得分最高的所有下标

> **[yiduobo的每日leetcode 2155.分组得分最高的所有下标](https://zhuanlan.zhihu.com/p/530870457) · 知乎 · 2022-06-19 · 赞同 1**
> 力扣：[2155. 分组得分最高的所有下标](https://leetcode.cn/problems/all-divisions-with-the-highest-score-of-a-binary-array/) · Medium · 灵茶山艾府：[计算前后缀 + 简洁写法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2155.分组得分最高的所有下标

[力扣](https://leetcode.cn/problems/all-divisions-with-the-highest-score-of-a-binary-array/)

题目要求将数组分为两个部分，使得左半部分中的0的数目加上右半部分中1的数目最多。

对于这类问题，经典做法就是利用前缀和。

左半部分中0的数目，就等于左半部分的长度减去左半部分中1的数目，也就是左半部分的前缀和。右半部分中1的数目，就等于全体1的数目减去左半部分中1的数目，也就是总和减去左半部分的前缀和。也就是说，只需要一趟遍历，在过程中计算左半部分的前缀和，然后利用上面这两个结论计算左半部分的0以及右半部分的1并更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxScoreIndices(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        all_one = sum(nums)
        max_s = all_one
        res = [0]

        now_one = 0
        for index, num in enumerate(nums):
            now_one += num
            now_s = index + 1 - now_one + all_one - now_one
            if now_s > max_s:
                max_s = now_s
                res = [index + 1]
            elif now_s == max_s:
                res.append(index + 1)
        
        return res
```
