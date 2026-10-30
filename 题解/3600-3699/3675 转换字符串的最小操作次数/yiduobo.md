---
title: "3675. 转换字符串的最小操作次数"
aliases: ["yiduobo的每日leetcode 3675.转换字符串的最小操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1952807320691114438"
zhihu_id: "1952807320691114438"
zhihu_title: "yiduobo的每日leetcode 3675.转换字符串的最小操作次数"
question_id: "3675"
question: "转换字符串的最小操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-transform-string/"
difficulty: "Medium"
rating: 1414
created: "2025-09-21T20:14:09+08:00"
updated: "2025-09-21T20:14:10+08:00"
upvotes: 2
comments: 0
---

# 3675. 转换字符串的最小操作次数

> **[yiduobo的每日leetcode 3675.转换字符串的最小操作次数](https://zhuanlan.zhihu.com/p/1952807320691114438) · 知乎 · 2025-09-21 · 赞同 2**
> 力扣：[3675. 转换字符串的最小操作次数](https://leetcode.cn/problems/minimum-operations-to-transform-string/) · Medium · 灵茶山艾府：[阅读理解题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3675.转换字符串的最小操作次数

[3675. 转换字符串的最小操作次数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-transform-string/description/)

题目给出一个仅由小写英文字母组成的字符串s，接下来可以执行以下操作任意次（包括零次）。每次操作中，都可以选择一个字符c，并将字符串中所有的c都替换为英文字母表中的下一个小写字母，问将s转换为全'a'所需的最小操作次数。

题目中的字母表式循环的，也就是说'z'的下一个字母是'a'。

由于最终的目标是将字符串中的所有字符都变为'a'，因此在这里就应该按照'b' -> 'c' -> 'd' -> ... -> 'z' -> 'a'的顺序进行转换。当然，若这个转换路径中的某些前缀字符不存在，那么就可以跳过这些字符，也就是说，在这里只需要找出字符串中不为'a'的最小字符mi，然后逐步将mi转换为'z'再转换为'a'即可。

若不存在这样的mi，也就是说字符串一开始就是全'a'，那么最终答案就为0，反之答案就是将mi转换为'z'的次数，也就是ord('z') - ord(mi)，再加上1。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        mi = None
        for c in s:
            if c != 'a' and (mi is None or mi > c):
                mi = c
        
        if mi is None:
            return 0
        return 123 - ord(mi)
```
