---
title: "680. 验证回文字符串II"
aliases: ["yiduobo的每日leetcode 680.验证回文字符串II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/two-pointers", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/301769466"
zhihu_id: "301769466"
zhihu_title: "yiduobo的每日leetcode 680.验证回文字符串II"
question_id: "680"
question: "验证回文串 II"
problem_url: "https://leetcode.cn/problems/valid-palindrome-ii/"
difficulty: "Easy"
rating: 1400
created: "2020-11-20T00:02:15+08:00"
updated: "2020-11-20T00:02:15+08:00"
upvotes: 0
comments: 0
---

# 680. 验证回文字符串II

> **[yiduobo的每日leetcode 680.验证回文字符串II](https://zhuanlan.zhihu.com/p/301769466) · 知乎 · 2020-11-20 · 赞同 0**
> 力扣：[680. 验证回文串 II](https://leetcode.cn/problems/valid-palindrome-ii/) · Easy · 灵茶山艾府：[贪心：为什么相等的时候不需要删（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

680.验证回文字符串II

[力扣](https://leetcode-cn.com/problems/valid-palindrome-ii/)

比较基础的题目。两个指针从两端开始往中间扫描，若当前的两侧字符相同，那么向内继续扫描，若当前的两侧字符不同，就尝试删去其中一个，然后检测剩下的字符串是否是回文串。

最后附上python代码：

```python
class Solution(object):
    def validPalindrome(self, s):
        """
        :type s: str
        :rtype: bool
        """

        l = 0
        r = len(s) - 1
        while l < r:
            if s[l] != s[r]:
                new_l = l + 1
                new_r = r
                while new_l < new_r and s[new_l] == s[new_r]:
                    new_l += 1
                    new_r -= 1
                if new_l >= new_r:
                    return True

                new_l = l
                new_r = r - 1
                while new_l < new_r and s[new_l] == s[new_r]:
                    new_l += 1
                    new_r -= 1
                if new_l >= new_r:
                    return True

                return False

            else:
                l += 1
                r -= 1

        return True
```
