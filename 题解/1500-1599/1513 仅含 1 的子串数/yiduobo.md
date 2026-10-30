---
title: "1513. 仅含1的子串数"
aliases: ["yiduobo的每日leetcode 1513.仅含1的子串数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bian-li", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/420785287"
zhihu_id: "420785287"
zhihu_title: "yiduobo的每日leetcode 1513.仅含1的子串数"
question_id: "1513"
question: "仅含 1 的子串数"
problem_url: "https://leetcode.cn/problems/number-of-substrings-with-only-1s/"
difficulty: "Medium"
rating: 1351
created: "2021-10-12T23:37:35+08:00"
updated: "2021-10-12T23:37:35+08:00"
upvotes: 0
comments: 0
---

# 1513. 仅含1的子串数

> **[yiduobo的每日leetcode 1513.仅含1的子串数](https://zhuanlan.zhihu.com/p/420785287) · 知乎 · 2021-10-12 · 赞同 0**
> 力扣：[1513. 仅含 1 的子串数](https://leetcode.cn/problems/number-of-substrings-with-only-1s/) · Medium · 灵茶山艾府：[枚举子串右端点，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1513.仅含1的子串数

[力扣](https://leetcode-cn.com/problems/number-of-substrings-with-only-1s/)

题目要求出仅含1的子串的数目，也就是说可以先按照0来对字符串进行分割，得到若干个全1的字符串。

对于某个长度为k的全1字符串而言，长度为1的字符共有k个，长度为2的共有k - 1个，依次类推，最终长度为k的只有1个，因此一共有1 + 2 + ... + k \= k \* (k + 1) / 2个合法的子串。

那么只需要对于分割出来的每个全1子串，都分别求出其合法的子串数目，然后累加即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def numSub(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        mod = 10 ** 9 + 7
        res = 0
        l = 0
        for char in s:
            if char == '1':
                l += 1
            else:
                res += l * (l + 1) / 2
                res %= mod
                l = 0
        
        res += l * (l + 1) / 2
        return res % mod
```
