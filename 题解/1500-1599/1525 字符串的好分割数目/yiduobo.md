---
title: "1525. 字符串的好分割数目"
aliases: ["yiduobo的每日leetcode 1525.字符串的好分割数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/422192268"
zhihu_id: "422192268"
zhihu_title: "yiduobo的每日leetcode 1525.字符串的好分割数目"
question_id: "1525"
question: "字符串的好分割数目"
problem_url: "https://leetcode.cn/problems/number-of-good-ways-to-split-a-string/"
created: "2021-10-16T16:13:17+08:00"
updated: "2021-10-16T16:13:17+08:00"
upvotes: 0
comments: 0
---

# 1525. 字符串的好分割数目

> **[yiduobo的每日leetcode 1525.字符串的好分割数目](https://zhuanlan.zhihu.com/p/422192268) · 知乎 · 2021-10-16 · 赞同 0**
> 力扣：[1525. 字符串的好分割数目](https://leetcode.cn/problems/number-of-good-ways-to-split-a-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1525.字符串的好分割数目

[力扣](https://leetcode-cn.com/problems/number-of-good-ways-to-split-a-string/)

从左向右一趟扫描，枚举每种分割的情况。对于每种情况，判断左侧和右侧中不同字符的数目即可。

最后附上python代码：

```python
class Solution(object):
    def numSplits(self, s):
        """
        :type s: str
        :rtype: int
        """

        left = set()
        right = {}
        for char in s:
            right[char] = right.get(char, 0) + 1
        
        res = 0
        for char in s:
            left.add(char)
            right[char] -= 1
            if right[char] == 0:
                right.pop(char)
            
            if len(left) == len(right):
                res += 1
        
        return res
```
