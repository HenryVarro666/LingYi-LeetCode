---
title: "3681. 子序列最大XOR值"
aliases: ["yiduobo的每日leetcode 3681.子序列最大XOR值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/math", "题单/位运算", "题单/位运算/七-线性基"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1953237183512154362"
zhihu_id: "1953237183512154362"
zhihu_title: "yiduobo的每日leetcode 3681.子序列最大XOR值"
question_id: "3681"
question: "子序列最大 XOR 值"
problem_url: "https://leetcode.cn/problems/maximum-xor-of-subsequences/"
difficulty: "Hard"
created: "2025-09-24T21:50:11+08:00"
updated: "2025-09-24T21:50:13+08:00"
upvotes: 0
comments: 0
---

# 3681. 子序列最大XOR值

> **[yiduobo的每日leetcode 3681.子序列最大XOR值](https://zhuanlan.zhihu.com/p/1953237183512154362) · 知乎 · 2025-09-24 · 赞同 0**
> 力扣：[3681. 子序列最大 XOR 值](https://leetcode.cn/problems/maximum-xor-of-subsequences/) · Hard · 灵茶山艾府：[【模板】线性基（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3681.子序列最大XOR值

<https://leetcode.cn/problems/maximum-xor-of-subsequences/description/>

题目给出一个长度为n的整数数组nums，其中所有元素非负。现在要求从中选出两个子序列nums，这两个子序列可以为空同时允许重叠，分别定义这两个子序列中所有元素的按位异或为x和y，问x与y异或的最大值是多少。

首先可以明确的是，这两个子序列中的元素不应该重叠，因为同一个元素异或两次等于0，也就是说不选取这两个子序列重叠的部分对结果并没有任何影响。既然这两个子序列不重叠，那么本题相当于要求从nums中选出一个子序列，要求这个子序列的异或值最大。

可以发现，这就是子集最大异或问题，直接照搬之前3630中异或线性基的处理方法就行了。

[yiduobo的每日leetcode 3630.划分数组得到最大异或运算和与运算之和](https://zhuanlan.zhihu.com/p/1945950594863980896)

最后附上python代码：

```python
class Solution(object):
    def maxXorSubsequences(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        length = len(bin(max(nums))) - 2
        f = [None] * (length + 1)
        for x in nums:
            for index in range(length, -1, -1):
                if x & (1 << index) == (1 << index):
                    if f[index] is None:
                        f[index] = x
                        break
                    else:
                        x ^= f[index]

        res = 0
        for index in range(length, -1, -1):
            if f[index] and (res & (1 << index) == 0):
                res ^= f[index]
            
        return res
```
