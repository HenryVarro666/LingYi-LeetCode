---
title: "1750. 删除字符串两端相同字符后的最短长度"
aliases: ["yiduobo的每日leetcode 1750.删除字符串两端相同字符后的最短长度"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/454880007"
zhihu_id: "454880007"
zhihu_title: "yiduobo的每日leetcode 1750.删除字符串两端相同字符后的最短长度"
question_id: "1750"
question: "删除字符串两端相同字符后的最短长度"
problem_url: "https://leetcode.cn/problems/minimum-length-of-string-after-deleting-similar-ends/"
created: "2022-01-08T19:59:36+08:00"
updated: "2022-01-08T19:59:36+08:00"
upvotes: 0
comments: 0
---

# 1750. 删除字符串两端相同字符后的最短长度

> **[yiduobo的每日leetcode 1750.删除字符串两端相同字符后的最短长度](https://zhuanlan.zhihu.com/p/454880007) · 知乎 · 2022-01-08 · 赞同 0**
> 力扣：[1750. 删除字符串两端相同字符后的最短长度](https://leetcode.cn/problems/minimum-length-of-string-after-deleting-similar-ends/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1750.删除字符串两端相同字符后的最短长度

[力扣](https://leetcode-cn.com/problems/minimum-length-of-string-after-deleting-similar-ends/)

由于题目要求只有当两端字符相同时才能执行删除操作，设这个字符为char，那么如果其中某一端在删除操作完成后没有删干净但另一端全部删掉了，那么此时对于两端的字符而言，其中没删干净的那一端依然是char，而另一端必然不是char，此时就无法继续删除操作了。因此为了尽可能多的删除字符，在可以删除的时候就应该将两端的字符都删除干净，那么就有了一种做法：

使用两个指针l和r从两端向中间扫：

1、若此时s[l] \= s[r]，那么说明还可以执行删除操作，需要将两端等于s[l]的字符都删除掉。

首先考察l这一侧。若l \< r且s[l] \= s[r]，那么就将l向后移动，直到l等于r或者s[l]不等于s[r]。

若l等于r，说明s中的字符都一样可以全部删除，此时直接返回0即可。

若l不等于r，说明l和r直接还有s[l]之外的字符，此时则需要操作r这一侧。

接下来考察r这一侧。

若s[r] \= s[l - 1]，那么就将r向前移动，直到s[r]不等于s[l - 1]。

此时可以认为删除了两侧的字符，只剩下l到r之间的字符需要考虑了。

2、若此时s[l] !\= s[r]，那么说明已经无法继续执行删除操作了，剩下字符串的长度就是r - l + 1。

最后附上python代码：

```python
class Solution(object):
    def minimumLength(self, s):
        """
        :type s: str
        :rtype: int
        """

        l = 0
        r = len(s) - 1
        while l < r and s[l] == s[r]:
            while l < r and s[l] == s[r]:
                l += 1
            
            if l == r:
                return 0
            
            while s[r] == s[l - 1]:
                r -= 1
            
        return r - l + 1
```
