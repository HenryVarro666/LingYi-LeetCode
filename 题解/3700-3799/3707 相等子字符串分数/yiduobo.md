---
title: "3707. 相等子字符串分数"
aliases: ["yiduobo的每日leetcode 3707.相等子字符串分数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li", "题单/动态规划", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1960747728930857768"
zhihu_id: "1960747728930857768"
zhihu_title: "yiduobo的每日leetcode 3707.相等子字符串分数"
question_id: "3707"
question: "相等子字符串分数"
problem_url: "https://leetcode.cn/problems/equal-score-substrings/"
difficulty: "Easy"
rating: 1262
created: "2025-10-12T16:56:22+08:00"
updated: "2025-10-12T16:56:22+08:00"
upvotes: 0
comments: 0
---

# 3707. 相等子字符串分数

> **[yiduobo的每日leetcode 3707.相等子字符串分数](https://zhuanlan.zhihu.com/p/1960747728930857768) · 知乎 · 2025-10-12 · 赞同 0**
> 力扣：[3707. 相等子字符串分数](https://leetcode.cn/problems/equal-score-substrings/) · Easy · 灵茶山艾府：[两次遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3707.相等子字符串分数

[3707. 相等子字符串分数 - 力扣（LeetCode）](https://leetcode.cn/problems/equal-score-substrings/description/)

题目给出一个由小写英文字母组成的字符串s。一个字符串的得分定义为其所有字符在字母表中的位置之和，其中'a' \= 1，'b' \= 2，...，'z' \= 26。

要求判断能否将s切分为两个非空子串，这两个子串的得分相同。

首先，可以按题目描述计算出每个字符的得分，那么题目实际上就是给出一个数组，问是否存在某个前缀，其和恰好等于数组总和的一半。

对于这个问题，只需先一趟遍历，计算数组总和，再进行一趟遍历，计算前缀和，并判断是否存在恰好等于总和一半的前缀和即可。

最后附上python代码：

```python
class Solution(object):
    def scoreBalance(self, s):
        """
        :type s: str
        :rtype: bool
        """
        
        total = 0
        for c in s:
            total += ord(c) - 96
        
        now = 0
        for c in s:
            now += ord(c) - 96
            if now + now == total:
                return True
        
        return False
```
