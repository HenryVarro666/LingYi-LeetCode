---
title: "4021. 得到旋转回文字符串的最少操作次数I"
aliases: ["yiduobo的每日leetcode 4021.得到旋转回文字符串的最少操作次数I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/enumeration", "leetcode/numpy", "leetcode/fast-fourier-transform", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2072837887305978384"
zhihu_id: "2072837887305978384"
zhihu_title: "yiduobo的每日leetcode 4021.得到旋转回文字符串的最少操作次数I"
question_id: "4021"
question: "得到旋转回文字符串的最少操作次数 I"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-a-rotated-palindrome-i/"
difficulty: "Medium"
created: "2026-08-18T00:17:02+08:00"
updated: "2026-08-18T00:17:02+08:00"
upvotes: 1
comments: 4
---

# 4021. 得到旋转回文字符串的最少操作次数I

> **[yiduobo的每日leetcode 4021.得到旋转回文字符串的最少操作次数I](https://zhuanlan.zhihu.com/p/2072837887305978384) · 知乎 · 2026-08-18 · 赞同 1**
> 力扣：[4021. 得到旋转回文字符串的最少操作次数 I](https://leetcode.cn/problems/minimum-operations-to-make-a-rotated-palindrome-i/) · Medium · 灵茶山艾府：[两种方法：暴力枚举 / 卷积（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4021.得到旋转回文字符串的最少操作次数I

<https://leetcode.cn/problems/minimum-operations-to-make-a-rotated-palindrome-i/description/>

题目给出一个由小写英文字符组成的字符串s，其长度不超过2000。

现在可以按照任意顺序执行以下操作任意次，包括零次：

- 递增：选择一个下标index，并将s[index]替换为下一个小写字符。'z'之后的字符是'a'。
- 左旋：将字符串的第一个字符移动到末尾。

问使得s成为回文串所需的最少操作次数。

由于题目中s的长度不大，因此在这里可以直接枚举左旋的字符数量，然后拼接得到新的字符串t。

接下来对于当前的t，使用两个指针left和right从两端向中间同时移动。对于当前指向的两个字符，必须将二者变为一致。这两个字符在字母表中的距离为dis \= abs(ord(t[left]) - ord(t[right]))，那么如果将ascii码较小的变为较大的，所需的操作次数就是dis，反之就是26 - dis，在这里取较小的那个累加到总代价中即可。

需要注意在这里计算完总代价后，还需要额外加上移位的代价，然后才能更新答案。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        def calc(t):
            left, right = 0, len(t) - 1
            cost = 0
            while left < right:
                dis = abs(ord(t[left]) - ord(t[right]))
                cost += min(dis, 26 - dis)
                left += 1
                right -= 1
            
            return cost
        
        res = 26 * len(s)
        for index in range(len(s)):
            res = min(res, index + calc(s[index:] + s[:index]))
        return res
```
