---
title: "3722. 反转后字典序最小的字符串"
aliases: ["yiduobo的每日leetcode 3722.反转后字典序最小的字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration", "leetcode/suffix-array", "题单/字符串", "题单/字符串/四-字符串哈希", "题单/字符串/八-后缀数组/后缀自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1966969336452346426"
zhihu_id: "1966969336452346426"
zhihu_title: "yiduobo的每日leetcode 3722.反转后字典序最小的字符串"
question_id: "3722"
question: "反转后字典序最小的字符串"
problem_url: "https://leetcode.cn/problems/lexicographically-smallest-string-after-reverse/"
difficulty: "Medium"
created: "2025-10-29T21:01:21+08:00"
updated: "2025-10-29T21:01:21+08:00"
upvotes: 3
comments: 0
---

# 3722. 反转后字典序最小的字符串

> **[yiduobo的每日leetcode 3722.反转后字典序最小的字符串](https://zhuanlan.zhihu.com/p/1966969336452346426) · 知乎 · 2025-10-29 · 赞同 3**
> 力扣：[3722. 反转后字典序最小的字符串](https://leetcode.cn/problems/lexicographically-smallest-string-after-reverse/) · Medium · 灵茶山艾府：[枚举 k，附 O(nlogn) 后缀数组做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3722.反转后字典序最小的字符串

[3722. 反转后字典序最小的字符串 - 力扣（LeetCode）](https://leetcode.cn/problems/lexicographically-smallest-string-after-reverse/description/)

题目给出一个由小写字母组成的，长度为n的字符串s，n的大小在1到1000之间。

现在要求找出一个1到n之间的整数k，然后翻转s的前k个字符，或者翻转s的后k个字符。

问执行操作后可以得到的字典序最小的字符串是什么。

由于n的规模不大，因此可以直接暴力枚举这个k，然后按照题目要求，分别计算两种情况构成的字符串，取其中的最小值即可。

在具体实现上，可以从1到n枚举这个k，让前k个字符与后n - k个字符这两种情况一同计算，即s[:k]与s[k:]一同计算。

最后附上python代码：

```python
class Solution(object):
    def lexSmallest(self, s):
        """
        :type s: str
        :rtype: str
        """
        
        res = s
        for k in range(1, len(s) + 1):
            rl = s[:k][::-1]
            res = min(res, rl + s[k:])
            rr = s[k:][::-1]
            res = min(res, s[:k] + rr)
        
        return res
```
