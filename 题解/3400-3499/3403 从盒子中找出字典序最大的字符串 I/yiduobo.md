---
title: "3403. 从盒子中找出字典序最大的字符串I & 3406. 从盒子中找出字典序最大的字符串II"
aliases: ["yiduobo的每日leetcode 3403.从盒子中找出字典序最大的字符串I && 3406.从盒子中找出字典序最大的字符串II", "3403. 从盒子中找出字典序最大的字符串I", "3406. 从盒子中找出字典序最大的字符串II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/enumeration", "leetcode/suffix-array", "题单/贪心算法", "题单/字符串", "题单/贪心算法/三-字符串贪心", "题单/字符串/五-最小表示法", "leetcode/hard", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/31141752184"
zhihu_id: "31141752184"
zhihu_title: "yiduobo的每日leetcode 3403.从盒子中找出字典序最大的字符串I && 3406.从盒子中找出字典序最大的字符串II"
question_id: ["3403", "3406"]
question: ["从盒子中找出字典序最大的字符串 I", "从盒子中找出字典序最大的字符串 II"]
problem_url: ["https://leetcode.cn/problems/find-the-lexicographically-largest-string-from-the-box-i/", "https://leetcode.cn/problems/find-the-lexicographically-largest-string-from-the-box-ii/"]
difficulty: ["Medium", "Hard"]
rating: 1762
created: "2025-03-18T22:46:17+08:00"
updated: "2025-03-18T22:46:17+08:00"
upvotes: 1
comments: 0
---

# 3403. 从盒子中找出字典序最大的字符串I & 3406. 从盒子中找出字典序最大的字符串II

> **[yiduobo的每日leetcode 3403.从盒子中找出字典序最大的字符串I && 3406.从盒子中找出字典序最大的字符串II](https://zhuanlan.zhihu.com/p/31141752184) · 知乎 · 2025-03-18 · 赞同 1**
> 力扣：[3403. 从盒子中找出字典序最大的字符串 I](https://leetcode.cn/problems/find-the-lexicographically-largest-string-from-the-box-i/) · Medium · 灵茶山艾府：[两种方法：枚举左端点/最大表示法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)
> 力扣：[3406. 从盒子中找出字典序最大的字符串 II](https://leetcode.cn/problems/find-the-lexicographically-largest-string-from-the-box-ii/) · Hard · 灵茶山艾府：[O(n) 最大表示法（Python/Java/C++/Go）](../3406%20从盒子中找出字典序最大的字符串%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3403.从盒子中找出字典序最大的字符串I

[3403. 从盒子中找出字典序最大的字符串 I - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-lexicographically-largest-string-from-the-box-i/description/)

3406.从盒子中找出字典序最大的字符串II

[3406. 从盒子中找出字典序最大的字符串 II - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-lexicographically-largest-string-from-the-box-ii/)

题目给出一个字符串word以及一个整数numFriends，现在要求将word分离成numFriends个非空的子串，问分离出的子串中字典序最大的子串是什么。

两题的题设一样，第二题的数据规模较大，word和numFriends的大小可达2 \* 10^5。

首先考虑特殊情况。当numFriends为1时，答案就是word本身。

接下来考虑一般情况。

题目需要找出字典序最大的子串，那么在不考虑长度限制的前提下，这个子串必然是word的某个后缀。理由也很简单，因为对于某个子串word[left: right]，若right不等于len(word)，那么对于后缀word[left:]，其前right - left个字符与word[left: right]相同，但是其还有word[right:]这个部分，因此其字典序必然大于word[left: right]，也就是说字典序最大的子串必然是word的某个后缀。

对于本题，由于必须将word划分为numFriends个非空的子串，那么最终答案的长度必然小于等于len(word) - numsFriends + 1，也就是说将word划分为numFriends - 1个长度为1的子串，以及1个长度为len(word) - numFriends + 1的子串。

综合以上两点，最终答案就是word中字典序最大的后缀的长度为len(word) - numFriends + 1的前缀，另外如果这个后缀的长度不足len(word) - numFriends + 1，答案就是这个后缀自身。

接下来的问题就是如何找出这个字典序最大的后缀。这个问题就是之前1163题需要计算的内容，直接参考之前的方法就行了。

[yiduobo：yiduobo的每日leetcode 1163.按字典序排在最后的子串](https://zhuanlan.zhihu.com/p/379043216)

最后附上python代码：

```python
class Solution(object):
    def answerString(self, word, numFriends):
        """
        :type word: str
        :type numFriends: int
        :rtype: str
        """
        
        if numFriends == 1:
            return word

        p = 0
        q = 1
        length = 0
        while q + length < len(word):
            if word[p + length] == word[q + length]:
                length += 1
            elif word[p] < word[q + length]:
                p = q + length
                q = p + 1
                length = 0
            elif word[p + length] < word[q + length]:
                p = q
                q += 1
                length = 0
            else:
                q += length + 1
                length = 0

        return word[p: p + len(word) - numFriends + 1]
```
