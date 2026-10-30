---
title: "97. 交错字符串"
aliases: ["yiduobo的每日leetcode 97.交错字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/面试经典-150-题", "题单/动态规划/四-经典线性-DP", "题单/面试经典-150-题/多维动态规划"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/137322145"
zhihu_id: "137322145"
zhihu_title: "yiduobo的每日leetcode 97.交错字符串"
question_id: "97"
question: "交错字符串"
problem_url: "https://leetcode.cn/problems/interleaving-string/"
difficulty: "Medium"
created: "2020-04-29T21:45:34+08:00"
updated: "2020-04-29T21:45:34+08:00"
upvotes: 0
comments: 0
---

# 97. 交错字符串

> **[yiduobo的每日leetcode 97.交错字符串](https://zhuanlan.zhihu.com/p/137322145) · 知乎 · 2020-04-29 · 赞同 0**
> 力扣：[97. 交错字符串](https://leetcode.cn/problems/interleaving-string/) · Medium · 灵茶山艾府：[教你一步步思考动态规划：从记忆化搜索到递推到空间优化！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

97.交错字符串<https://leetcode-cn.com/problems/interleaving-string/>

动态规划的题目。实际上，这么多题目看下来，与串有关的问题中，涉及到位置匹配的，大多数都是动态规划去解决，状态也一般是某个串的前i位与某个串的前j位满足XXXX。

这里也不例外，f[i][j]表示s1的前i位与s2的前j位交错后能否构成s3的前i + j位，于是有：

1、i与j都为0。意思是s1和s2都为空，且s3也为空，于是此时f[i][j] \= True。

2、i为0，j不为0。说明此时s3必须由s2单独进行匹配，于是当f[i][j - 1]为True，即s2的前j - 1位能与s3匹配上，且s2[j - 1] \=\= s3[j - 1]，即当前第j位也能匹配上，那么就有f[i][j] \= True，否则f[i][j] \= False。

3、i不为0，j为0。与情况2相反，说明此时s3需要由s1单独匹配，于是当f[i - 1][j]为True，且s1[i - 1] \=\= s3[i - 1]，则f[i][j] \= True，否则f[i][j] \= False。

4、i和j都不为0。此时s3的第i + j位可能由s1的第i位或者s2的第j位来匹配，于是当f[i - 1][j]为True且s1[i - 1] \=\= s3[i + j - 1]，或者f[i][j - 1]为True且s2[j - 1] \=\= s3[i + j - 1]，那么就有f[i][j] \= True，否则f[i][j] \= False。

最后f[m][n]即为最后的答案。

当然，这里也可以用滚动数组来优化掉f的一维，于是最后的时间复杂度为O(mn)，空间复杂度为O(min(m, n))。

最后附上python代码，简单起见，这里没有使用滚动数组：

```python
class Solution(object):
    def isInterleave(self, s1, s2, s3):
        """
        :type s1: str
        :type s2: str
        :type s3: str
        :rtype: bool
        """

        m = len(s1)
        n = len(s2)
        if m + n != len(s3):
            return False

        f = [[False] * (n + 1) for index in range(m + 1)]

        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0:
                    if j == 0:
                        f[i][j] = True
                    elif f[i][j - 1] and s2[j - 1] == s3[j - 1]:
                        f[i][j] = True
                else:
                    if j == 0:
                        if f[i - 1][j] and s1[i - 1] == s3[i - 1]:
                            f[i][j] = True
                    elif (f[i - 1][j] and s1[i - 1] == s3[i + j - 1]) or (f[i][j - 1] and s2[j - 1] == s3[i + j - 1]):
                        f[i][j] = True

        return f[m][n]
```
