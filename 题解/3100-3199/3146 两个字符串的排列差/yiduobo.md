---
title: "3146. 两个字符串的排列差"
aliases: ["yiduobo的每日leetcode 3146.两个字符串的排列差"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/hash-table", "leetcode/string", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/703495668"
zhihu_id: "703495668"
zhihu_title: "yiduobo的每日leetcode 3146.两个字符串的排列差"
question_id: "3146"
question: "两个字符串的排列差"
problem_url: "https://leetcode.cn/problems/permutation-difference-between-two-strings/"
difficulty: "Easy"
created: "2024-06-15T03:03:56+08:00"
updated: "2024-06-15T03:03:56+08:00"
upvotes: 0
comments: 0
---

# 3146. 两个字符串的排列差

> **[yiduobo的每日leetcode 3146.两个字符串的排列差](https://zhuanlan.zhihu.com/p/703495668) · 知乎 · 2024-06-15 · 赞同 0**
> 力扣：[3146. 两个字符串的排列差](https://leetcode.cn/problems/permutation-difference-between-two-strings/) · Easy · 灵茶山艾府：[简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3146.两个字符串的排列差

[. - 力扣（LeetCode）](https://leetcode.cn/problems/permutation-difference-between-two-strings/description/)

题目给出两个字符串s和t，单个字符串中包含的字符都各不相同，且t是s的一个排列。现在需要计算s和t中每个字符在两个字符串中下标之差的绝对值之和。

先对s进行一趟遍历，使用哈希表记录其中每个字符出现的下标，接下来再对t进行一趟遍历，计算当前字符在哈希表中对应的值与当前下标之差的绝对值，累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def findPermutationDifference(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: int
        """

        pos = {}
        for index, char in enumerate(s):
            pos[char] = index
        
        res = 0
        for index, char in enumerate(t):
            res += abs(index - pos[char])
        return res
```
