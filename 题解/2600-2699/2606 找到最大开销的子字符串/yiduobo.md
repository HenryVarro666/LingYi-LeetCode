---
title: "2606. 找到最大开销的子字符串"
aliases: ["yiduobo的每日leetcode 2606.找到最大开销的子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/dp", "leetcode/di-tui", "leetcode/dp-2", "题单/动态规划", "题单/动态规划/一-入门-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/645157206"
zhihu_id: "645157206"
zhihu_title: "yiduobo的每日leetcode 2606.找到最大开销的子字符串"
question_id: "2606"
question: "找到最大开销的子字符串"
problem_url: "https://leetcode.cn/problems/find-the-substring-with-maximum-cost/"
difficulty: "Medium"
rating: 1422
created: "2023-07-22T04:25:24+08:00"
updated: "2023-07-22T04:25:24+08:00"
upvotes: 0
comments: 0
---

# 2606. 找到最大开销的子字符串

> **[yiduobo的每日leetcode 2606.找到最大开销的子字符串](https://zhuanlan.zhihu.com/p/645157206) · 知乎 · 2023-07-22 · 赞同 0**
> 力扣：[2606. 找到最大开销的子字符串](https://leetcode.cn/problems/find-the-substring-with-maximum-cost/) · Medium · 灵茶山艾府：[【转换】最大子数组和（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2606.找到最大开销的子字符串

[力扣](https://leetcode.cn/problems/find-the-substring-with-maximum-cost/)

将字符转化为其对应的价值后，问题就变成了经典的最大子段和问题。对于这个问题，只需一趟遍历，使用贪心法进行求解就行了。

最后附上python代码：

```python
class Solution(object):
    def maximumCostSubstring(self, s, chars, vals):
        """
        :type s: str
        :type chars: str
        :type vals: List[int]
        :rtype: int
        """

        val_dict = {}
        for ch, v in zip(chars, vals):
            val_dict[ch] = v

        res = 0
        now = 0
        for ch in s:
            v = val_dict.get(ch, ord(ch) - 96)
            now += v
            if now < 0:
                now = 0
            res = max(res, now)
        
        return res
```
