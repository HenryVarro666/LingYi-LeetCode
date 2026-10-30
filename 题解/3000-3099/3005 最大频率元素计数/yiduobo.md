---
title: "3005. 最大频率元素计数"
aliases: ["yiduobo的每日leetcode 3005.最大频率元素计数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/693509685"
zhihu_id: "693509685"
zhihu_title: "yiduobo的每日leetcode 3005.最大频率元素计数"
question_id: "3005"
question: "最大频率元素计数"
problem_url: "https://leetcode.cn/problems/count-elements-with-maximum-frequency/"
difficulty: "Easy"
created: "2024-04-20T01:36:11+08:00"
updated: "2024-04-20T19:34:01+08:00"
upvotes: 0
comments: 0
---

# 3005. 最大频率元素计数

> **[yiduobo的每日leetcode 3005.最大频率元素计数](https://zhuanlan.zhihu.com/p/693509685) · 知乎 · 2024-04-20 · 赞同 0**
> 力扣：[3005. 最大频率元素计数](https://leetcode.cn/problems/count-elements-with-maximum-frequency/) · Easy · 灵茶山艾府：[一次遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3005.最大频率元素计数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-elements-with-maximum-frequency/description/)

一样遍历，使用哈希表统计每个数出现的频率，然后再遍历这些频率，找出其中的最大值，并将所有的最大值累加即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxFrequencyElements(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        freq = Counter(nums)
        res = 0
        max_f = 0
        for v, f in freq.items():
            if f > max_f:
                res = f
                max_f = f
            elif f == max_f:
                res += f
        
        return res
```
