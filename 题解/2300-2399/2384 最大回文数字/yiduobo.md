---
title: "2384. 最大回文数字"
aliases: ["yiduobo的每日leetcode 2384.最大回文数字"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/hash-table", "leetcode/string", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/565257896"
zhihu_id: "565257896"
zhihu_title: "yiduobo的每日leetcode 2384.最大回文数字"
question_id: "2384"
question: "最大回文数字"
problem_url: "https://leetcode.cn/problems/largest-palindromic-number/"
difficulty: "Medium"
rating: 1636
created: "2022-09-17T01:49:32+08:00"
updated: "2022-09-17T01:49:32+08:00"
upvotes: 0
comments: 0
---

# 2384. 最大回文数字

> **[yiduobo的每日leetcode 2384.最大回文数字](https://zhuanlan.zhihu.com/p/565257896) · 知乎 · 2022-09-17 · 赞同 0**
> 力扣：[2384. 最大回文数字](https://leetcode.cn/problems/largest-palindromic-number/) · Medium · 灵茶山艾府：[统计 + 贪心](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2384.最大回文数字

[力扣](https://leetcode.cn/problems/largest-palindromic-number/)

题目需要构造回文数字，且要求尽可能大。对于回文数的构造，可以先使用哈希表统计每种数字出现的次数，然后按两个相同的数字一组放在对称的位置上。为了使得结果尽可能大，那么就应该将较大的数字安排在高位上，也就是说应该按从大到小的顺序，从外向内一组一组地安排数字。除此之外，如果还有落单的数字，那么可以选择其中最大的那个放在中间。

需要特别注意的是，题目不允许出现前导0。一旦构造的结果有前导0，由于是从大到小安排的数字，那么说明成对出现的数字只有0，那么此时如果有落单的数字，答案就是其中的最大值，否则答案就是0。

最后附上python代码：

```python
class Solution(object):
    def largestPalindromic(self, num):
        """
        :type num: str
        :rtype: str
        """

        cnt_list = [0] * 10
        for digit in num:
            cnt_list[int(digit)] += 1
        
        mid = None
        res = []
        for digit in range(9, -1, -1):
            res.extend([digit] * (cnt_list[digit] / 2))
            if cnt_list[digit] % 2 == 1 and mid is None:
                mid = digit
        
        if not res:
            return str(mid)
        elif res[0] == 0:
            if mid is None:
                return '0'
            else:
                return str(mid)
        else:
            if mid is None:
                res = res + res[::-1]
            else:
                res = res + [mid] + res[::-1]
            
            return ''.join([str(x) for x in res])
```
