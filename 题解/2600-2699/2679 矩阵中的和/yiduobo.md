---
title: "2679. 矩阵中的和"
aliases: ["yiduobo的每日leetcode 2679.矩阵中的和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/649532690"
zhihu_id: "649532690"
zhihu_title: "yiduobo的每日leetcode 2679.矩阵中的和"
question_id: "2679"
question: "矩阵中的和"
problem_url: "https://leetcode.cn/problems/sum-in-a-matrix/"
difficulty: "Medium"
created: "2023-08-11T23:34:59+08:00"
updated: "2023-08-11T23:34:59+08:00"
upvotes: 0
comments: 0
---

# 2679. 矩阵中的和

> **[yiduobo的每日leetcode 2679.矩阵中的和](https://zhuanlan.zhihu.com/p/649532690) · 知乎 · 2023-08-11 · 赞同 0**
> 力扣：[2679. 矩阵中的和](https://leetcode.cn/problems/sum-in-a-matrix/) · Medium · 灵茶山艾府：[排序（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2679.矩阵中的和

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/sum-in-a-matrix/description/)

遍历每一行，将每行都从大到小进行排序。接下来遍历每一列，每次选出当前列中的最大值累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def matrixSum(self, nums):
        """
        :type nums: List[List[int]]
        :rtype: int
        """

        res = 0

        for line in nums:
            line.sort(reverse=True)
        
        for j in range(len(nums[0])):
            v = 0
            for i in range(len(nums)):
                v = max(v, nums[i][j])
            
            res += v
        
        return res
```
