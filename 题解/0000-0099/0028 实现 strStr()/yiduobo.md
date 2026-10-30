---
title: "28. 实现 strStr()"
aliases: ["yiduobo的每日leetcode 28.实现 strStr()"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/117670077"
zhihu_id: "117670077"
zhihu_title: "yiduobo的每日leetcode 28.实现 strStr()"
question_id: "28"
question: "实现 strStr()"
problem_url: "https://leetcode.cn/problems/implement-strstr/"
created: "2020-03-26T23:48:25+08:00"
updated: "2020-03-26T23:48:25+08:00"
upvotes: 0
comments: 0
---

# 28. 实现 strStr()

> **[yiduobo的每日leetcode 28.实现 strStr()](https://zhuanlan.zhihu.com/p/117670077) · 知乎 · 2020-03-26 · 赞同 0**
> 力扣：[28. 实现 strStr()](https://leetcode.cn/problems/implement-strstr/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

28.实现 strStr()<https://leetcode-cn.com/problems/implement-strstr/>

经典的字符串匹配的题目，有rk和kmp两种经典的算法，都是线性的算法。

---

**rk算法**

思路是取一个长度窗口，然后分别计算两个串在这个窗口长度中字符串的哈希值，如果哈希值相同，表示现在长度窗口中的字符是匹配的，那么逐位往后滑动这个窗口，并更新两边的哈希值。当窗口滑动到needle末尾时表示匹配结束。

这里哈希算法一般就是将字符看做26个数字，进行26进制数字计算后取模。模数一般取一个大的素数。

---

**kmp算法**

kmp算是自动机的一种，不过这里用dp的思路来解释可能更加清楚一些。

f\[i\]表示needle中以第i个字符结尾的字符串中，能与needle的前缀匹配的最长的长度，即满足needle\[ : f\[index\]\] 等于 needle\[index - f\[index\] + 1 : index + 1\]。若不存在能匹配的前缀，则有f\[index\] \= 0。

那么对于f\[i\]，首先可以知道以needle\[i - 1\]结尾的字符串能与needle的前缀匹配的最长的长度为f\[i - 1\]，那么若needle\[f\[i - 1\]\]是否与needle\[index\]相同，就可以在f\[i - 1\]的基础上加上一位，即f\[i\] \= f\[i - 1\] + 1。

如果不相同，则说明不能通过f\[i - 1\]匹配过来，但是可以通过对f\[i - 1\]进行套娃，与以needle\[f\[i - 1\]\]结尾的字符串匹配的最长前缀，即needle\[f\[f\[i - 1\] - 1\]也是有相同前缀的，因此令pos\=f\[f\[i - 1\]- 1\]， 然后不停迭代直到某个needle\[pos\]与needle\[index\]相同，或者pos移到了边界为止。此时再通过pos来更新f\[i\]即可。

通过needle计算出f之后，用相同的思路去匹配haystack即可。

最后附上python代码，这里是用kmp做的：

```python
class Solution(object):
    def strStr(self, haystack, needle):
        """
        :type haystack: str
        :type needle: str
        :rtype: int
        """

        f = []

        m = len(haystack)
        n = len(needle)

        if n == 0:
            return 0
        if m == 0:
            return -1

        pos = 0
        f.append(0)
        for index in range(1, n):
            while pos > 0 and needle[pos] != needle[index]:
                pos = f[pos - 1]
            if needle[pos] == needle[index]:
                pos += 1
            f.append(pos)

        pos = 0
        for index in range(m):
            while pos > 0 and needle[pos] != haystack[index]:
                pos = f[pos - 1]
            if needle[pos] == haystack[index]:
                pos += 1
            if pos == n:
                return index - n + 1

        return -1
```
