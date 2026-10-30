---
title: "3159. 查询数组中元素的出现位置"
aliases: ["yiduobo的每日leetcode 3159.查询数组中元素的出现位置"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/704364214"
zhihu_id: "704364214"
zhihu_title: "yiduobo的每日leetcode 3159.查询数组中元素的出现位置"
question_id: "3159"
question: "查询数组中元素的出现位置"
problem_url: "https://leetcode.cn/problems/find-occurrences-of-an-element-in-an-array/"
difficulty: "Medium"
created: "2024-06-20T00:07:10+08:00"
updated: "2024-06-20T00:07:10+08:00"
upvotes: 1
comments: 0
---

# 3159. 查询数组中元素的出现位置

> **[yiduobo的每日leetcode 3159.查询数组中元素的出现位置](https://zhuanlan.zhihu.com/p/704364214) · 知乎 · 2024-06-20 · 赞同 1**
> 力扣：[3159. 查询数组中元素的出现位置](https://leetcode.cn/problems/find-occurrences-of-an-element-in-an-array/) · Medium · 灵茶山艾府：[记录所有等于 x 的元素下标（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3159.查询数组中元素的出现位置

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-occurrences-of-an-element-in-an-array/description/)

题目给出一个整数数组nums，一个整数数组queries以及一个整数x，对于queries中的每个元素queries[i]，要求找出nums中第queries[i]个x的下标是多少，若queries[i]大于x在nums中出现的次数，则返回-1。

题目关心的是x在nums中的下标，那么就可以先对nums进行一趟遍历，将x出现的所有下标用一个数组pos收集起来。接下来对于queries中的每个询问，若queries[i]大于pos的长度，对应的答案就是-1，否则对应的答案就是pos中的第queries[i]个元素，即pos[queries[i] - 1]。

最后附上python代码：

```python
class Solution(object):
    def occurrencesOfElement(self, nums, queries, x):
        """
        :type nums: List[int]
        :type queries: List[int]
        :type x: int
        :rtype: List[int]
        """

        pos = []
        for index, v in enumerate(nums):
            if v == x:
                pos.append(index)
        
        res = []
        for q in queries:
            if q > len(pos):
                res.append(-1)
            else:
                res.append(pos[q - 1])
        
        return res
```
