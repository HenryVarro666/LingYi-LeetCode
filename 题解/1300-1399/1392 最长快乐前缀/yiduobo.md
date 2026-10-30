---
title: "1392. 最长快乐前缀"
aliases: ["yiduobo的每日leetcode 1392.最长快乐前缀"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/403985434"
zhihu_id: "403985434"
zhihu_title: "yiduobo的每日leetcode 1392.最长快乐前缀"
question_id: "1392"
question: "最长快乐前缀"
problem_url: "https://leetcode.cn/problems/longest-happy-prefix/"
created: "2021-08-26T23:33:27+08:00"
updated: "2021-08-26T23:33:27+08:00"
upvotes: 1
comments: 0
---

# 1392. 最长快乐前缀

> **[yiduobo的每日leetcode 1392.最长快乐前缀](https://zhuanlan.zhihu.com/p/403985434) · 知乎 · 2021-08-26 · 赞同 1**
> 力扣：[1392. 最长快乐前缀](https://leetcode.cn/problems/longest-happy-prefix/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1392.最长快乐前缀

[力扣](https://leetcode-cn.com/problems/longest-happy-prefix/)

题目要求找出最长的与前缀相同的后缀，回忆一下kmp算法中next数组的定义：

f\[i\]表示的是以第i个字符结尾的字符串中，能与前缀匹配的最长长度，即对于子串s\[:i + 1\]，满足子串s\[:next\[i\]\]等于s\[i - next\[i\] + 1 : i + 1\]

那么next\[-1\]表示的就是字符串s中最长的，且满足与前缀相同的后缀的长度，那么s\[:next\[-1\]\]就是我们要求的答案了。

最后附上python代码：

```python
class Solution(object):
    def longestPrefix(self, s):
        """
        :type s: str
        :rtype: str
        """

        f = [0]
        n = len(s)
        pos = 0
        for index in range(1, n):
            while pos > 0 and s[pos] != s[index]:
                pos = f[pos - 1]
            if s[pos] == s[index]:
                pos += 1
            f.append(pos)
        
        return s[:f[-1]]
```
