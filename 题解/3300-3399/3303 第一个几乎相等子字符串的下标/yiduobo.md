---
title: "3303. 第一个几乎相等子字符串的下标"
aliases: ["yiduobo的每日leetcode 3303.第一个几乎相等子字符串的下标"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/string", "leetcode/string-matching", "题单/动态规划", "题单/字符串", "题单/动态规划/专题-前后缀分解", "题单/字符串/二-Z-函数-后缀的前缀"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1002773941"
zhihu_id: "1002773941"
zhihu_title: "yiduobo的每日leetcode 3303.第一个几乎相等子字符串的下标"
question_id: "3303"
question: "第一个几乎相等子字符串的下标"
problem_url: "https://leetcode.cn/problems/find-the-occurrence-of-first-almost-equal-substring/"
difficulty: "Hard"
rating: 2509
created: "2024-10-14T03:58:30+08:00"
updated: "2024-10-14T03:58:30+08:00"
upvotes: 0
comments: 0
---

# 3303. 第一个几乎相等子字符串的下标

> **[yiduobo的每日leetcode 3303.第一个几乎相等子字符串的下标](https://zhuanlan.zhihu.com/p/1002773941) · 知乎 · 2024-10-14 · 赞同 0**
> 力扣：[3303. 第一个几乎相等子字符串的下标](https://leetcode.cn/problems/find-the-occurrence-of-first-almost-equal-substring/) · Hard · 灵茶山艾府：[前后缀分解 + Z 数组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3303.第一个几乎相等子字符串的下标

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-occurrence-of-first-almost-equal-substring/description/)

题目给出两个字符串s和pattern，要求从s中找出一个最靠前的子串，这个子串与pattern几乎相等。

几乎相等的定义为，如果一个字符串x修改至多一个字符可以变成y，那么就称x与y几乎相等。

本题与上一题很相似，不同的是本题需要找的是最靠前的子串而不是子序列，处理方法也有所区别。

首先考虑特殊情况。当pattern的长度为1时，直接将s的首字符替换成pattern[0]就行了，对应的答案为0。

接下来考虑一般情况。

由于是子串，那么在确定了起点index后，整个子串也随之确定，即s[index : index + len(pattern)]，方便起见，将这个子串记为t。对于这个子串t，若需要从中选取某个下标p进行替换，这个p需要满足：

1、t的前缀t[:p]是pattern的前缀

2、t的后缀t[p + 1:]是pattern的后缀

在这里逐个枚举index得到t，再从中枚举p的话效率就很低了，不妨考虑什么情况下必然存在可用的p。

为了尽量发挥前缀匹配的长度，在这里就应该将p设置在t的前缀与pattern前缀的最大匹配长度加1的位置，接下来如果t剩余字符形成的后缀能与pattern的后缀匹配，也就是剩余字符的数量小于等于t的后缀与pattern后缀的最大匹配长度，那么就说明p可用。

也就是说，如果t的前缀与pattern前缀的最大匹配长度，加上t的后缀与pattern的后缀的最大匹配长度，再加上1之后大于等于pattern的长度的话，就说明t中必然可以找到合法的p，而此时t起点对应的index即为最终答案。

对于s中每个位置开始的前缀能与pattern的前缀的最长匹配长度这个问题，可以将pattern接在s的前面，然后使用扩展kmp算法来处理。关于扩展kmp算法的描述可以参考之前的3029题：

[yiduobo：yiduobo的每日leetcode 3029.将单词恢复初始状态所需的最短时间I && 3031.将单词恢复初始状态所需的最短时间II](https://zhuanlan.zhihu.com/p/695360382)

另一方面，对于后缀则只需将翻转后的pattern接在翻转后的s前面，然后再翻转拼接后的字符串，就同样可以使用扩展kmp算法来处理了。

分别记left[index]和right[index]上面得到的计算结果，那么对于子串s[index : index + len(pattern)]而言，其前缀匹配的最大长度即为left[index]，而后缀匹配的最大长度则需要从终点出发，即right[index + len(pattern) - 1]。若这二者之和再加上1大于等于pattern的长度，那么s[index : index + len(pattern)]就与pattern几乎相等。一趟遍历，找出首个满足条件的index即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minStartingIndex(self, s, pattern):
        """
        :type s: str
        :type pattern: str
        :rtype: int
        """

        if len(pattern) == 1:
            return 0

        def get_match(t):
            z = [0]
            left, right = 0, 0
            for index in range(1, len(t)):
                if index <= right and z[index - left] < right - index + 1:
                    z.append(z[index - left])
                else:
                    z.append(max(0, right - index + 1))
                    while z[-1] + index < len(t) and t[z[-1] + index] == t[z[-1]]:
                        z[-1] += 1
                    
                    if index + z[-1] - 1 > right:
                        left, right = index, index + z[-1] - 1

            return z[len(pattern):]

        left = get_match(pattern + s)
        right = get_match(pattern[::-1] + s[::-1])[::-1]
        
        for index in range(len(s) - len(pattern) + 1):
            if left[index] + right[index + len(pattern) - 1] + 1 >= len(pattern):
                return index
                
        return -1
```
