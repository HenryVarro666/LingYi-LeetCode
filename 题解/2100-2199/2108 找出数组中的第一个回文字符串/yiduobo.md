---
title: "2108. 找出数组中的第一个回文字符串"
aliases: ["yiduobo的每日leetcode 2108.找出数组中的第一个回文字符串"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/523287015"
zhihu_id: "523287015"
zhihu_title: "yiduobo的每日leetcode 2108.找出数组中的第一个回文字符串"
question_id: "2108"
question: "找出数组中的第一个回文字符串"
problem_url: "https://leetcode.cn/problems/find-first-palindromic-string-in-the-array/"
difficulty: "Easy"
created: "2022-06-02T00:13:05+08:00"
updated: "2022-06-02T00:13:05+08:00"
upvotes: 0
comments: 0
---

# 2108. 找出数组中的第一个回文字符串

> **[yiduobo的每日leetcode 2108.找出数组中的第一个回文字符串](https://zhuanlan.zhihu.com/p/523287015) · 知乎 · 2022-06-02 · 赞同 0**
> 力扣：[2108. 找出数组中的第一个回文字符串](https://leetcode.cn/problems/find-first-palindromic-string-in-the-array/) · Easy · 灵茶山艾府：[遍历，找第一个回文串](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2108.找出数组中的第一个回文字符串

[力扣](https://leetcode.cn/problems/find-first-palindromic-string-in-the-array/)

比较基础的题目。从左往右遍历数组中的每个字符串，然后判断其是否为回文字符串即可。具体的判断方法可以使用两个指针从两侧往中间同步扫，若某一时刻指向的字符不同，说明该字符串不是回文串。若直到两个指针相遇都没有出现字符不同的情况，则说明这个字符串是回文字符串。

最后附上python：

```python
class Solution(object):
    def firstPalindrome(self, words):
        """
        :type words: List[str]
        :rtype: str
        """

        for word in words:
            flag = True
            l = 0
            r = len(word) - 1
            while l < r:
                if word[l] != word[r]:
                    flag = False
                    break
                l += 1
                r -= 1
            
            if flag:
                return word
        
        return ""
```
