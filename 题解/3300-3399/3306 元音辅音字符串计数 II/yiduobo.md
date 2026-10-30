---
title: "3305. 元音辅音字符串计数I & 3306. 元音辅音字符串计数II"
aliases: ["yiduobo的每日leetcode 3305.元音辅音字符串计数I && 3306.元音辅音字符串计数II", "3305. 元音辅音字符串计数I", "3306. 元音辅音字符串计数II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/sliding-window", "leetcode/bit-manipulation", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1091258102"
zhihu_id: "1091258102"
zhihu_title: "yiduobo的每日leetcode 3305.元音辅音字符串计数I && 3306.元音辅音字符串计数II"
question_id: ["3305", "3306"]
question: ["元音辅音字符串计数 I", "元音辅音字符串计数 II"]
problem_url: ["https://leetcode.cn/problems/count-of-substrings-containing-every-vowel-and-k-consonants-i/", "https://leetcode.cn/problems/count-of-substrings-containing-every-vowel-and-k-consonants-ii/"]
difficulty: "Medium"
rating: 2200
created: "2024-10-15T03:28:19+08:00"
updated: "2024-10-15T03:28:19+08:00"
upvotes: 2
comments: 0
---

# 3305. 元音辅音字符串计数I & 3306. 元音辅音字符串计数II

> **[yiduobo的每日leetcode 3305.元音辅音字符串计数I && 3306.元音辅音字符串计数II](https://zhuanlan.zhihu.com/p/1091258102) · 知乎 · 2024-10-15 · 赞同 2**
> 力扣：[3305. 元音辅音字符串计数 I](https://leetcode.cn/problems/count-of-substrings-containing-every-vowel-and-k-consonants-i/) · Medium · 灵茶山艾府：[O(n) 两次滑动窗口（Python/Java/C++/Go）](../3305%20元音辅音字符串计数%20I/灵茶山艾府.md)
> 力扣：[3306. 元音辅音字符串计数 II](https://leetcode.cn/problems/count-of-substrings-containing-every-vowel-and-k-consonants-ii/) · Medium · 灵茶山艾府：[恰好型滑动窗口：转换成两个至少型滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3305.元音辅音字符串计数I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-of-substrings-containing-every-vowel-and-k-consonants-i/)

3306.语音辅音字符串计数II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-of-substrings-containing-every-vowel-and-k-consonants-ii/description/)

题目给出一个字符串word以及一个非负整数k，要求计算word中包含每种元音字母至少一个，且恰好包含k个辅音字母的所有子串的数目。

两题的题设一样，第二题的数据规模较大。

非常标准的滑动窗口问题，但是由于需要同时处理包含元音字母各一个，且恰好包含k个辅音字母，那么在这里就需两个变长的滑动窗口。

从左向右一趟遍历，固定住窗口的左边界，那么：

1、处理元音字母的窗口右边界需要保证窗口内每种元音字母至少都出现了一次，且这个右边界最小。所有大于等于右边界的下标都可以作为当前窗口的合法右边界。不妨设这个最小右边界为v。

2、处理辅音字母的窗口右边界需要保证窗口内的辅音字母数量恰好为k个，且这个右边界最小。所有在当前右边界，到下一个辅音字母之间的下标都可以左右当前窗口的合法右边界。不妨设这个最小右边界为p，下一个辅音字母的下标为q。

那么对于以上的边界，有三种情况：

1、v \< p \< q：

此时所有在p到q - 1之间的下标都是合法的，一共可以形成q - p个子串。

2、p \< v \< q：

此时所有在v到q - 1之间的下标都是合法的，一共可以形成q - v个子串。

3、p \< q \< v：

此时找不到合法的子串

一趟遍历，计算对应的边界并更新答案即可。需要特别注意的是，当某个左边界无法满足元音或者辅音要求时，后续就无需再继续计算了，可以直接退出。另外当k等于0时，若当前左边界为元音字母，那么p就是左边界的下标，否则p不存在，这种情况下不应该更新答案。

最后附上python代码：

```python
class Solution(object):
    def countOfSubstrings(self, word, k):
        """
        :type word: str
        :type k: int
        :rtype: int
        """

        vowel_freq = {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0}
        consonant = 0
        vowel = 0
        n = len(word)

        v = -1 
        p = -1
        q = 0
        res = 0

        for index, char in enumerate(word):
            while v + 1 < n and vowel < 5:
                if word[v + 1] in vowel_freq:
                    vowel_freq[word[v + 1]] += 1
                    if vowel_freq[word[v + 1]] == 1:
                        vowel += 1
                v += 1

            if vowel < 5:
                break
            
            if k == 0:
                if char in vowel_freq:
                    p = index
                else:
                    p = None
            else:
                while p + 1 < n and consonant < k:
                    if word[p + 1] not in vowel_freq:
                        consonant += 1
                    p += 1
                
                if consonant < k:
                    break

            if p is not None:
                if q <= p:
                    q = p + 1
                    while q < n and word[q] in vowel_freq:
                        q += 1
            
                if v < p:
                    res += q - p
                elif v < q:
                    res += q - v

            if char in vowel_freq:
                vowel_freq[char] -= 1
                if vowel_freq[char] == 0:
                    vowel -= 1
            
            elif k > 0:
                consonant -= 1
            

        return res
```
