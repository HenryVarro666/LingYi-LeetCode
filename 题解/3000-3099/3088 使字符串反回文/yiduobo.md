---
title: "3088. 使字符串反回文"
aliases: ["yiduobo的每日leetcode 3088.使字符串反回文"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/698860616"
zhihu_id: "698860616"
zhihu_title: "yiduobo的每日leetcode 3088.使字符串反回文"
question_id: "3088"
question: "使字符串反回文"
problem_url: "https://leetcode.cn/problems/make-string-anti-palindrome/"
created: "2024-05-20T21:56:48+08:00"
updated: "2024-05-20T21:56:48+08:00"
upvotes: 1
comments: 0
---

# 3088. 使字符串反回文

> **[yiduobo的每日leetcode 3088.使字符串反回文](https://zhuanlan.zhihu.com/p/698860616) · 知乎 · 2024-05-20 · 赞同 1**
> 力扣：[3088. 使字符串反回文](https://leetcode.cn/problems/make-string-anti-palindrome/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3088.使字符串反回文

[. - 力扣（LeetCode）](https://leetcode.cn/problems/make-string-anti-palindrome/description/)

题目中所说的反回文指的是字符串中对称位置上的字符不能相同。给出一个字符串，要求将字符串中的字符重新排列，得到字典序最小的反回文串。

首先，根据鸽笼原理，若字符串中某种字符的数量超过了字符串长度的一半，那么必然存在一组对称位置上的字符都是该字符，也就是说这种情况下是无法构造的，直接返回-1。而对于其他情况，则一定可以形成反回文串。

由于题目要求答案的字典序最小，那么一个自然的想法就是先将字符串按字符ascii进行排序，得到的字符串必然是字典序最小的，但是此时可能出现正中间处于对称位置上的字符是相同的。由于字符串是排序好的，因此相等的字符只可能是唯一的一种。为了使得字典序最小，那么在这里就应该想办法调换这些相等的字符中后半部分的字符，保留前半部分的字符不动，这样才能使得字典序最小。

在这里可以先证明调换使用的字符都来自于字符串的后半部分。方便起见，令mid \= n / 2，接下来设中间相等字符char的起点为left + 1，终点为right - 1，也就是说前半部分的char区间是[left + 1, mid - 1]，长度left_length为mid - 1 - left，后半部分的char区间则是[mid, right - 1]，长度right_length为right - mid。

当left_length > right_length时，只需要将后半部分的char区间替换成其他字符，同时将这right_length个char移动到mid + left_length之外去就行了。后半部分的其他字符数量mid - right_length是大于right_length的，因为right_length + left_length是char出现的总次数，必然是小于n的一半，也就是mid的，也就是说

mid > left_length + right_length > right_length + right_length

即

mid - right_length > right_lenght

反过来，当left_length \<\= right_length时，此时需要调换只是[mid, mid + left_length - 1]区间内一共left_length个字符，而不是整个后半部分的right_length个字符，而mid - right_length > left_length

证明了可以使用从right开始的其他字符替换从mid开始的char之后，最后需要考虑具体的交换方案。

当left_length > right_length时，[mid, mid + left_length - 1]这个区间内是不能再出现char的，因此需要将从right开始的left_length个字符填充到这个区间中，然后将中间的char填充到mid + left_length开始的right_length个位置上。

反过来，当left_length \<\= right_length是，此时同样是将[mid, mid + left_length - 1]这个区间内的字符用从right开始的left_length个字符填充，而这些char则需要填充到从right开始left_length个位置上。

观察后面这种情况对于char的填充可以发现，由于[mid + left_length, right - 1]这一段也还是char，因此在这里将char填充到right开始的left_length个位置上，也可以视为将char填充到从mid + length开始的right_length个位置上。

换言之，两种情况的交换方案可以视为统一的方案，即先将right开始的left_length个字符填充到[mid, mid + left_length - 1]，然后用char填充[mid + length, mid + left_length + right_length]。

到了这里，就得到了完整的算法。先将字符串按ascii码从小到大进行排序，然后从mid和mid + 1开始，分别向左右两侧找到第一个不等于中间字符char的位置left和right，再根据上面的交换方案执行交换即可。

最后附上python代码：

```python
class Solution(object):
    def makeAntiPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """

        m = len(s) // 2

        max_freq = max(Counter(s).values())
        if max_freq > m:
            return "-1"
        
        base = sorted(s)
        left = m - 1
        right = m
        while base[left] == base[m]:
            left -= 1
        while base[right] == base[m - 1]:
            right += 1
        
        left_length = m - 1 - left
        right_length = right - m

        tmp = base[m]
        for index in range(left_length):
            base[m + index] = base[right + index]
        for index in range(right_length):
            base[m + left_length + index] = tmp
            
        return ''.join(base)
```
