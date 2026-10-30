---
title: "267. 回文排列II"
aliases: ["yiduobo的每日leetcode 267.回文排列II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/593733036"
zhihu_id: "593733036"
zhihu_title: "yiduobo的每日leetcode 267.回文排列II"
question_id: "267"
question: "回文排列II"
problem_url: "https://leetcode.cn/problems/palindrome-permutation-ii/"
created: "2022-12-23T01:37:09+08:00"
updated: "2022-12-23T01:37:09+08:00"
upvotes: 0
comments: 0
---

# 267. 回文排列II

> **[yiduobo的每日leetcode 267.回文排列II](https://zhuanlan.zhihu.com/p/593733036) · 知乎 · 2022-12-23 · 赞同 0**
> 力扣：[267. 回文排列II](https://leetcode.cn/problems/palindrome-permutation-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

267.回文排列II

[力扣](https://leetcode.cn/problems/palindrome-permutation-ii/)

本题首先需要判断是否可以形成回文排列，然后再找出所有可行的排列。

对于判断的问题，可以直接照搬之前266题的做法：

[yiduobo：yiduobo的每日leetcode 266.回文排列](https://zhuanlan.zhihu.com/p/593493958)

如果可以形成回文排列，那么在这里就只需找出所有可行排列的前半部分，也就是找出所有成对出现字符的所有可行排列。对于这个问题，则可以参考之前47题的做法：

[yiduobo：yiduobo的每日leetcode 47.全排列II](https://zhuanlan.zhihu.com/p/125766510)

在枚举到一种可行的排列后，将其与反转后的排列拼接起来就得到了一种可行的回文排列了。需要注意如果字符串的长度为奇数，那么就存在一个落单的字符，此时需要将这个字符置于枚举到的排列与反转排列的中间，作为回文排列的中心字符。

最后附上python代码：

```python
class Solution(object):
    def generatePalindromes(self, s):
        """
        :type s: str
        :rtype: List[str]
        """

        char_dict = {}
        char_set = set()

        for char in s:
            if char in char_set:
                char_dict[char] = char_dict.get(char, 0) + 1
                char_set.remove(char)
            else:
                char_set.add(char)
        
        if len(char_set) >= 2:
            return []
        
        if len(char_set) == 1:
            mid = list(char_set)[0]
        else:
            mid = ''
        
        res = []
        
        def dfs(level, now, char_dict, res):
            if level == len(s) / 2:
                res.append('')
                for char in now:
                    res[-1] += char
                res[-1] += mid
                for char in now[::-1]:
                    res[-1] += char
                return
            
            for char in char_dict:
                if char_dict[char] > 0:
                    char_dict[char] -= 1
                    now.append(char)
                    dfs(level + 1, now, char_dict, res)
                    now.pop()
                    char_dict[char] += 1
        
        dfs(0, [], char_dict, res)
        return res
```
