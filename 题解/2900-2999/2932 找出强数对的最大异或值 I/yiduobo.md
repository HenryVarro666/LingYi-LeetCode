---
title: "2932. 找出强数对的最大异或值I"
aliases: ["yiduobo的每日leetcode 2932.找出强数对的最大异或值I"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/trie", "leetcode/hash-table", "leetcode/sliding-window"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/690670843"
zhihu_id: "690670843"
zhihu_title: "yiduobo的每日leetcode 2932.找出强数对的最大异或值I"
question_id: "2932"
question: "找出强数对的最大异或值 I"
problem_url: "https://leetcode.cn/problems/maximum-strong-pair-xor-i/"
difficulty: "Easy"
created: "2024-04-04T02:35:33+08:00"
updated: "2024-04-04T02:35:33+08:00"
upvotes: 1
comments: 0
---

# 2932. 找出强数对的最大异或值I

> **[yiduobo的每日leetcode 2932.找出强数对的最大异或值I](https://zhuanlan.zhihu.com/p/690670843) · 知乎 · 2024-04-04 · 赞同 1**
> 力扣：[2932. 找出强数对的最大异或值 I](https://leetcode.cn/problems/maximum-strong-pair-xor-i/) · Easy · 灵茶山艾府：[两种非暴力做法：0-1 trie+滑窗 / 哈希表（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2932.找出强数对的最大异或值I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-strong-pair-xor-i/)

题目的数据规模非常小，因此可以直接枚举每一组x和y，对于所有符合条件的x和y，计算二者的异或值并更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def maximumStrongPairXor(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0
        for x in nums:
            for y in nums:
                if abs(x - y) <= min(x, y):
                    res = max(res, x ^ y)
        
        return res
```
