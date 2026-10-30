---
title: "3723. 数位平方和的最大值"
aliases: ["yiduobo的每日leetcode 3723.数位平方和的最大值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/math", "题单/贪心算法", "题单/贪心算法/三-字符串贪心", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1965844548673570128"
zhihu_id: "1965844548673570128"
zhihu_title: "yiduobo的每日leetcode 3723.数位平方和的最大值"
question_id: "3723"
question: "数位平方和的最大值"
problem_url: "https://leetcode.cn/problems/maximize-sum-of-squares-of-digits/"
difficulty: "Medium"
rating: 1537
created: "2025-10-26T18:28:11+08:00"
updated: "2025-10-26T18:28:15+08:00"
upvotes: 3
comments: 0
---

# 3723. 数位平方和的最大值

> **[yiduobo的每日leetcode 3723.数位平方和的最大值](https://zhuanlan.zhihu.com/p/1965844548673570128) · 知乎 · 2025-10-26 · 赞同 3**
> 力扣：[3723. 数位平方和的最大值](https://leetcode.cn/problems/maximize-sum-of-squares-of-digits/) · Medium · 灵茶山艾府：[贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3723.数位平方和的最大值

<https://leetcode.cn/problems/maximize-sum-of-squares-of-digits/description/>

题目给出两个正整数num和sum，其中nums在1到2 \* 10^5之间，sum在1到2 \* 10^6之间。

若一个正整数n的位数恰好为num，且其各位上数字之和恰好为sum，那么就称其为好整数。

一个好整数的分数定义为其各位数字的平方之和，现在要求找出分数最大的那个好整数n，若有多个可能的整数，则返回最大的那个。若不存在，则返回空字符串。

首先考虑无解的情况。

由于n的数位上可以填充0，因此对于一个num位的整数而言，其最高位上如果填1，其他位上填0，就可以得到sum为1的情况；若其所有位上都填9，则可以得到sum为9 \* num的情况。也就是说，当sum处于1到9 \* num之间时是必然有解的。由于题目保证了sum为正整数，因此只需要考虑sum是否大于9 \* num，若大于，则说明无解，此时直接返回空字符串即可。

接下来处理一般情况。

题目要求找出分数最大的那个n，而对于一组和为s的非负整数a和b，要让a^2 + b^2最大，就应该让a取s，b取0，或者a取0，b取s。对于本题，则应该让值为9的数位尽可能的多。另一方面，对于分数相同的情况需要让n最大，那么就应该让这些9尽量集中在n的头部。

基于以上的结论，就可以先从sum中尽可能分离出9，记nine \= sum // 9，那么n的前nine位就应该都填充9。接下来，若nine就等于num，那么答案就是这nine个9构成的字符串；若nine \< num，那么首先应该将sum中分离掉9之后剩下的数填充到答案的下一位，然后将剩下的num - nine - 1位都填上0即可。

最后附上python代码：

```python
class Solution(object):
    def maxSumOfSquares(self, num, sum):
        """
        :type num: int
        :type sum: int
        :rtype: str
        """
        
        if num * 9 < sum:
            return ""
        
        nine = sum // 9
        
        if nine == num:
            return '9' * num
        else:
            return '9' * nine + str(sum - 9 * nine) + '0' * (num - nine - 1)
```
