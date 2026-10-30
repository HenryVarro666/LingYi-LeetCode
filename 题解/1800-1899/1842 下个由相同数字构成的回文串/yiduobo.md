---
title: "1842. 下个由相同数字构成的回文串"
aliases: ["yiduobo的每日leetcode 1842.下个由相同数字构成的回文串"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/string", "leetcode/pai-lie", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/622264514"
zhihu_id: "622264514"
zhihu_title: "yiduobo的每日leetcode 1842.下个由相同数字构成的回文串"
question_id: "1842"
question: "下个由相同数字构成的回文串"
problem_url: "https://leetcode.cn/problems/next-palindrome-using-same-digits/"
difficulty: "Hard"
created: "2023-04-16T04:07:50+08:00"
updated: "2023-04-16T04:07:50+08:00"
upvotes: 0
comments: 0
---

# 1842. 下个由相同数字构成的回文串

> **[yiduobo的每日leetcode 1842.下个由相同数字构成的回文串](https://zhuanlan.zhihu.com/p/622264514) · 知乎 · 2023-04-16 · 赞同 0**
> 力扣：[1842. 下个由相同数字构成的回文串](https://leetcode.cn/problems/next-palindrome-using-same-digits/) · Hard · 灵茶山艾府：[Go nextPermutation](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1842.下个由相同数字构成的回文串

[力扣](https://leetcode.cn/problems/next-palindrome-using-same-digits/)

由于字符串中每种字符的数量都是固定的，那么回文串的前半部分和后半部分都将分走每种字符的一半。换言之，无论怎么调整顺序，只要最后依然是回文串，那么前半部分和后半部分的字符组成都不会产生变化。

题目要求找出下一个回文串，由于半区的数字不会产生变化，那么实际上就是要求找出前半部分的下一个排列。对于这个问题，直接照搬之前31题的算法就行了。

[yiduobo：yiduobo的每日leetcode 31.下一个排列](https://zhuanlan.zhihu.com/p/119442273)

得到新的前半部分后，倒转这个前半部分就得到了后半部分。在这里需要特别注意长度为奇数时需要记录正中间的字符。

最后附上python代码：

```python
class Solution(object):
    def nextPalindrome(self, num):
        """
        :type num: str
        :rtype: str
        """

        n = len(num) / 2

        if len(num) % 2 == 1:
            mid = num[n]
        else:
            mid = ''
        
        num_list = list(num[:n])
        p = n - 1
        while p > 0 and num_list[p] <= num_list[p - 1]:
            p -= 1
        
        if p <= 0:
            return ""
        
        p -= 1
        q = n - 1
        while num_list[q] <= num_list[p]:
            q -= 1

        num_list[p], num_list[q] = num_list[q], num_list[p]
        left = p + 1
        right = n - 1
        while left < right:
            num_list[left], num_list[right] = num_list[right], num_list[left]
            left += 1
            right -= 1
        
        res = ''.join(num_list) + mid
        num_list.reverse()
        return res + ''.join(num_list)
```
