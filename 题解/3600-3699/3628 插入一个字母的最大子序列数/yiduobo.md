---
title: "3628. 插入一个字母的最大子序列数"
aliases: ["yiduobo的每日leetcode 3628.插入一个字母的最大子序列数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/四-经典线性-DP", "题单/动态规划/六-状态机-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1945527589532866043"
zhihu_id: "1945527589532866043"
zhihu_title: "yiduobo的每日leetcode 3628.插入一个字母的最大子序列数"
question_id: "3628"
question: "插入一个字母的最大子序列数"
problem_url: "https://leetcode.cn/problems/maximum-number-of-subsequences-after-one-inserting/"
difficulty: "Medium"
rating: 1754
created: "2025-08-31T17:07:06+08:00"
updated: "2025-08-31T17:07:06+08:00"
upvotes: 0
comments: 0
---

# 3628. 插入一个字母的最大子序列数

> **[yiduobo的每日leetcode 3628.插入一个字母的最大子序列数](https://zhuanlan.zhihu.com/p/1945527589532866043) · 知乎 · 2025-08-31 · 赞同 0**
> 力扣：[3628. 插入一个字母的最大子序列数](https://leetcode.cn/problems/maximum-number-of-subsequences-after-one-inserting/) · Medium · 灵茶山艾府：[两种方法：复用 115 题代码 / 状态机 DP + 前后缀分解（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3628.插入一个字母的最大子序列数

[3628. 插入一个字母的最大子序列数 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-number-of-subsequences-after-one-inserting/description/)

题目给出一个由大写字母组成的字符串s。现在可以在字符串的任意位置最多插入一个大写字母，问插入字母后字符串中可以形成的LCT子序列的最大数量。

插入的字符必然是L、C、T三者之一，如果插入的是L，那么插入到头部是最优的，新增的LCT序列的数目就是原始字符串中CT序列的数目；同样的，如果插入的是T，那么插入到尾部是最优的，新增的LCT序列的数目就是原始字符串中LC序列的数目。而对于C，则应该插入到中间某处，新增的LCT序列的数目为其左侧L的数目乘以右侧C的数目。

另一方面，由于题目要找的是LCT的总数，因此还需要计算原始字符串中LCT的数目。对于这个问题，可以利用动态规划进行求解。令L[index]，LC[index]以及LCT[index]记录前index个字符中L、LC序列以及LCT序列的数目，那么：

1、对于L[index]，若s[index]为'L'，那么就有L[index] \= L[index - 1] + 1，否则L[index]就是L[index - 1]

2、对于LC[index]，若s[index]为'C'，那么就有LC[index] \= LC[index - 1] + L[index - 1]，否则LC[index]就是LC[index - 1]

3、对于LCT[index]，若s[index]为'T'，那么就有LCT[index] \= LCT[index - 1] + LC[index - 1]，否则LCT[index]就是LCT[index - 1]

这里的L、LC、LCT都可以利用变量迭代省去index这一维，不过在新插入C的时需要知道每个位置左侧L的数目，因此在这里可以保留L数组，然后使用变量迭代计算LC和LCT。

到了这里，就得到了原始字符串中LCT序列的总数，接下来还需要计算每个位置右侧T的数目，以及原始字符串中ct序列的数目。对于这两个问题，则可以按照上面计算LCT序列相同的方式，从后往前一趟遍历利用动态规划求解。令T和CT分别计算当前后缀中T和CT序列的数目，那么从后往前遍历：

1、对于T，若当前字符为'T'，那么就将T加上1，否则T不变。另一方面，结合之前得到的L数组，就可以计算在当前位置插入C后新得到的LCT序列，也就是当前位置对应的L，乘以当前的T，方便期间，记其中乘积的最大值为best

2、对于CT，若当前字符为'C'，那么就将其加上T，否则CT不变。

计算完成后，取best、LC、CT中的最大值，也就是插入C到字符串中间、插入T到字符串末尾、插入L到字符串头部这三种情况可以得到的新LCT序列的最大值，再加上原始的LCT即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def numOfSubsequences(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        L = [0]
        LC = 0
        LCT = 0
        for c in s:
            if c == 'L':
                L.append(L[-1] + 1)
            else:
                if c == 'C':
                    LC += L[-1]
                elif c == 'T':
                    LCT += LC
                L.append(L[-1])
        
        L.pop()
        T = 0
        CT = 0
        best = 0
        for c in s[::-1]:
            if c == 'T':
                T += 1
            elif c == 'C':
                CT += T
            
            best = max(best, L[-1] * T)
            L.pop()
        
        return max(best, LC, CT) + LCT
```
