---
title: "3333. 找到初始输入字符串II"
aliases: ["yiduobo的每日leetcode 3333.找到初始输入字符串II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "leetcode/prefix-sum", "题单/动态规划", "题单/数学算法", "题单/动态规划/三-背包", "题单/动态规划/十一-优化-DP", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/24662997065"
zhihu_id: "24662997065"
zhihu_title: "yiduobo的每日leetcode 3333.找到初始输入字符串II"
question_id: "3333"
question: "找到初始输入字符串 II"
problem_url: "https://leetcode.cn/problems/find-the-original-typed-string-ii/"
difficulty: "Hard"
rating: 2629
created: "2025-02-19T00:41:38+08:00"
updated: "2025-02-19T00:41:38+08:00"
upvotes: 1
comments: 0
---

# 3333. 找到初始输入字符串II

> **[yiduobo的每日leetcode 3333.找到初始输入字符串II](https://zhuanlan.zhihu.com/p/24662997065) · 知乎 · 2025-02-19 · 赞同 1**
> 力扣：[3333. 找到初始输入字符串 II](https://leetcode.cn/problems/find-the-original-typed-string-ii/) · Hard · 灵茶山艾府：[前缀和优化多重背包（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3333.找到初始输入字符串II

[3333. 找到初始输入字符串 II - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-original-typed-string-ii/description/)

之前3330题的加强版，不过题设变化比较大，做法也完全不同。

题目给出一个字符串word，这个字符串是逐个字符输入得到的，但是在输入过程中可能存在若干次误输入，这里的误输入指的是某个字符被重复输入了多次。另外给出一个正整数k，表示一开始想要输入的字符串长度至少为k，现在要求从word和k反推出一开始想要输入的字符串有多少种可能。

首先考虑边界情况，若word的长度小于k，那么答案显然为0。

接下来是一般情况。根据题目中误输入的定义，那么误输入一定会形成相同字符构成的子串，于是可以先一趟遍历，将word分离成若干段相同字符构成的子串。

不妨设这些子串一共有t段，每个子串的长度分别为cnt[0]到cnt[t - 1]，那么最短的原始字符串就是由着t种字符各一个构成的。例如样例1和样例2中的'aabbccdd'，最短的原始字符串就是'abcd'，而cnt则为[2, 2, 2, 2]；对于样例3中的'aaabbb'，最短的原始字符串就是'ab'，而cnt则为[3, 3]。

接下来又可以分为两种情况：

1、t >\= k：

这种情况下最短的原始字符串长度已经达标，因此原始字符串中的每种字符数量是比较自由的。更具体的，对于第index种字符，其可能的数量可以是1到cnt[index]，因此只需将cnt中的所有元素累乘起来即为最终答案。

2、t \< k：

这种情况下最短的原始字符串长度是不够的，还需要补充额外的k - t个字符才能达标，实际上需要计算的就是从这t种字符中，除去构成最短字符串的t种字符各一个之外，额外选出若干字符构成长度大于等于k - t的字符串的方案数。在这里直接计算是比较困难的，因为字符串长度可能的取值范围非常大，不过注意到k的取值范围很小，因此可以利用上面情况1的结果反过来计算。

具体来说，就是长度至少的为k的原始字符串的数量，等于情况1中计算的所有可能的原始字符串数量，减去长度小于k的原始字符串的数量，而后面这个值在转化后可以通过动态规划求解：

令f[index][total]表示由第0种到第index种字符中除去构成最短原始字符串后剩下的多余字符中选出total个字符的方案数，那么对于f[index][total]：

1）若cnt[index] \= 1：

这种情况下第index种字符已经填到最短可能字符串里面去了，没有额外的字符可用，因此有

f[index][total] \= f[index - 1][total]

2）若cnt[index] - 1 >\= total：

这种情况下第index种字符的余量很足，可能的取值范围为0到total。

若当前字符取0个，那么就要求前面的字符一共取total个，取1个则要求前面的字符一共取total - 1个，以此类推，于是有

f[index][total] \= f[index - 1][total] + f[index - 1][total - 1] + ... + f[index - 1][0]

3）若cnt[index] - 1 \< total：

这种情况下第index种字符的数量不足total个，可能的取值范围为0到cnt[index] - 1。与情况2）类似，在这里有

f[index][total] \= f[index - 1][total] + f[index - 1][total - 1] + ... + f[index - 1][total - (cnt[index] - 1)]

计算完成后，f[t - 1][0] + f[t - 1][1] + ... + f[t - 1][k - t - 1]就是从多余字符中选出若干字符，构成长度不足k - t的字符串的方案数，将这些方案从情况1中的方案数中减去即为最终答案。

---

到了这里还有一个问题，情况2中动态规划的时间复杂度太高了，需要进行优化。

注意到f的更新是上一轮状态的区间和，于是可以使用前缀和来进行优化。

f的状态表示保持不变，令s[index][total]表示f[index][0] + f[index][1] + ... + f[index][total]之和，那么对于上面的转移方程，就可以改写成

1）若cnt[index] \= 1：

这种情况下不变

2）若cnt[index] - 1 >\= total：

f[index][total] \= f[index - 1][total] + f[index - 1][total - 1] + ... + f[index - 1][0]

后面的连加恰好就是s的定义，于是有

f[index][total] \= s[index - 1][total]

3）若cnt[index] - 1 \< total：

f[index][total] \= f[index - 1][total] + f[index - 1][total - 1] + ... + f[index - 1][total - (cnt[index] - 1)]

后面的连加可以写成前缀和之差的形式，于是有

f[index][total] \= s[index - 1][total] - s[index - 1][total - (cnt[index] - 1) - 1]

计算出所有的f[index][total]后，只需一趟遍历，使用f[index][total]来更新是s[index][total]即可。

另外由于f和s的每一轮之和上一轮有关，因此可以利用s和f的相互迭代省去index这一维。

最后附上python代码：

```python
class Solution(object):
    def possibleStringCount(self, word, k):
        """
        :type word: str
        :type k: int
        :rtype: int
        """
        
        if len(word) < k:
            return 0

        cnt = []
        pre = 0
        t = 0
        for index in range(1, len(word)):
            if word[index] != word[index - 1]:
                t += 1
                cnt.append(index - pre)
                pre = index
        
        t += 1
        cnt.append(len(word) - pre)
        k = max(0, k - t)

        res = 1
        mod = 10 ** 9 + 7
        for c in cnt:
            res = res * c % mod

        if k > 0:
            f = [0] * k
            s = [1] * k
            for c in cnt:
                if c == 1:
                    continue
                c -= 1

                for total in range(k):
                    if c >= total:
                        f[total] = s[total]
                    else:
                        f[total] = (s[total] - s[total - c - 1] + mod) % mod

                s[0] = f[0]
                for total in range(1, k):
                    s[total] = (s[total - 1] + f[total]) % mod

            for total in range(k):
                res -= f[total]
                if res < 0:
                    res += mod

        return res
```
