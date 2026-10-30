---
title: "266. 回文排列"
aliases: ["yiduobo的每日leetcode 266.回文排列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/593493958"
zhihu_id: "593493958"
zhihu_title: "yiduobo的每日leetcode 266.回文排列"
question_id: "266"
question: "回文排列"
problem_url: "https://leetcode.cn/problems/palindrome-permutation/"
created: "2022-12-21T23:55:26+08:00"
updated: "2022-12-21T23:55:26+08:00"
upvotes: 0
comments: 0
---

# 266. 回文排列

> **[yiduobo的每日leetcode 266.回文排列](https://zhuanlan.zhihu.com/p/593493958) · 知乎 · 2022-12-21 · 赞同 0**
> 力扣：[266. 回文排列](https://leetcode.cn/problems/palindrome-permutation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

266.回文排列

[力扣](https://leetcode.cn/problems/palindrome-permutation/)

对于一个回文串，除中心字符外的所有字符都是成对出现的，换言之，回文串中落单的字符数量只能是0个或者1个。根据这个结论，就可以对s进行一趟遍历，统计其中落单字符的数量。若不超过1个，那么就返回true，否则就返回false。

最后附上python代码：

```python
class Solution(object):
    def canPermutePalindrome(self, s):
        """
        :type s: str
        :rtype: bool
        """

        char_set = set()
        for char in s:
            if char not in char_set:
                char_set.add(char)
            else:
                char_set.remove(char)
        
        return len(char_set) <= 1
```
