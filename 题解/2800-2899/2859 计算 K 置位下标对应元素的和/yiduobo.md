---
title: "2859. 计算K置位下标对应元素的和"
aliases: ["yiduobo的每日leetcode 2859.计算K置位下标对应元素的和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/661367834"
zhihu_id: "661367834"
zhihu_title: "yiduobo的每日leetcode 2859.计算K置位下标对应元素的和"
question_id: "2859"
question: "计算 K 置位下标对应元素的和"
problem_url: "https://leetcode.cn/problems/sum-of-values-at-indices-with-k-set-bits/"
difficulty: "Easy"
created: "2023-10-15T03:48:39+08:00"
updated: "2023-10-15T03:48:39+08:00"
upvotes: 0
comments: 0
---

# 2859. 计算K置位下标对应元素的和

> **[yiduobo的每日leetcode 2859.计算K置位下标对应元素的和](https://zhuanlan.zhihu.com/p/661367834) · 知乎 · 2023-10-15 · 赞同 0**
> 力扣：[2859. 计算 K 置位下标对应元素的和](https://leetcode.cn/problems/sum-of-values-at-indices-with-k-set-bits/) · Easy · 灵茶山艾府：[库函数写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2859.计算K置位下标对应元素的和

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/sum-of-values-at-indices-with-k-set-bits/)

直接按照题目的描述一趟遍历，对于当前遍历到的下标index对应的数字v，计算index二进制表示中1的数目cnt，若cnt等于k，那么就将v累加到答案中。至于cnt的计算方法，则可以将其转化为二进制后逐位分离计算，也可以通过lowbit操作不断分离出最低位的1来进行计算。

最后附上python代码：

```python
class Solution(object):
    def sumIndicesWithKSetBits(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        res = 0
        for index, v in enumerate(nums):
            cnt = 0
            while index:
                cnt += 1
                index -= index & -index

            if cnt == k:
                res += v
        
        return res
```
