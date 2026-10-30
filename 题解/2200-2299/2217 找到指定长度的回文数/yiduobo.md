---
title: "2217. 找到指定长度的回文数"
aliases: ["yiduobo的每日leetcode 2217.找到指定长度的回文数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/541671379"
zhihu_id: "541671379"
zhihu_title: "yiduobo的每日leetcode 2217.找到指定长度的回文数"
question_id: "2217"
question: "找到指定长度的回文数"
problem_url: "https://leetcode.cn/problems/find-palindrome-with-fixed-length/"
difficulty: "Medium"
rating: 1822
created: "2022-07-14T18:57:28+08:00"
updated: "2022-07-14T18:57:28+08:00"
upvotes: 0
comments: 0
---

# 2217. 找到指定长度的回文数

> **[yiduobo的每日leetcode 2217.找到指定长度的回文数](https://zhuanlan.zhihu.com/p/541671379) · 知乎 · 2022-07-14 · 赞同 0**
> 力扣：[2217. 找到指定长度的回文数](https://leetcode.cn/problems/find-palindrome-with-fixed-length/) · Medium · 灵茶山艾府：[反转回文数左半部分](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2217.找到指定长度的回文数

[力扣](https://leetcode.cn/problems/find-palindrome-with-fixed-length/)

题目要求找出长度为n的第k小的回文数，由于回文数的左右两个半边是对称的，那么高位越小，也就是左半边越小，整个回文数就越小。对于长度为n的回文数，最小的左半边是100...0，记为base。base里有(n - 1)/2个0。接下来则是100...001、100...002这样类推，那么第k小的就是100...000 + k - 1，记这个值为left。

得到left后，首先需要判断left是不是越界了，也就是当left >\= base \* 10。若越界，则直接返回-1。若没有越界，那么就可以利用left来构造出整个回文数，具体构造方法就是将left复制一份再反过来拼在left后面。在这里需要注意n的奇偶性问题，当n为奇数时，left的最后一位，也就是整个回文数正中间那一位是不需要复制的。

最后附上python代码：

```python
class Solution(object):
    def kthPalindrome(self, queries, intLength):
        """
        :type queries: List[int]
        :type intLength: int
        :rtype: List[int]
        """

        base = 10 ** ((intLength - 1) / 2)
        res = []
        for q in queries:
            left = base + q - 1
            if left >= base * 10:
                res.append(-1)
                continue
            left_list = list(str(left))
            if intLength % 2 == 0:
                start_pos = len(left_list) - 1
            else:
                start_pos = len(left_list) - 2
            
            for index in range(start_pos, -1, -1):
                left = left * 10 + int(left_list[index])
            res.append(left)
        
        return res
```
