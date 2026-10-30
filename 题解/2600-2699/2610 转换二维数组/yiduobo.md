---
title: "2610. 转换二维数组"
aliases: ["yiduobo的每日leetcode 2610.转换二维数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/645434849"
zhihu_id: "645434849"
zhihu_title: "yiduobo的每日leetcode 2610.转换二维数组"
question_id: "2610"
question: "转换二维数组"
problem_url: "https://leetcode.cn/problems/convert-an-array-into-a-2d-array-with-conditions/"
difficulty: "Medium"
created: "2023-07-24T02:16:42+08:00"
updated: "2023-07-24T02:16:42+08:00"
upvotes: 0
comments: 0
---

# 2610. 转换二维数组

> **[yiduobo的每日leetcode 2610.转换二维数组](https://zhuanlan.zhihu.com/p/645434849) · 知乎 · 2023-07-24 · 赞同 0**
> 力扣：[2610. 转换二维数组](https://leetcode.cn/problems/convert-an-array-into-a-2d-array-with-conditions/) · Medium · 灵茶山艾府：[一图秒懂（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2610.转换二维数组

[力扣](https://leetcode.cn/problems/convert-an-array-into-a-2d-array-with-conditions/)

对于nums中的数，若某个数出现了k次，那么二维数组中至少需要有k行，才能保证这个数不会在同一个行中出现两次。更进一步的，设这些数出现次数的最大值为max_freq，那么最终的二维数组就至少需要max_freq行。构造出一个拥有max_freq行的二维数组后，对于nums中的数v，若其出现的次数为k，只需在二维数组的0到k - 1行分别加入一个v就行了。

最后附上python代码：

```python
class Solution(object):
    def findMatrix(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """

        num_dict = {}
        max_freq = 0
        for v in nums:
            num_dict[v] = num_dict.get(v, 0) + 1
            max_freq = max(max_freq, num_dict[v])
        
        res = [[] for _ in range(max_freq)]
        for v in num_dict:
            for index in range(num_dict[v]):
                res[index].append(v)
        
        return res
```
