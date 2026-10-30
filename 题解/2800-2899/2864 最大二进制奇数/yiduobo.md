---
title: "2864. 最大二进制奇数"
aliases: ["yiduobo的每日leetcode 2864.最大二进制奇数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/661689060"
zhihu_id: "661689060"
zhihu_title: "yiduobo的每日leetcode 2864.最大二进制奇数"
question_id: "2864"
question: "最大二进制奇数"
problem_url: "https://leetcode.cn/problems/maximum-odd-binary-number/"
difficulty: "Easy"
created: "2023-10-17T00:46:05+08:00"
updated: "2023-10-17T00:46:05+08:00"
upvotes: 0
comments: 0
---

# 2864. 最大二进制奇数

> **[yiduobo的每日leetcode 2864.最大二进制奇数](https://zhuanlan.zhihu.com/p/661689060) · 知乎 · 2023-10-17 · 赞同 0**
> 力扣：[2864. 最大二进制奇数](https://leetcode.cn/problems/maximum-odd-binary-number/) · Easy · 灵茶山艾府：[贪心（每个语言都只需要两行！）Python/Java/C++/Go/JS/Rust](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2864.最大二进制奇数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximum-odd-binary-number/)

为了使得答案为奇数，那么二进制的最低位必须是1，而为了使得答案最大，那么就应该将剩下的1集中在答案的高位，于是只需一趟遍历，统计s中1的个数cnt，那么最终答案就是cnt - 1个1，拼接上所有的0，再拼接上最低位的这个1。

最后附上python代码：

```python
class Solution(object):
    def maximumOddBinaryNumber(self, s):
        """
        :type s: str
        :rtype: str
        """

        one = sum([int(x) for x in s])
        n = len(s)
        
        return '1' * (one - 1) + '0' * (n - one) + '1'
```
