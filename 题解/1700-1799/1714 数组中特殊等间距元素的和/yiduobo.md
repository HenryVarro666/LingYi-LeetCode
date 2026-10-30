---
title: "1714. 数组中特殊等间距元素的和"
aliases: ["yiduobo的每日leetcode 1714.数组中特殊等间距元素的和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/620277426"
zhihu_id: "620277426"
zhihu_title: "yiduobo的每日leetcode 1714.数组中特殊等间距元素的和"
question_id: "1714"
question: "数组中特殊等间距元素的和"
problem_url: "https://leetcode.cn/problems/sum-of-special-evenly-spaced-elements-in-array/"
created: "2023-04-08T01:48:48+08:00"
updated: "2023-04-08T01:48:48+08:00"
upvotes: 0
comments: 0
---

# 1714. 数组中特殊等间距元素的和

> **[yiduobo的每日leetcode 1714.数组中特殊等间距元素的和](https://zhuanlan.zhihu.com/p/620277426) · 知乎 · 2023-04-08 · 赞同 0**
> 力扣：[1714. 数组中特殊等间距元素的和](https://leetcode.cn/problems/sum-of-special-evenly-spaced-elements-in-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1714.数组中特殊等间距元素的和

[力扣](https://leetcode.cn/problems/sum-of-special-evenly-spaced-elements-in-array/)

对于一个给定的y而言，按照对y的余数一共可以分成y条序列，而每一组询问(x, y)就是询问所有对y取余的值为x % y的数的某个后缀和。对于这个问题，可以直接计算后缀和，也可以计算前缀和然后通过前缀和之差得到。

如果直接计算每个(x, y)对应剩余系下的前缀和，然后利用哈希表应付重复的情况，那么最坏复杂度是O(n \* sqrt(n))。这里的复杂度并不是O(n^2)，因为对于越大的y，每个剩余系需要遍历的数的个数仅有n / y个，因此y越小计算的次数越多，在最坏情况下就是计算一次y \= 1，两次y \= 2，三次y \= 3，依次类推。而对于y相同的情况，加起来刚好是一次遍历，因此最坏的时间复杂度为O(n \* sqrt(n))。

最后还有一个问题就是在对应剩余系的前缀和中，如何确定询问对应的区间起点。这个问题也很简单，就是序列中的第x / y项。

最后附上python代码：

```python
class Solution(object):
    def solve(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        s_dict = {}
        res = []
        mod = 10 ** 9 + 7
        for x, y in queries:
            seq_begin = x % y
            key = (y, seq_begin)
            if key not in s_dict:
                s_dict[key] = []
                now = 0
                for index in range(seq_begin, len(nums), y):
                    now += nums[index]
                    if now >= mod:
                        now -= mod
                    s_dict[key].append(now)
            
            res.append(s_dict[key][-1])
            query_begin = x / y
            if query_begin > 0:
                res[-1] -= s_dict[key][query_begin - 1]
                if res[-1] < 0:
                    res[-1] += mod

        return res
```
