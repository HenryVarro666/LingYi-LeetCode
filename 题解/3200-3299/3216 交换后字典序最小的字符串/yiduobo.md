---
title: "3215. 用偶数异或设置位计数三元组II & 3216. 交换后字典序最小的字符串"
aliases: ["yiduobo的每日leetcode 3215.用偶数异或设置位计数三元组II && 3216.交换后字典序最小的字符串", "3215. 用偶数异或设置位计数三元组II", "3216. 交换后字典序最小的字符串"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/719088507"
zhihu_id: "719088507"
zhihu_title: "yiduobo的每日leetcode 3215.用偶数异或设置位计数三元组II && 3216.交换后字典序最小的字符串"
question_id: ["3215", "3216"]
question: ["用偶数异或设置位计数三元组II", "交换后字典序最小的字符串"]
problem_url: ["https://leetcode.cn/problems/count-triplets-with-even-xor-set-bits-ii/", "https://leetcode.cn/problems/lexicographically-smallest-string-after-a-swap/"]
difficulty: "Easy"
rating: 1243
created: "2024-09-09T22:48:16+08:00"
updated: "2024-09-09T22:48:16+08:00"
upvotes: 0
comments: 0
---

# 3215. 用偶数异或设置位计数三元组II & 3216. 交换后字典序最小的字符串

> **[yiduobo的每日leetcode 3215.用偶数异或设置位计数三元组II && 3216.交换后字典序最小的字符串](https://zhuanlan.zhihu.com/p/719088507) · 知乎 · 2024-09-09 · 赞同 0**
> 力扣：[3215. 用偶数异或设置位计数三元组II](https://leetcode.cn/problems/count-triplets-with-even-xor-set-bits-ii/)
> 力扣：[3216. 交换后字典序最小的字符串](https://leetcode.cn/problems/lexicographically-smallest-string-after-a-swap/) · Easy · 灵茶山艾府：[贪心，附思考题（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3215.用偶数异或设置位计数三元组II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-triplets-with-even-xor-set-bits-ii/description/)

本题与之前的3199题题设相同，数据规模更大。之前的处理方法是很优的，可以直接套用。

[yiduobo：yiduobo的每日leetcode 3199.用偶数异或设置位计数三元组I](https://zhuanlan.zhihu.com/p/707323153)

3216.交换后字典序最小的字符串

[. - 力扣（LeetCode）](https://leetcode.cn/problems/lexicographically-smallest-string-after-a-swap/description/)

题目给出一个数字字符串，可以交换其中一组相邻且奇偶性相同的字符，问最终可以得到的最大数字是什么。

为了使得最终答案最大，又只能交换一次，那么就应该尽量在高位上进行交换。于是只需从头开始向后一趟遍历，若当前数字与下一位数字奇偶性相同，且当前数字更小，那么就进行交换并返回答案。

最后附上python代码：

```python
class Solution(object):
    def getSmallestString(self, s):
        """
        :type s: str
        :rtype: str
        """

        for i in range(1, len(s)):
            if (int(s[i]) + int(s[i - 1])) % 2 == 0 and s[i] < s[i - 1]:
                return s[:i - 1] + s[i] + s[i - 1] + s[i + 1:]
        
        return s
```
