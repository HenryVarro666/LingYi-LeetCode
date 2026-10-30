---
title: "3750. 最少反转次数得到翻转二进制字符串"
aliases: ["yiduobo的每日leetcode 3750.最少反转次数得到翻转二进制字符串"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/string", "题单/位运算", "题单/位运算/一-基础题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1976795556207695304"
zhihu_id: "1976795556207695304"
zhihu_title: "yiduobo的每日leetcode 3750.最少反转次数得到翻转二进制字符串"
question_id: "3750"
question: "最少翻转次数得到反转二进制字符串"
problem_url: "https://leetcode.cn/problems/minimum-number-of-flips-to-reverse-binary-string/"
difficulty: "Easy"
rating: 1289
created: "2025-11-27T00:06:24+08:00"
updated: "2025-11-27T00:06:27+08:00"
upvotes: 0
comments: 0
---

# 3750. 最少反转次数得到翻转二进制字符串

> **[yiduobo的每日leetcode 3750.最少反转次数得到翻转二进制字符串](https://zhuanlan.zhihu.com/p/1976795556207695304) · 知乎 · 2025-11-27 · 赞同 0**
> 力扣：[3750. 最少翻转次数得到反转二进制字符串](https://leetcode.cn/problems/minimum-number-of-flips-to-reverse-binary-string/) · Easy · 灵茶山艾府：[两种方法：从 O(log n) 到 O(1)（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3750.最少反转次数得到翻转二进制字符串

[3750. 最少反转次数得到翻转二进制字符串 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-number-of-flips-to-reverse-binary-string/description/)

题目给出一个正整数n，令s为n的二进制表示。二进制字符串s的反转指的是将s中的字符按相反顺序排列得到的字符串。现在可以翻转s中的任意一位若干次，问使得s变为其原始形式的反转所需的最少翻转次数。

先通过模2除以2将n变成s，接下来使用两个指针left和right从s的两端向中间走。

对于当前的left、right，s[left]、s[right]在反转的s中对应的就是s[right]、s[left]。若s[left]与s[right]相同，那么就不需要操作，反之就需要将s[left]以及s[right]都变为对方，需要进行两次翻转操作。无论是否相同，都需要将left和right都向中间移动一步。重复以上过程直到left大于等于right为止。

最后附上python代码：

```python
class Solution(object):
    def minimumFlips(self, n):
        """
        :type n: int
        :rtype: int
        """
        
        digits = []
        while n:
            digits.append(n % 2)
            n //= 2
        
        left, right = 0, len(digits) - 1
        res = 0
        while left < right:
            if digits[left] != digits[right]:
                res += 2
            left += 1
            right -= 1
        
        return res
```
