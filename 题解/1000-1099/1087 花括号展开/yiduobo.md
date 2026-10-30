---
title: "1087. 花括号展开"
aliases: ["yiduobo的每日leetcode 1087.花括号展开"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/608956727"
zhihu_id: "608956727"
zhihu_title: "yiduobo的每日leetcode 1087.花括号展开"
question_id: "1087"
question: "花括号展开"
problem_url: "https://leetcode.cn/problems/brace-expansion/"
created: "2023-02-23T22:57:48+08:00"
updated: "2023-02-23T22:57:48+08:00"
upvotes: 0
comments: 0
---

# 1087. 花括号展开

> **[yiduobo的每日leetcode 1087.花括号展开](https://zhuanlan.zhihu.com/p/608956727) · 知乎 · 2023-02-23 · 赞同 0**
> 力扣：[1087. 花括号展开](https://leetcode.cn/problems/brace-expansion/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1087.花括号展开

[力扣](https://leetcode.cn/problems/brace-expansion/)

为了能够尝试每一位上各种各样的组合，本题应该使用回溯法来进行处理。

从s的头部开始向后进行处理，若当前处理的位置s[level]为左括号，那么从level + 1开始向后找到第一个右括号的下标p，在level + 1到p - 1直接的字符就是当前这一轮可以使用的字符。将这些字符排序，然后逐个尝试。反过来，若当前处理的s[level]不是括号，那么当前这一轮就只能选择s[level]。

最后附上python代码：

```python
class Solution(object):
    def expand(self, s):
        """
        :type s: str
        :rtype: List[str]
        """

        res = []

        def dfs(level, now):
            if level == len(s):
                res.append(''.join(now))
                return

            if s[level] == '{':
                p = level + 1
                while s[p] != '}':
                    p += 1
                
                char_list = sorted(s[level + 1 : p].split(','))
                for char in char_list:
                    now.append(char)
                    dfs(p + 1, now)
                    now.pop()
            else:
                now.append(s[level])
                dfs(level + 1, now)
                now.pop()

        dfs(0, [])
        return res
```
