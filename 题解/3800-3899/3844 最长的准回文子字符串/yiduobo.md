---
title: "3844. 最长的准回文子字符串"
aliases: ["yiduobo的每日leetcode 3844.最长的准回文子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration", "leetcode/suffix-array", "题单/字符串", "题单/字符串/三-Manacher-算法-回文串", "题单/字符串/四-字符串哈希", "题单/字符串/八-后缀数组/后缀自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2010154524833247430"
zhihu_id: "2010154524833247430"
zhihu_title: "yiduobo的每日leetcode 3844.最长的准回文子字符串"
question_id: "3844"
question: "最长的准回文子字符串"
problem_url: "https://leetcode.cn/problems/longest-almost-palindromic-substring/"
difficulty: "Medium"
rating: 1990
created: "2026-03-01T01:45:01+08:00"
updated: "2026-03-01T01:45:05+08:00"
upvotes: 0
comments: 0
---

# 3844. 最长的准回文子字符串

> **[yiduobo的每日leetcode 3844.最长的准回文子字符串](https://zhuanlan.zhihu.com/p/2010154524833247430) · 知乎 · 2026-03-01 · 赞同 0**
> 力扣：[3844. 最长的准回文子字符串](https://leetcode.cn/problems/longest-almost-palindromic-substring/) · Medium · 灵茶山艾府：[两种方法：中心扩展法 / Manacher 算法 + 后缀数组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3844.最长的准回文子字符串

<https://leetcode.cn/problems/longest-almost-palindromic-substring/description/>

题目给出一个由小写英文字母组成的字符串s。

若一个子字符串在恰好删掉一个字符后变成回文字符串，就称其是准回文串。

要求找出s中最长的准回文串的长度。

首先可以明确的是，一个标准的回文串必然也是一个准回文串：若这个回文串长度为奇数，删掉中心字符后依然是回文串；若其长度为偶数，则删掉中心两个字符的其中之一，得到的依然是回文串。

而对于非标准回文串，其必然可以拆解为三个部分，分别为：

- 中心回文部分。这个部分是一个完整的回文串，其长度可以是奇数也可以是偶数
- 单个额外字符。这个字符就是恰好删掉的那个字符
- 外侧回文部分。这个部分是从内向外的若干组相同的字符，也可以为空

基于上面的结论，就可以先一趟遍历，以s[index]为中心向两侧扩展，得到中心回文部分。若s[index]与s[index - 1]相同，也可以以s[index - 1]与s[index]为中心向两侧扩展，得到中心回文部分。

无论是哪一种，都可以先用这个中心回文的长度更新答案，接下来对于当前扩展得到的[left, right]，可以选择left - 1或者right + 1作为单个额外字符，接下来再从[left - 2, right + 1]以及[left - 1, right + 2]开始向两侧扩展外侧回文部分，使用最终的长度更新答案。

最后附上python代码：

```python
class Solution(object):
    def almostPalindromic(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        def calc(left, right):
            while left > 0 and right + 1 < n and s[left - 1] == s[right + 1]:
                left -= 1
                right += 1
            
            if right - left + 1 == n:
                return n
            
            ma = 0
            
            if left > 0:
                p1 = left - 1
                p2 = right
                while p1 > 0 and p2 + 1 < n and s[p1 - 1] == s[p2 + 1]:
                    p1 -= 1
                    p2 += 1
                
                ma = max(ma, p2 - p1 + 1)
            
            if right + 1 < n:
                p1 = left
                p2 = right + 1
                while p1 > 0 and p2 + 1 < n and s[p1 - 1] == s[p2 + 1]:
                    p1 -= 1
                    p2 += 1
                ma = max(ma, p2 - p1 + 1)

            return ma

        res = 0
        n = len(s)

        for index in range(n):
            res = max(res, calc(index, index))
            if res == n:
                break
            
            if index > 0 and s[index - 1] == s[index]:
                res = max(res, calc(index - 1, index))
            if res == n:
                break

        return res
```
