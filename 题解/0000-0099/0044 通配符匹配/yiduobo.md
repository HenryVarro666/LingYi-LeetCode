---
title: "44. 通配符匹配"
aliases: ["yiduobo的每日leetcode 44.通配符匹配"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/string", "leetcode/zheng-ze-biao-da-shi", "leetcode/zheng-ze", "题单/动态规划", "题单/动态规划/四-经典线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/124324820"
zhihu_id: "124324820"
zhihu_title: "yiduobo的每日leetcode 44.通配符匹配"
question_id: "44"
question: "通配符匹配"
problem_url: "https://leetcode.cn/problems/wildcard-matching/"
difficulty: "Hard"
created: "2020-04-03T23:58:50+08:00"
updated: "2020-04-03T23:58:50+08:00"
upvotes: 0
comments: 0
---

# 44. 通配符匹配

> **[yiduobo的每日leetcode 44.通配符匹配](https://zhuanlan.zhihu.com/p/124324820) · 知乎 · 2020-04-03 · 赞同 0**
> 力扣：[44. 通配符匹配](https://leetcode.cn/problems/wildcard-matching/) · Hard · 灵茶山艾府：[Go 库函数正则匹配](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

44.通配符匹配<https://leetcode-cn.com/problems/wildcard-matching/>

前面某道正则匹配的升级版，使用平方的dp依然是可以做的，但是在这里会超时。

注意到星号在这里非常强悍，可以匹配任意字符串，那么在遇到一个星号时，我们可以假设其匹配了零个字符，然后往后匹配。当匹配不了时，让星号往后兼容s中的一个字符，再从星号后面重新开始匹配。这样做可以省去很多不必要的比较，但是具体时间复杂度不太好分析。

最后附上python代码：

```python
class Solution(object):
    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """

        m = len(s)
        n = len(p)
        i = 0
        j = 0
        s_pos = -1
        p_pos = -1

        while i < m:
            if j < n and (p[j] == '?' or p[j] == s[i]):
                i += 1
                j += 1
            elif j < n and p[j] == '*':
                s_pos = i
                p_pos = j
                j += 1
            elif s_pos >= 0:
                s_pos += 1
                i = s_pos
                j = p_pos
            else:
                return False

        for index in range(j, n):
            if p[index] != '*':
                return False
        
        return True
```
