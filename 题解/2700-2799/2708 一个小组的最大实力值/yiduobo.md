---
title: "2708. 一个小组的最大实力值"
aliases: ["yiduobo的每日leetcode 2708.一个小组的最大实力值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/六-状态机-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/650975666"
zhihu_id: "650975666"
zhihu_title: "yiduobo的每日leetcode 2708.一个小组的最大实力值"
question_id: "2708"
question: "一个小组的最大实力值"
problem_url: "https://leetcode.cn/problems/maximum-strength-of-a-group/"
difficulty: "Medium"
created: "2023-08-19T01:29:23+08:00"
updated: "2023-08-19T01:29:23+08:00"
upvotes: 0
comments: 0
---

# 2708. 一个小组的最大实力值

> **[yiduobo的每日leetcode 2708.一个小组的最大实力值](https://zhuanlan.zhihu.com/p/650975666) · 知乎 · 2023-08-19 · 赞同 0**
> 力扣：[2708. 一个小组的最大实力值](https://leetcode.cn/problems/maximum-strength-of-a-group/) · Medium · 灵茶山艾府：[O(n) 一次遍历，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2708.一个小组的最大实力值

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximum-strength-of-a-group/)

题目中计算小组实力是通过乘法，那么在这里对于0和负数就需要特别进行处理。

首先，若数组中存在正数，或者存在两个以上的负数，那么就不应该选择0加入，因为一旦有0加入这个小组的实力值就必然为0了。也就是说，只有当数组中不存在正数，且负数的数量不超过一个时，才应该选择0作为答案。

接下来对于负数，若数组中只存在一个数且这个数为负数，那么此时就只能被迫选择这个负数，否则的话负数都应该成对出现，使得二者的乘积变为正数。当数组中存在奇数个负数时，应该将其中绝对值最小的那个排除出去，这样才能使得其他负数的乘积最大。

最后对于正数，自然是全部都要了。

最后附上python代码：

```python
class Solution(object):
    def maxStrength(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = None
        neg = 0
        zero = 0
        max_neg = None
        for v in nums:
            if v == 0:
                zero += 1
            else:
                if res is None:
                    res = v
                else:
                    res *= v
                if v < 0:
                    neg += 1
                    if max_neg is None or max_neg < v:
                        max_neg = v

        if res is None:
            res = 0
        elif res < 0 and len(nums) > 1:
            if neg == 1 and neg + zero == len(nums):
                res = 0
            else:
                res /= max_neg
        
        return res
```
