---
title: "2778. 特殊元素平方和"
aliases: ["yiduobo的每日leetcode 2778.特殊元素平方和"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/655689387"
zhihu_id: "655689387"
zhihu_title: "yiduobo的每日leetcode 2778.特殊元素平方和"
question_id: "2778"
question: "特殊元素平方和"
problem_url: "https://leetcode.cn/problems/sum-of-squares-of-special-elements/"
difficulty: "Easy"
created: "2023-09-12T03:40:22+08:00"
updated: "2023-09-12T03:40:22+08:00"
upvotes: 0
comments: 0
---

# 2778. 特殊元素平方和

> **[yiduobo的每日leetcode 2778.特殊元素平方和](https://zhuanlan.zhihu.com/p/655689387) · 知乎 · 2023-09-12 · 赞同 0**
> 力扣：[2778. 特殊元素平方和](https://leetcode.cn/problems/sum-of-squares-of-special-elements/) · Easy · 灵茶山艾府：[两种方法：遍历/枚举因子](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2778.特殊元素平方和

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/sum-of-squares-of-special-elements/)

按照题目要求直接一趟遍历，对于当前遍历到的下标index，若其满足index + 1可以被数组长度整除，那么就将nums[index] \* nums[index]累加到答案中。

最后附上python代码：

```python
class Solution(object):
    def sumOfSquares(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0
        for index, v in enumerate(nums):
            if len(nums) % (index + 1) == 0:
                res += v * v
        
        return res
```
