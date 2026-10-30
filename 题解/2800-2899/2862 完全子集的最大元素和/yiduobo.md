---
title: "2862. 完全子集的最大元素和"
aliases: ["yiduobo的每日leetcode 2862.完全子集的最大元素和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/661481123"
zhihu_id: "661481123"
zhihu_title: "yiduobo的每日leetcode 2862.完全子集的最大元素和"
question_id: "2862"
question: "完全子集的最大元素和"
problem_url: "https://leetcode.cn/problems/maximum-element-sum-of-a-complete-subset-of-indices/"
difficulty: "Hard"
rating: 2292
created: "2023-10-16T01:09:41+08:00"
updated: "2023-10-16T01:09:41+08:00"
upvotes: 0
comments: 0
---

# 2862. 完全子集的最大元素和

> **[yiduobo的每日leetcode 2862.完全子集的最大元素和](https://zhuanlan.zhihu.com/p/661481123) · 知乎 · 2023-10-16 · 赞同 0**
> 力扣：[2862. 完全子集的最大元素和](https://leetcode.cn/problems/maximum-element-sum-of-a-complete-subset-of-indices/) · Hard · 灵茶山艾府：[三种方法：按照 core 分组 / 枚举 core / 打表预处理（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2862.完全子集的最大元素和

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximum-element-sum-of-a-complete-subset-of-indices/)

首先，由于nums中的所有元素都是正数，因此在这里就应该尽量选择满的集合。更具体的说，对于样例2中的集合而言，在可以选择{1, 4, 9}的前提下就没有理由选择{1, 4}、{1, 9}、{4, 9}。

在这里不妨记所有小于等于数组长度n的完全平方数形成的集合为基础集合base，那么base本身是一个备选答案。除此之外，其他的备选答案必然都是在base的基础上对其中每个元素都乘以一个mul，这样一来才可以使得集合中的元素两两之间的乘积为完全平方数，同时保证新得到的集合是尽量满的。例如样例中的{1, 4, 9}，乘以2之后得到的是{2, 8, 18}，但是由于这里的18超出了数组的边界，因此只能保留{2, 8}这两个元素。

可以发现，随着mul越来越大，超出数组边界的元素将越来越多，因此可以从2开始向上枚举mul，当前mul对应的备选答案集合就可以在上一轮的基础上得到。具体实现上，可以不计算出具体的备选集合，而是只需不断弹出base集合中最大的元素，直到base中剩下元素的最大值乘以mul小于等于n为止。得到mul对应的备选集合后，一趟遍历计算集合中下标对应元素之和并更新答案即可。

由于候选集合的大小不超过sqrt(n)，而枚举mul的轮次为n - 1轮，因此这是一个O(n \* sqrt(n))的算法，足够处理本题了。

最后附上python代码：

```python
class Solution(object):
    def maximumSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        index_list = []
        x = 1
        n = len(nums)
        while x * x <= n:
            index_list.append(x * x)
            x += 1
        
        res = 0
        mul = 1
        while index_list:
            res = max(res, sum([nums[p * mul - 1] for p in index_list]))
            mul += 1
            while index_list and index_list[-1] * mul > n:
                index_list.pop()
        
        return res
```
