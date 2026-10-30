---
title: "2935. 找出强数对的最大异或值II"
aliases: ["yiduobo的每日leetcode 2935.找出强数对的最大异或值II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/trie", "leetcode/hash-table", "leetcode/sliding-window", "题单/常用数据结构", "题单/位运算", "题单/常用数据结构/六-字典树-trie", "题单/位运算/五-试填法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/690781916"
zhihu_id: "690781916"
zhihu_title: "yiduobo的每日leetcode 2935.找出强数对的最大异或值II"
question_id: "2935"
question: "找出强数对的最大异或值 II"
problem_url: "https://leetcode.cn/problems/maximum-strong-pair-xor-ii/"
difficulty: "Hard"
rating: 2349
created: "2024-04-05T05:46:00+08:00"
updated: "2024-04-05T05:46:00+08:00"
upvotes: 1
comments: 0
---

# 2935. 找出强数对的最大异或值II

> **[yiduobo的每日leetcode 2935.找出强数对的最大异或值II](https://zhuanlan.zhihu.com/p/690781916) · 知乎 · 2024-04-05 · 赞同 1**
> 力扣：[2935. 找出强数对的最大异或值 II](https://leetcode.cn/problems/maximum-strong-pair-xor-ii/) · Hard · 灵茶山艾府：[两种方法：0-1 trie+滑窗 / 哈希表（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2935.找出强数对的最大异或值II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-strong-pair-xor-ii/description/)

之前2932题的强化版，本题的数据规模到了10^5，因此O(n^2)的暴力算法肯定不行了，必须想办法进行优化。

首先观察题目中关于强数对的定义abs(x - y) \<\= min(x, y)，不妨设x \<\= y，这里的绝对值拆开得到的是y - x \<\= x，那么强数对就是所有满足y \<\= x \* 2的数对。有了这一点，就可以先将数组排序，然后枚举y，接下来就可以利用单调性找出可以与y形成强数对的最大的x，问题就变成了给出一个变长的滑动窗口在数组中从左向右滑动，问当前窗口内的数与窗口右边界的数异或值的最大值。

对于这个问题，则可以利用之前1707题中类似的做法，利用trie树储存区间内的数，然后在trie树中尽量反向查找窗口右边界这个数，这样的话可以让异或结果从高位到低位尽可能出现1从而使得异或结果最大。

[yiduobo：yiduobo的每日leetcode 1707.与数组中元素的最大异或值](https://zhuanlan.zhihu.com/p/449610412)

最后附上python代码：

```python
class Solution(object):
    def maximumStrongPairXor(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        root = [[None, None], [0, 0]]

        def add(v, delta):
            now = root
            for i in range(19, -1, -1):
                if v & (1 << i) == (1 << i):
                    t = 1
                else:
                    t = 0
                
                if now[0][t] is None:
                    now[0][t] = [[None, None], [0, 0]]
                now[1][t] += delta
                now = now[0][t]

        def get(v):
            ma = 0
            now = root
            for i in range(19, -1, -1):
                if v & (1 << i) == (1 << i):
                    t = 0
                else:
                    t = 1
                
                if now[1][t] > 0:
                    now = now[0][t]
                    ma |= (1 << i)
                else:
                    now = now[0][1 - t]
                    
            return ma

        nums.sort()
        p = 0
        res = 0
        for v in nums:
            while p < len(nums) and nums[p] + nums[p] < v:
                add(nums[p], -1)
                p += 1
            add(v, 1)
            res = max(res, get(v))
        
        return res
```
