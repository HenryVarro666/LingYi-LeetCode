---
title: "2154. 将找到的值乘以2"
aliases: ["yiduobo的每日leetcode 2154.将找到的值乘以2"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/hash-table", "题单/位运算", "题单/位运算/一-基础题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/530867149"
zhihu_id: "530867149"
zhihu_title: "yiduobo的每日leetcode 2154.将找到的值乘以2"
question_id: "2154"
question: "将找到的值乘以 2"
problem_url: "https://leetcode.cn/problems/keep-multiplying-found-values-by-two/"
difficulty: "Easy"
created: "2022-06-19T13:31:48+08:00"
updated: "2022-06-19T13:31:48+08:00"
upvotes: 0
comments: 0
---

# 2154. 将找到的值乘以2

> **[yiduobo的每日leetcode 2154.将找到的值乘以2](https://zhuanlan.zhihu.com/p/530867149) · 知乎 · 2022-06-19 · 赞同 0**
> 力扣：[2154. 将找到的值乘以 2](https://leetcode.cn/problems/keep-multiplying-found-values-by-two/) · Easy · 灵茶山艾府：[巧妙利用位运算优化空间复杂度：从 O(n) 到 O(log U) 到 O(1)](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2154.将找到的值乘以2

[力扣](https://leetcode.cn/problems/keep-multiplying-found-values-by-two/)

比较基础的题目，使用集合记录出现过的数字，然后从original开始迭代。若当前的original出现在集合中，那么就将original更新为original \* 2，然后重复此过程直到当前original不在集合中为止。

最后附上python代码：

```python
class Solution(object):
    def findFinalValue(self, nums, original):
        """
        :type nums: List[int]
        :type original: int
        :rtype: int
        """

        num_set = set(nums)
        while original in num_set:
            original += original
        
        return original
```
