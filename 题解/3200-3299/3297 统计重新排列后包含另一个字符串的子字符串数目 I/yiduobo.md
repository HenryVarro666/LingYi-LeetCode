---
title: "3297. 统计重新排列后包含另一个字符串的子字符串数目I & 3298. 统计重新排列后包含另一个字符串的子字符串数目II"
aliases: ["yiduobo的每日leetcode 3297.统计重新排列后包含另一个字符串的子字符串数目I && 3298.统计重新排列后包含另一个字符串的子字符串数目II", "3297. 统计重新排列后包含另一个字符串的子字符串数目I", "3298. 统计重新排列后包含另一个字符串的子字符串数目II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sliding-window", "leetcode/hard", "leetcode/array", "leetcode/string", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/942253222"
zhihu_id: "942253222"
zhihu_title: "yiduobo的每日leetcode 3297.统计重新排列后包含另一个字符串的子字符串数目I && 3298.统计重新排列后包含另一个字符串的子字符串数目II"
question_id: ["3297", "3298"]
question: ["统计重新排列后包含另一个字符串的子字符串数目 I", "统计重新排列后包含另一个字符串的子字符串数目 II"]
problem_url: ["https://leetcode.cn/problems/count-substrings-that-can-be-rearranged-to-contain-a-string-i/", "https://leetcode.cn/problems/count-substrings-that-can-be-rearranged-to-contain-a-string-ii/"]
difficulty: ["Medium", "Hard"]
rating: 1909
created: "2024-10-12T02:39:14+08:00"
updated: "2024-10-12T02:39:14+08:00"
upvotes: 1
comments: 0
---

# 3297. 统计重新排列后包含另一个字符串的子字符串数目I & 3298. 统计重新排列后包含另一个字符串的子字符串数目II

> **[yiduobo的每日leetcode 3297.统计重新排列后包含另一个字符串的子字符串数目I && 3298.统计重新排列后包含另一个字符串的子字符串数目II](https://zhuanlan.zhihu.com/p/942253222) · 知乎 · 2024-10-12 · 赞同 1**
> 力扣：[3297. 统计重新排列后包含另一个字符串的子字符串数目 I](https://leetcode.cn/problems/count-substrings-that-can-be-rearranged-to-contain-a-string-i/) · Medium · 灵茶山艾府：[O(n) 线性做法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)
> 力扣：[3298. 统计重新排列后包含另一个字符串的子字符串数目 II](https://leetcode.cn/problems/count-substrings-that-can-be-rearranged-to-contain-a-string-ii/) · Hard · 灵茶山艾府：[O(n) 滑动窗口求个数（Python/Java/C++/C/Go/JS/Rust）](../3298%20统计重新排列后包含另一个字符串的子字符串数目%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3297.统计重新排列后包含另一个字符串的子字符串数目I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-substrings-that-can-be-rearranged-to-contain-a-string-i/description/)

3298.统计重新排列后包含另一个字符串的子字符串数目II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-substrings-that-can-be-rearranged-to-contain-a-string-ii/)

题目给出两个字符串word1和word2，对于word1中的某个子串x，如果将x重新排列后可以形成以word2为前缀的字符串，那么就称x为合法的字符。问word1中有多少个合法的子串。

两题的题设一样，第二题的数据规模较大，题目要求给出一个线性复杂度的算法。

注意到子串可以重新排列，那么对于word2中出现的所有字符，只要子串中同样的字符数量充足，那么子串就是合法的。更具体的，令哈希表freq1表示子串中每种字符出现的次数，哈希表freq2表示word2中每种字符出现的次数，那么对于freq2中的任意字符串x，若freq1[x] >\= freq2[x]，那么子串就是合法的。

这是一个非常标准的变长滑动窗口的问题。对于每个子串左边界index，可以找出最小的右边界p，满足word1[index : p]是合法的，那么对于所有左边界位于index，右边界位于p - 1到len(word1) - 1之间的子串都是合法的，一共有len(word1) - p + 1个合法的子串。

而对于合法性的判断，则可以通过上面描述的，一开始先计算好哈希表freq2，然后使用哈希表freq1来统计当前窗口内每种字符的数量。为了避免每次都需要对比整个哈希表，可以使用一个变量cnt表示目前freq1中已经达标的字符数量。对于某个字符char，若freq1[char]的数量从freq2[char] - 1变成freq2[char]，说明在这一时刻char这个字符的数量达标了，此时应该将cnt加上1，反之若freq1[char]的数量从freq2[char]变为freq2[char] - 1，那么说明char在这一刻由达标变成了不达标，此时则应该将cnt减去1。有了cnt后，就可以通过cnt与freq2的大小关系来判断当前窗口内的子串是否合法了。

其他的操作过程则直接按照常规滑动窗口的处理方法，每一轮先向后移动p，找出合法的最小右边界，更新答案后再移动窗口左边界并重复此过程直到找不到合法右边界为止。

最后附上python代码：

```python
class Solution(object):
    def validSubstringCount(self, word1, word2):
        """
        :type word1: str
        :type word2: str
        :rtype: int
        """

        freq2 = {}
        for char in word2:
            freq2[char] = freq2.get(char, 0) + 1
        
        cnt = 0
        freq1 = {}
        p = 0
        res = 0
        for char in word1:
            while p < len(word1) and cnt < len(freq2):
                freq1[word1[p]] = freq1.get(word1[p], 0) + 1
                if freq1[word1[p]] == freq2.get(word1[p], 0):
                    cnt += 1
                p += 1
            
            if cnt < len(freq2):
                break
            
            res += len(word1) - p + 1

            freq1[char] -= 1
            if freq1[char] == freq2.get(char, 0) - 1:
                cnt -= 1
        
        return res
```
