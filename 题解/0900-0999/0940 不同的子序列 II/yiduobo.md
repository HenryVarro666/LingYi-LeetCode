---
title: "940. 不同的子序列II"
aliases: ["yiduobo的每日leetcode 940.不同的子序列II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/358466835"
zhihu_id: "358466835"
zhihu_title: "yiduobo的每日leetcode 940.不同的子序列II"
question_id: "940"
question: "不同的子序列 II"
problem_url: "https://leetcode.cn/problems/distinct-subsequences-ii/"
difficulty: "Hard"
rating: 1985
created: "2021-03-19T22:45:20+08:00"
updated: "2021-03-19T22:45:20+08:00"
upvotes: 0
comments: 0
---

# 940. 不同的子序列II

> **[yiduobo的每日leetcode 940.不同的子序列II](https://zhuanlan.zhihu.com/p/358466835) · 知乎 · 2021-03-19 · 赞同 0**
> 力扣：[940. 不同的子序列 II](https://leetcode.cn/problems/distinct-subsequences-ii/) · Hard · 灵茶山艾府：[细分问题 + 复杂度优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

940.不同的子序列II

[力扣](https://leetcode-cn.com/problems/distinct-subsequences-ii/)

题目要求找出所有子序列，那么如果不考虑重复的情况，对于一个长度为l的字符串一共就有2^l种可能性，即每一位选或者不选。另外还需要减去1，因为空串是不合法的。

接下来要想办法处理重复的情况。

不妨设字符串的形式为[XXXX]A1[YYYY]A2，其中A1和A2是相同的字符，X和Y是其他非A1字符，那么对于A1左侧的X形成的所有合法序列，设为C(X)，那么C(X) + A1与C(X) + A2是重复的子序列，于是此时有多少个C(X)，就会因为A1和A2产生多少种重复子序列。除此之外，单独的A1和A2也是重复的，这就启发我们可以使用动态规划来求解。

令f[i]表示S中从头开始到S[i]这一段可以形成多少种不同的子序列。设上面例子中A1和A2的下标分别为p1和p2，那么首先有

f[p2] \= f[p2 - 1] + f[p2 - 1] + 1

这里也很好理解，就是对于A2而言，可以选择是否将其加入答案。若不加入，则有f[p2 - 1]种合法答案。同样地，若加入，则也可以提供f[p2 - 1]中合法答案。最后，还需要考虑单独就一个A2这种情况，因此还需要加上1。

根据上面去重的结论，f[p2]还需要减去(f[p1 - 1] + 1)，即A1左侧可形成的C(X)，以及单独一个A1这种情况。

需要注意的是，由于我们在此处定义的f为不同子序列的个数，因此对于A1多次出现的情况，例如[XXXX]A1[YYYY]A2[ZZZZ]A3，我们在求解f[p3]时就只需要减去(f[p2 - 1] + 1)，因为A1与A3重复的情况以及在计算f[p2]时被清算过一次了，因此无需再次计算。

于是现在就有了一种做法，令f[i]表示S从开头到S[i]一共可以形成多少种不同的子序列：

1、首先有f[0] \= 1，即S[0]就一种可能的子序列

2、接下来从1开始遍历到len(S) - 1，对于当前的f[i]，有

f[i] \= f[i - 1] + f[i - 1] + 1

另外，若S[i]之前出现过，设last_pos为S[i]最近一次出现的位置，若last_pos > 0，则有

f[i] -\= f[last_pos - 1] + 1

否则有

f[i] -\= 1

处理完毕后，f[-1]就是最终答案

最后附上python代码：

```python
class Solution(object):
    def distinctSubseqII(self, S):
        """
        :type S: str
        :rtype: int
        """

        f = [1]
        mod = 10 ** 9 + 7
        last_pos = {S[0] : 0}
        for index in range(1, len(S)):
            char = S[index]
            f.append((f[-1] + f[-1] + 1) % mod)
            if char in last_pos:
                if last_pos[char] == 0:
                    f[-1] = (f[-1] + mod - 1) % mod
                else:
                    f[-1] = (f[-1] + mod - f[last_pos[char] - 1] - 1) % mod
            last_pos[char] = index
        
        return f[-1]
```
