---
title: "2223. 构造字符串的总得分和"
aliases: ["yiduobo的每日leetcode 2223.构造字符串的总得分和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/string", "leetcode/string-matching", "题单/字符串", "题单/字符串/二-Z-函数-后缀的前缀"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/542506981"
zhihu_id: "542506981"
zhihu_title: "yiduobo的每日leetcode 2223.构造字符串的总得分和"
question_id: "2223"
question: "构造字符串的总得分和"
problem_url: "https://leetcode.cn/problems/sum-of-scores-of-built-strings/"
difficulty: "Hard"
rating: 2220
created: "2022-07-17T00:26:18+08:00"
updated: "2022-07-17T00:26:18+08:00"
upvotes: 0
comments: 0
---

# 2223. 构造字符串的总得分和

> **[yiduobo的每日leetcode 2223.构造字符串的总得分和](https://zhuanlan.zhihu.com/p/542506981) · 知乎 · 2022-07-17 · 赞同 0**
> 力扣：[2223. 构造字符串的总得分和](https://leetcode.cn/problems/sum-of-scores-of-built-strings/) · Hard · 灵茶山艾府：[O(n) 扩展 KMP](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2223.构造字符串的总得分和

[力扣](https://leetcode.cn/problems/sum-of-scores-of-built-strings/)

题目要求找出字符串所有后缀与原字符串最长公共前缀的长度之和，这是一个经典的字符串问题。

第一种做法自然是后缀数组。对于后缀相关的问题，使用后缀数组总是ok的。

第二种做法则是利用类似rk算法的字符串哈希。

我在这里采用的是第三种做法，即利用kmp算法中next数组的定义来进行计算。

首先回忆一下kmp算法next数组的定义。next\[i\]表示的是字符串中，以第i个字符结尾的字符串中，能与字符串前缀匹配的最长的长度。换言之，就是满足s\[:next\[i\]\] \= s\[i - next\[i\] + 1 : i + 1\]的最大的next\[i\]。如果无法匹配，那么就有next\[i\] \= 0。

对于本题，直接使用next数组是不合适的。例如样例的babab，其next数组分别是[0, 0, 1, 2, 3]。对于最后这个3，表示的最后的三个字符bab与babab的公共前缀长度为3。

乍一看确实就是想要的，但是仔细分析其实有两个问题：

1、这里的3是基于最后一个字符b得到的，而在这之前分别存在一个b和ba与babab的前缀匹配，也就是next数组中的1和2。换言之，next数组中有三个数表示的是同一个后缀，这也就意味着统计的时候不能直接将这个next[i] \= 3加入到答案中，因为可能产生重复。

2、这里只统计到了bab这一个后缀，但是最后之后的两个后缀，也就是ab和b都没有计算到，其中b本身也是可以匹配的。而对于next数组中的2，也就是原字符串中的s[3] \= 'a'而言，应该判断的后缀为ab，但是实际上next[3] \= 2代表的是字符串中的第2、3个字符，也就是ba，这完全就不是我们想要的。

对于这两个问题，第一个问题相对好解决。在这里将统计长度转化为统计次数就行了。具体来说，就是对于bab这样长度为3的匹配，转化为bab的匹配、ba的匹配以及b的匹配，也就是对应next数组中后面的1、2、3的三次匹配，这样就可以避免重复计算的问题。

而对于第二个问题则复杂一点，需要再从kmp中next数组出发来解决。简单来说，现在的问题就是对于bab中的ab以及b这两种情况无法计算出其与babab前缀匹配的长度，那么在这里可以进行转化。

由于next[4] \= 3，也就是说babab的最后3个字符实际上与babab的前三个字符是完全相同的，那么第三、四个字符的ab，以及第四个字符单独的b，这两个后缀与babab的匹配，就可以转化成字符串中第一、二个字符的ab，以及第二个字符单独的b，这两个后缀的前缀与babab的匹配，在这里恰好又回到了next数组的定义。不过需要注意的是，按next的计算方式，每次之能往回走一层，也就是找出最长的匹配，那么需要不断向前迭代，也就是

next[i] -> next[next[i] - 1] -> next[next[next[i] - 1] - 1] -> ... -> 0

到了这里就得到了一种做法。由于是统计次数，那么可以令g\[i\]表示能与字符串前缀匹配i个字符的子串出现的次数，那么首先可以利用next数组来初始化g，即对于所有的next\[i\]，先让g\[next\[i\]\]加上1。

接下来，根据对第二个问题的分析，每个next[i]除了本身需要计数之外，其套娃的next[next[i] - 1]，next[next[next[i] - 1] - 1]等也需要计数，因此需要从大到小枚举i，使用g[next[i] - 1] +\= g[i]来完成计数。

动态规划完成后，根据g数组的定义，所有有匹配长度的匹配都应该计算一次，那么就应该将g数组中除了g[0]之外的所有数都加起来。另外，这里并没有计算到字符串本体，因此还需要在这个和的基础上再加上字符串的长度才是最终答案。

最后附上python代码：

```python
class Solution(object):
    def sumScores(self, s):
        """
        :type s: str
        :rtype: int
        """

        pos = 0
        f = [0]
        n = len(s)
        for index in range(1, n):
            while pos > 0 and s[pos] != s[index]:
                pos = f[pos - 1]
            if s[pos] == s[index]:
                pos += 1
            f.append(pos)

        g = [0] * n
        for index in range(n):
            g[f[index]] += 1
        
        for index in range(n - 1, 0, -1):
            g[f[index - 1]] += g[index]

        return n + sum(g[1:])
```
