---
title: "2207. 字符串中最多数目的子字符串"
aliases: ["yiduobo的每日leetcode 2207.字符串中最多数目的子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/539718244"
zhihu_id: "539718244"
zhihu_title: "yiduobo的每日leetcode 2207.字符串中最多数目的子字符串"
question_id: "2207"
question: "字符串中最多数目的子序列"
problem_url: "https://leetcode.cn/problems/maximize-number-of-subsequences-in-a-string/"
difficulty: "Medium"
created: "2022-07-09T23:32:55+08:00"
updated: "2022-07-09T23:32:55+08:00"
upvotes: 0
comments: 0
---

# 2207. 字符串中最多数目的子字符串

> **[yiduobo的每日leetcode 2207.字符串中最多数目的子字符串](https://zhuanlan.zhihu.com/p/539718244) · 知乎 · 2022-07-09 · 赞同 0**
> 力扣：[2207. 字符串中最多数目的子序列](https://leetcode.cn/problems/maximize-number-of-subsequences-in-a-string/) · Medium · 灵茶山艾府：[贪心 + 一次遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2207.字符串中最多数目的子字符串

[力扣](https://leetcode.cn/problems/maximize-number-of-subsequences-in-a-string/)

由于有一次插入字符的机会，那么最终答案可以分为两个部分，分别是由插入字符带来的等于pattern的子序列数目，再加上原始字符串text中等于pattern的子序列数目。对这两部分分别进行讨论：

1、插入pattern[0]或者pattern[1]带来的子序列。

当插入的字符为pattern[0]时，由插入的字符带来的等于pattern的子序列数目就取决于在插入位置的右侧有多少个字符等于pattern[1]，那么显然应该将pattern[0]插入到text的头部，这样一来其右侧等于pattern[1]的字符必然是最多的。

类似的，当插入的字符为pattern[1]时，则应该将其插入到text的末尾。

不妨设text中等于pattern[0]的字符有cnt1个，等于pattern[1]的字符有cnt2个，那么由插入字符带来的合法子序列数目就是max(cnt1, cnt2)

2、原始字符串text中等于pattern的子序列。

对于text中的某个字符text[index]，若其恰好等于pattern[1]，那么以该字符为结尾，且恰好等于pattern的子序列数目就是text[0]到text[index - 1]之间等于pattern[0]的字符的数目。

那么就可以从左向右一趟遍历，在过程中统计当前的前缀中有多少个字符等于pattern[0]，并在当前字符等于pattern[1]时使用这个统计值更新答案。

情况1恰好需要统计pattern[0]和pattern[1]出现的次数，现在已经统计了pattern[0]的数目，只需顺便也把pattern[1]的数目统计出来就好了。

最后附上python代码：

```python
class Solution(object):
    def maximumSubsequenceCount(self, text, pattern):
        """
        :type text: str
        :type pattern: str
        :rtype: int
        """

        cnt1 = cnt2 = 0
        res = 0
        for char in text:
            if char == pattern[1]:
                res += cnt1
                cnt2 += 1
            if char == pattern[0]:
                cnt1 += 1
        
        return res + max(cnt1, cnt2)
```
