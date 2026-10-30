---
title: "2657. 找到两个数组的前缀公共数组"
aliases: ["yiduobo的每日leetcode 2657.找到两个数组的前缀公共数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "题单/位运算", "题单/位运算/一-基础题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/648095037"
zhihu_id: "648095037"
zhihu_title: "yiduobo的每日leetcode 2657.找到两个数组的前缀公共数组"
question_id: "2657"
question: "找到两个数组的前缀公共数组"
problem_url: "https://leetcode.cn/problems/find-the-prefix-common-array-of-two-arrays/"
difficulty: "Medium"
created: "2023-08-04T23:48:37+08:00"
updated: "2023-08-04T23:48:37+08:00"
upvotes: 0
comments: 0
---

# 2657. 找到两个数组的前缀公共数组

> **[yiduobo的每日leetcode 2657.找到两个数组的前缀公共数组](https://zhuanlan.zhihu.com/p/648095037) · 知乎 · 2023-08-04 · 赞同 0**
> 力扣：[2657. 找到两个数组的前缀公共数组](https://leetcode.cn/problems/find-the-prefix-common-array-of-two-arrays/) · Medium · 灵茶山艾府：[利用位运算加速（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2657.找到两个数组的前缀公共数组

[力扣](https://leetcode.cn/problems/find-the-prefix-common-array-of-two-arrays/)

题目的数据规模很小，只需遍历两个数组所有长度相同的前缀，然后检测前缀中同时出现的数字个数即可。

在具体实现上，由于数组中的数都不超过50，因此可以分别使用两个50位的二进制数来表示A和B的当前前缀中是否包含某个数，那么同时出现的数字个数就是这两个二进制数按位与的结果中1的个数。

最后附上python代码：

```python
class Solution(object):
    def findThePrefixCommonArray(self, A, B):
        """
        :type A: List[int]
        :type B: List[int]
        :rtype: List[int]
        """

        x = y = 0
        res = []
        for a, b in zip(A, B):
            x |= (1 << a)
            y |= (1 << b)
            
            t = x & y
            cnt = 0
            while t:
                t -= t & -t
                cnt += 1
            
            res.append(cnt)
        
        return res
```
