---
title: "727. 最小窗口子序列"
aliases: ["yiduobo的每日leetcode 727.最小窗口子序列"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/string", "leetcode/zi-dong-ji", "leetcode/zi-xu-lie", "题单/字符串", "题单/字符串/九-子序列自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/605004530"
zhihu_id: "605004530"
zhihu_title: "yiduobo的每日leetcode 727.最小窗口子序列"
question_id: "727"
question: "最小窗口子序列"
problem_url: "https://leetcode.cn/problems/minimum-window-subsequence/"
difficulty: "Hard"
created: "2023-02-10T01:27:59+08:00"
updated: "2023-02-10T01:27:59+08:00"
upvotes: 0
comments: 0
---

# 727. 最小窗口子序列

> **[yiduobo的每日leetcode 727.最小窗口子序列](https://zhuanlan.zhihu.com/p/605004530) · 知乎 · 2023-02-10 · 赞同 0**
> 力扣：[727. 最小窗口子序列](https://leetcode.cn/problems/minimum-window-subsequence/) · Hard · 灵茶山艾府：[子序列自动机](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

727.最小窗口子序列

[力扣](https://leetcode.cn/problems/minimum-window-subsequence/)

设s1的长度为n，s2的长度为m，那么在确定了s1中子串的起点start后，就可以通过贪心算法在O(n + m)的时间复杂度内找出包含s2的最短子串，其中最短的那个就是答案。这个算法的时间复杂度为O(n \* (n + m))，需要进行优化。

注意到题目中字符串只包含小写字符，那么如果将每个位置右侧各种字符的下一次出现位置提前预处理出来，那么在执行贪心算法时就不需要在s1中枚举，而是改成通过下一个位置进行m次跳跃就行了。这样一来，就可以在O(m)的时间内找出包含s2的最短子串了，总的时间复杂度就优化到了O(mn)。优化后的算法为：

1、首先从后向前遍历s1，预处理出next数组，其中next[index]记录了s1在index这个位置右侧每种字符首次出现的下标

2、接下来从前向后s1，通过贪心算法找出以当前位置为起始位置的包含子序列s2的最短子串，并更新答案

最后附上python代码：

```python
class Solution(object):
    def minWindow(self, s1, s2):
        """
        :type s1: str
        :type s2: str
        :rtype: str
        """

        n = len(s1)
        m = len(s2)

        next = [{}]
        for index in range(n - 1, 0, -1):
            next.append(next[-1].copy())
            next[-1][s1[index]] = index
        
        next.reverse()
        
        mi = None
        mi_start = None

        for index in range(n):
            if s1[index] != s2[0]:
                continue

            p = 1
            now = index
            while p < m:
                if s2[p] in next[now]:
                    now = next[now][s2[p]]
                    p += 1
                else:
                    break
            
            if p == m and (mi is None or mi > now - index + 1):
                mi = now - index + 1
                mi_start = index
        
        if mi is None:
            return ""
        
        return s1[mi_start : mi_start + mi]
```
