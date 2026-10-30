---
title: "1461. 检查一个字符串是否包含所有长度为K的二进制子串"
aliases: ["yiduobo的每日leetcode 1461.检查一个字符串是否包含所有长度为K的二进制子串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/hash-table", "leetcode/enumeration", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/一-定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/412922680"
zhihu_id: "412922680"
zhihu_title: "yiduobo的每日leetcode 1461.检查一个字符串是否包含所有长度为K的二进制子串"
question_id: "1461"
question: "检查一个字符串是否包含所有长度为 K 的二进制子串"
problem_url: "https://leetcode.cn/problems/check-if-a-string-contains-all-binary-codes-of-size-k/"
difficulty: "Medium"
rating: 1504
created: "2021-09-22T23:40:39+08:00"
updated: "2021-09-22T23:40:39+08:00"
upvotes: 0
comments: 0
---

# 1461. 检查一个字符串是否包含所有长度为K的二进制子串

> **[yiduobo的每日leetcode 1461.检查一个字符串是否包含所有长度为K的二进制子串](https://zhuanlan.zhihu.com/p/412922680) · 知乎 · 2021-09-22 · 赞同 0**
> 力扣：[1461. 检查一个字符串是否包含所有长度为 K 的二进制子串](https://leetcode.cn/problems/check-if-a-string-contains-all-binary-codes-of-size-k/) · Medium · 灵茶山艾府：[两种方法：暴力 / 位运算（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1461.检查一个字符串是否包含所有长度为K的二进制子串

[力扣](https://leetcode-cn.com/problems/check-if-a-string-contains-all-binary-codes-of-size-k/)

所有长度为K的二进制串数目一共有2^k个，而一个长度为l的字符串中所包含的长度为k的子串数目则一共是l - k + 1个，那么可以先检测这个总数与目标子串数目的大小，若数目不足，那么答案必然为false。

接下来则可以利用滑动窗口，找出s中所有长度为k的子串，并将这些子串储存在集合中。由于这里的k最多为20，那么最多只有1048576个子串，同时也可以使用二进制编码来表示各个子串。处理完成后，若最终集合的大小恰好为2^k，那么答案就是true，否则答案就是false。

最后附上python代码：

```python
class Solution(object):
    def hasAllCodes(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: bool
        """

        p = 1 << k
        if len(s) - k + 1 < p:
            return False

        num_set = set()
        now = 0
        for char in s[:k]:
            now = now + now + int(char)
        
        num_set.add(now)
        for char in s[k:]:
            now = now + now + int(char)
            if now >= p:
                now -= p
            num_set.add(now)
        
        return len(num_set) == p
```
