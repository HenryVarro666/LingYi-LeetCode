---
title: "4065. 移除不同值重排数组"
aliases: ["yiduobo的每日leetcode 4065.移除不同值重排数组"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/sorting", "leetcode/simulation", "leetcode/bao-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2088747088179943260"
zhihu_id: "2088747088179943260"
zhihu_title: "yiduobo的每日leetcode 4065.移除不同值重排数组"
question_id: "4065"
question: "移除不同值重排数组"
problem_url: "https://leetcode.cn/problems/rearrange-array-by-removing-distinct-values/"
difficulty: "Easy"
created: "2026-09-30T21:53:27+08:00"
updated: "2026-09-30T21:53:27+08:00"
upvotes: 2
comments: 0
---

# 4065. 移除不同值重排数组

> **[yiduobo的每日leetcode 4065.移除不同值重排数组](https://zhuanlan.zhihu.com/p/2088747088179943260) · 知乎 · 2026-09-30 · 赞同 2**
> 力扣：[4065. 移除不同值重排数组](https://leetcode.cn/problems/rearrange-array-by-removing-distinct-values/) · Easy · 灵茶山艾府：[两种方法：暴力模拟 / 按出现次数分组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4065.移除不同值重排数组

<https://leetcode.cn/problems/rearrange-array-by-removing-distinct-values/>

题目给出一个正整数数组nums，其长度以及其中元素的大小均不超过100。

在一开始，有一个空数组ans，需要重复执行以下操作，直到nums为空：

- 找出当前nums中所有不同的值
- 将这些不同值各移除一个，并按照升序将这些值依次添加到ans中

返回最终的ans。

题目中nums的长度以及其中元素的大小都不大，因此可以使用一个下标数组cnt记录每种元素出现的次数，然后按照题目描述不断执行操作，直到ans的长度等于nums的长度。

每一轮操作中，都从1遍历到100，对于当前遍历到的v，若cnt[v] > 0，那么就将v加入到ans的末尾，并将cnt[v]减去1。

最后附上python代码：

```python
class Solution(object):
    def rearrangeArray(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        
        cnt = [0] * 101
        for v in nums:
            cnt[v] += 1
        
        res = []
        while len(res) < len(nums):
            for v in range(1, 101):
                if cnt[v] > 0:
                    res.append(v)
                    cnt[v] -= 1
        
        return res
```
