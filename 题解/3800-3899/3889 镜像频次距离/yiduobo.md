---
title: "3889. 镜像频次距离"
aliases: ["yiduobo的每日leetcode 3889.镜像频次距离"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2024471041926243371"
zhihu_id: "2024471041926243371"
zhihu_title: "yiduobo的每日leetcode 3889.镜像频次距离"
question_id: "3889"
question: "镜像频次距离"
problem_url: "https://leetcode.cn/problems/mirror-frequency-distance/"
difficulty: "Medium"
created: "2026-04-06T14:04:07+08:00"
updated: "2026-04-06T14:04:10+08:00"
upvotes: 0
comments: 3
---

# 3889. 镜像频次距离

> **[yiduobo的每日leetcode 3889.镜像频次距离](https://zhuanlan.zhihu.com/p/2024471041926243371) · 知乎 · 2026-04-06 · 赞同 0**
> 力扣：[3889. 镜像频次距离](https://leetcode.cn/problems/mirror-frequency-distance/) · Medium · 灵茶山艾府：[阅读理解（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3889.镜像频次距离

<https://leetcode.cn/problems/mirror-frequency-distance/description/>

题目给出一个由小写英文字母和数字组成的字符串s。

对于每个字符，其镜像字符根据逆序定义其字符集合：

- 对于字母，某字符的镜像字符是字母表中从某尾与其位置相同的字母。例如'a'对应的是'z'，'b'对应的是'y'，以此类推。
- 对于数字，某字符的镜像字符是范围'0'到'9'中从末尾与其位置相同的数字。例如'0'对应的是'9'，'1'对应的是'8'，以此类推。

对于s中每种字符c，设m为其镜像字符，freq(x)表示字符x在字符串中出现的次数，计算其与镜像字符出现次数之间的绝对差，即|freq(c) - freq(m)|。

镜像对(c, m)和(m, c)被视为相同，只能被计算一次。

要求计算所有不同镜像对的绝对差之和。

由于题目需要计算的是不同镜像对的绝对差之和，在这里可以使用一个哈希表freq记录每种镜像对出现次数之差，但是只记录先半部分字母和数字的。具体来说，若某个字符c处于前半段，例如'0'到'4'，或者'a'到'm'，那么就将freq[c]加上1，反之则计算c的镜像字符m，然后将freq[m]减去1。

而对于镜像字符的求解，数字的镜像字符是很好找的。由于是首位配对，因此一组镜像数字之和必然是9，那么若某个字符c是数字，就可以先将其转化为数字类型，然后用9减去，就得到镜像字符。

另一方面对于字母，也可以利用配对的思路，利用ascii码来进行计算。具体来说，所有镜像字母的ascii之和都是相同的，刚好等于ord('a') + ord('z')，那么对于字母c，就可以通过chr(ord('a') + ord('z') - ord(c))计算得到c的镜像字母。

全部计算完成后，遍历freq，将差值的绝对值累加起来即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def mirrorFrequency(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        freq = {}
        for c in s:
            if '0' <= c <= '4':
                v = int(c)
                delta = 1
            elif '5' <= c <= '9':
                v = 9 - int(c)
                delta = -1
            elif 'a' <= c <= 'm':
                v = c
                delta = 1
            else:
                v = chr(ord('a') + ord('z') - ord(c))
                delta = -1
        
            freq[v] = freq.get(v, 0) + delta
        
        return sum([abs(f) for f in freq.values()])
```
