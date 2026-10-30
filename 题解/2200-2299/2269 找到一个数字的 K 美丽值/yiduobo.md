---
title: "2269. 找到一个数字的K美丽值"
aliases: ["yiduobo的每日leetcode 2269.找到一个数字的K美丽值"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/549610915"
zhihu_id: "549610915"
zhihu_title: "yiduobo的每日leetcode 2269.找到一个数字的K美丽值"
question_id: "2269"
question: "找到一个数字的 K 美丽值"
problem_url: "https://leetcode.cn/problems/find-the-k-beauty-of-a-number/"
difficulty: "Easy"
created: "2022-08-04T01:02:56+08:00"
updated: "2022-08-04T01:02:56+08:00"
upvotes: 0
comments: 0
---

# 2269. 找到一个数字的K美丽值

> **[yiduobo的每日leetcode 2269.找到一个数字的K美丽值](https://zhuanlan.zhihu.com/p/549610915) · 知乎 · 2022-08-04 · 赞同 0**
> 力扣：[2269. 找到一个数字的 K 美丽值](https://leetcode.cn/problems/find-the-k-beauty-of-a-number/) · Easy · 灵茶山艾府：[两种方法：字符串 / 数学（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2269.找到一个数字的K美丽值

[力扣](https://leetcode.cn/problems/find-the-k-beauty-of-a-number/)

由于num的长度有限，那么完全可以从左向右一趟遍历，枚举num所有长为k的子串，然后判断num是否为这个子串的倍数并更新答案。

最后附上python代码：

```python
class Solution(object):
    def divisorSubstrings(self, num, k):
        """
        :type num: int
        :type k: int
        :rtype: int
        """

        digits = list(str(num))
        res = 0

        now = 0
        for digit in digits[:k]:
            now = now * 10 + int(digit)

        if now > 0 and num % now == 0:
            res += 1
        
        mod = 10 ** k
        for digit in digits[k:]:
            now = (now * 10 + int(digit)) % mod
            if now > 0 and num % now == 0:
                res += 1

        return res
```
