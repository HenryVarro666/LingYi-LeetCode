---
title: "32. 最长有效括号"
aliases: ["yiduobo的每日leetcode 32.最长有效括号"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "题单/常用数据结构", "题单/动态规划", "题单/LeetCode-热题-100", "题单/常用数据结构/三-栈", "题单/动态规划/七-其他线性-DP", "题单/LeetCode-热题-100/动态规划"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/119448108"
zhihu_id: "119448108"
zhihu_title: "yiduobo的每日leetcode 32.最长有效括号"
question_id: "32"
question: "最长有效括号"
problem_url: "https://leetcode.cn/problems/longest-valid-parentheses/"
difficulty: "Hard"
created: "2020-03-28T22:39:01+08:00"
updated: "2020-03-28T22:39:01+08:00"
upvotes: 0
comments: 0
---

# 32. 最长有效括号

> **[yiduobo的每日leetcode 32.最长有效括号](https://zhuanlan.zhihu.com/p/119448108) · 知乎 · 2020-03-28 · 赞同 0**
> 力扣：[32. 最长有效括号](https://leetcode.cn/problems/longest-valid-parentheses/) · Hard · 灵茶山艾府：[栈 + 配对标记 + O(1) 空间优化（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

32.最长有效括号<https://leetcode-cn.com/problems/longest-valid-parentheses/>

又是括号匹配的题目。经典的做法可以用一个栈维护左括号的下标，然后遇到匹配的右括号时弹出左括号并通过下标计算长度。不过这里用的是一种简单的匹配思路。

首先从头开始扫描，逐个记录左括号数目left与右括号的数目right。

对于新加入一个括号，如果此时

1、right > left，那么说明这个串已经没有维护的价值了，将left与right置0。

2、right \=\= left，那么说明当前串是匹配上的，更新res即可。

3、right \< left，无事发生。因为right \< left说明存在落单的左括号，但是这些落单的括号可能与后续的右括号形成匹配，因此无需改动。

但是上面这个做法有个问题，就是形如 (()()()() 的这种结构，因为最开始的左括号导致后面匹配上的括号都无法更新。

一个自然的想法是如果上面这种情况从右往左看，那么就能找到答案。但是是否可能出现类似的情况呢？答案是不会。

首先如果存在左单括号影响后续匹配，那么从后往前扫能找到答案。

接下来如果存在右单括号影响后续匹配，那么从前往后扫能找到答案。

那么如果同时存在左单括号与右单括号呢？这是不可能的，因为这两个单括号本身就能匹配。

因此只需要正反两次扫描，维护住left与right就行了。需要注意从后往前扫时，单个的right是合法的，但是left > right是不合法的，与从前往后扫正好相反，需要特别注意。

由于只需要两趟扫描，因此最后的时间复杂度为O(n)。

最后附上python代码：

```python
class Solution(object):
    def longestValidParentheses(self, s):
        """
        :type s: str
        :rtype: int
        """

        res = 0
        left = right = 0
        for index in range(len(s)):
            if s[index] == '(':
                left += 1
            else:
                right += 1
            if left == right:
                res = max(res, left + right)
            elif left < right:
                left = right = 0

        left = right = 0
        for index in range(len(s) - 1, -1, -1):
            if s[index] == '(':
                left += 1
            else:
                right += 1
            if left == right:
                res = max(res, left + right)
            elif left > right:
                left = right = 0

        return res
```
