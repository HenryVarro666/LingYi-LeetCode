---
title: "1332. 删除回文子序列"
aliases: ["yiduobo的每日leetcode 1332.删除回文子序列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/394986447"
zhihu_id: "394986447"
zhihu_title: "yiduobo的每日leetcode 1332.删除回文子序列"
question_id: "1332"
question: "删除回文子序列"
problem_url: "https://leetcode.cn/problems/remove-palindromic-subsequences/"
created: "2021-07-31T17:30:37+08:00"
updated: "2021-07-31T17:30:37+08:00"
upvotes: 0
comments: 0
---

# 1332. 删除回文子序列

> **[yiduobo的每日leetcode 1332.删除回文子序列](https://zhuanlan.zhihu.com/p/394986447) · 知乎 · 2021-07-31 · 赞同 0**
> 力扣：[1332. 删除回文子序列](https://leetcode.cn/problems/remove-palindromic-subsequences/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1332.删除回文子序列

[力扣](https://leetcode-cn.com/problems/remove-palindromic-subsequences/)

题目描述看上去还蛮复杂的，不过题目这里是删去子序列，而且字符串中只有a和b两种字符。当一个字符中所有字符相同时，该字符串必然是回文串，因此我们最多只需要两步就能删完，即先选出字符串中的所有a，此时必然能形成一个回文串。删去所有a之后，剩下的全都是b，同样是一个回文串，因此只需要两步就能完成删除。

当然，若字符串本身就是回文串，那么只需要一步就能删完，因此在这里我们可以先判断字符串是否为回文串，若是，那么答案为1，否则答案为2。

最后附上python代码：

```python
class Solution(object):
    def removePalindromeSub(self, s):
        """
        :type s: str
        :rtype: int
        """

        if len(s) == 0:
            return 0
        
        l = 0
        r = len(s) - 1
        while l < r and s[l] == s[r]:
            l += 1
            r -= 1
        
        if l >= r:
            return 1
        
        return 2
```
