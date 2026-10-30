---
title: "3674. 数组元素相等的最小操作次数"
aliases: ["yiduobo的每日leetcode 3674.数组元素相等的最小操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1952806521269358629"
zhihu_id: "1952806521269358629"
zhihu_title: "yiduobo的每日leetcode 3674.数组元素相等的最小操作次数"
question_id: "3674"
question: "数组元素相等的最小操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-equalize-array/"
difficulty: "Easy"
rating: 1369
created: "2025-09-21T20:13:59+08:00"
updated: "2025-09-21T20:14:01+08:00"
upvotes: 2
comments: 0
---

# 3674. 数组元素相等的最小操作次数

> **[yiduobo的每日leetcode 3674.数组元素相等的最小操作次数](https://zhuanlan.zhihu.com/p/1952806521269358629) · 知乎 · 2025-09-21 · 赞同 2**
> 力扣：[3674. 数组元素相等的最小操作次数](https://leetcode.cn/problems/minimum-operations-to-equalize-array/) · Easy · 灵茶山艾府：[脑筋急转弯（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3674.数组元素相等的最小操作次数

[3674. 数组元素相等的最小操作次数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-equalize-array/description/)

题目给出一个长度为n的整数数组nums，在一次操作中，可以选择任意子数组，并将这个子数组替换为其中所有元素的按位与结果。

问将nums中所有元素都变为相等所需的最小操作次数。

如果nums中所有元素在一开始就相等，那么答案显然为0，反之，则只需选取整个子数组执行按位与操作，最后就只会剩下按位与结果这一个元素，也就是说答案为1。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        for v in nums[1:]:
            if v != nums[0]:
                return 1
        
        return 0
```
