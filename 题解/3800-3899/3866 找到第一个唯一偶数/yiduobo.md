---
title: "3866. 找到第一个唯一偶数"
aliases: ["yiduobo的每日leetcode 3866.找到第一个唯一偶数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2017393195047223933"
zhihu_id: "2017393195047223933"
zhihu_title: "yiduobo的每日leetcode 3866.找到第一个唯一偶数"
question_id: "3866"
question: "找到第一个唯一偶数"
problem_url: "https://leetcode.cn/problems/first-unique-even-element/"
difficulty: "Easy"
created: "2026-03-18T00:15:53+08:00"
updated: "2026-03-18T00:15:53+08:00"
upvotes: 0
comments: 0
---

# 3866. 找到第一个唯一偶数

> **[yiduobo的每日leetcode 3866.找到第一个唯一偶数](https://zhuanlan.zhihu.com/p/2017393195047223933) · 知乎 · 2026-03-18 · 赞同 0**
> 力扣：[3866. 找到第一个唯一偶数](https://leetcode.cn/problems/first-unique-even-element/) · Easy · 灵茶山艾府：[O(n) 做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3866.找到第一个唯一偶数

<https://leetcode.cn/problems/first-unique-even-element/description/>

题目给出一个整数数组nums。

现在要求返回一个整数，表示nums中恰好出现一次的第一个偶数，若不存在，则返回-1。

一趟遍历，使用哈希表统计数组中每种元素出现的次数。然后再一趟遍历，对于当前元素v，若其为偶数，则通过哈希表检测其出现次数是否为恰好一次，若是，那么v就是要找的答案。若遍历完还没找到这样的v，则返回-1。

最后附上python代码：

```python
class Solution(object):
    def firstUniqueEven(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        cnt = {}
        for v in nums:
            cnt[v] = cnt.get(v, 0) + 1
        
        for v in nums:
            if v % 2 == 0 and cnt[v] == 1:
                return v
        return -1
```
