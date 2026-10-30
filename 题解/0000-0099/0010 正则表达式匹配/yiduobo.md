---
title: "10. 正则表达式匹配"
aliases: ["yiduobo的每日leetcode 10.正则表达式匹配"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/四-经典线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/113995518"
zhihu_id: "113995518"
zhihu_title: "yiduobo的每日leetcode 10.正则表达式匹配"
question_id: "10"
question: "正则表达式匹配"
problem_url: "https://leetcode.cn/problems/regular-expression-matching/"
difficulty: "Hard"
created: "2020-03-17T22:26:58+08:00"
updated: "2020-03-17T22:26:58+08:00"
upvotes: 1
comments: 0
---

# 10. 正则表达式匹配

> **[yiduobo的每日leetcode 10.正则表达式匹配](https://zhuanlan.zhihu.com/p/113995518) · 知乎 · 2020-03-17 · 赞同 1**
> 力扣：[10. 正则表达式匹配](https://leetcode.cn/problems/regular-expression-matching/) · Hard · 灵茶山艾府：[教你一步步思考 DP：记忆化搜索 -> 递推 -> 空间优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

每日一题的进度有点慢，加个速。

10.正则表达式匹配<https://leetcode-cn.com/problems/regular-expression-matching/>

拿到题的第一想法是做一个自动机，但是忘了怎么弄了，所以还是老老实实用dp来做。

f[i][j]表示s中的前i个字符与p中的前j个字符是否能匹配上。

首先，有f[0][0] \= True，表示两边都是空串的时候是匹配的。

接下来，当i \= 0时，如果此时p[j - 1]是"\*"，且f[0][j - 2]能匹配空串，那么f[i][j]也能匹配空串，原理是p[j - 1]的"\*"表示p[j - 2]这个字符出现了0次。其他情况下f[0][j]都为False，因为一旦出现了字符且没有"\*"的话就匹配不了空串了。

然后是i > 0的情况：

1、当j \= 0时，f[i][j]显然为False

2、当p[j - 1]为"."时，p[j - 1]一定能匹配上s[i - 1]，因此有f[i][j] \= f[i - 1][j - 1]

3、当p[j - 1]为普通字符时，若p[j - 1] \= s[i - 1]，同样有f[i][j] \= f[i - 1][j - 1]。若p[j - 1] !\= s[i - 1]，那么f[i][j]为False

4、当p[j - 1]为"\*"时，情况就比较复杂了：

- 首先当p[j - 1]不是第一个字符时，那么不管p[j - 2]是什么，都可以认为此时p[j - 1]的"\*"表示p[j - 2]出现0次。即如果f[i][j - 2]为True，那么f[i][j] \= True。
- 接下来，当p[j - 2]是普通字符，且p[j - 2] \= s[i - 1]，或者p[j - 2] \= "."时，那么此时的\*可以表示p[j - 2]出现了1次，即如果f[i][j - 1]为True，那么f[i][j] \= True；"\*"也可以表示p[j - 2]出现了2次，即f[i][j]可以从从f[i - 1][j - 1]得到答案；除此之外，"\*"还可以表示p[j - 2]出现了多次，即从s[i - 2]开始就是靠p[j - 1]的\*表示多个p[j - 2]来进行匹配的了，所以f[i][j]也可以通过f[i - 1][j]得到答案。
- 如果上述情况中，f[i][j]的前置状态都是False，那么f[i][j]只能是False了。

f[len_s][len_p]就是要求的答案。两重循环，所以时间复杂度应该是平方的复杂度。

最后附上python代码：

```python
class Solution(object):
    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """
        len_s = len(s)
        len_p = len(p)

        f = [[False] * (len_p + 2) for index in range(len_s +2)]

        for i in range(len_s + 1):
            for j in range(len_p + 1):
                if i == 0:
                    if j == 0:
                        f[i][j] = True
                    elif p[j - 1] == '*' and f[i][j - 2]:
                        f[i][j] = True
                    else:
                        f[i][j] = False
                else:
                    if j == 0:
                        f[i][j] = False
                    elif p[j - 1] == '.':
                        f[i][j] = f[i - 1][j - 1]
                    elif p[j - 1] == '*':
                        if j >= 2 and f[i][j - 2]:
                            f[i][j] = True
                            continue
                        if p[j - 2] == '.' or p[j -2] == s[i - 1]:
                            f[i][j] = f[i][j] or f[i][j - 1] or f[i - 1][j] or f[i - 1][j - 1]
                    elif p[j - 1] == s[i - 1]:
                        f[i][j] = f[i - 1][j - 1]
                    else:
                        f[i][j] = False

        return f[len_s][len_p]
```
