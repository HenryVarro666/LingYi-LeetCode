---
title: "3571. 最短超级串II"
aliases: ["yiduobo的每日leetcode 3571.最短超级串II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string-matching", "题单/字符串", "题单/字符串/一-KMP-前缀的后缀"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1936555344269678329"
zhihu_id: "1936555344269678329"
zhihu_title: "yiduobo的每日leetcode 3571.最短超级串II"
question_id: "3571"
question: "最短超级串 II"
problem_url: "https://leetcode.cn/problems/find-the-shortest-superstring-ii/"
difficulty: "Easy"
rating: 2800
created: "2025-08-06T22:43:03+08:00"
updated: "2025-08-06T22:43:03+08:00"
upvotes: 2
comments: 0
---

# 3571. 最短超级串II

> **[yiduobo的每日leetcode 3571.最短超级串II](https://zhuanlan.zhihu.com/p/1936555344269678329) · 知乎 · 2025-08-06 · 赞同 2**
> 力扣：[3571. 最短超级串 II](https://leetcode.cn/problems/find-the-shortest-superstring-ii/) · Easy · 灵茶山艾府：[O(n+m) KMP](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3571.最短超级串II

[3571. 最短超级串 II - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-shortest-superstring-ii/description/)

题目给出两个字符串s1和s2，长度都不超过100。要求找出同时包含s1和s2作为子串的最短字符串，如果存在多个，任意返回一个。

首先考虑特殊情况。

当s1完全包含了s2，那么答案显然就是s1；反之，若s2完全包含了s1，那么答案就是s2。

接下来考虑一般情况。

对于答案字符串s，要么s1在前s2在后，要么s2在前s1在后。为了使得s最短，其中就不应该包含任何没有作用的字符，也就是说要么满足s1是s的前缀，s2是s的后缀，要么满足s1是s的后缀，s2是s的前缀。

对于这两种情况，若前缀和后缀存在重叠，s的长度就可以缩短。例如样例一中的aba和bab，aba的后缀ba与bab的前缀ba重叠，那么将aba作为s的前缀，bab作为s的后缀，去掉重叠的部分，就可以构造出答案abab。

更进一步的，对于前面这种情况，s1的后缀与s2的前缀重叠的部分越多，s就越短；而对于后面这种情况，s1的前缀与s2的后缀重叠的部分越多，s就越短。由于本题的数据规模较小，因此可以直接一趟遍历，检测上面描述的s1和s2的重叠情况，选择重叠长度较大的那么方法构造答案字符串s即可。

最后附上python代码：

```python
class Solution(object):
    def shortestSuperstring(self, s1, s2):
        """
        :type s1: str
        :type s2: str
        :rtype: str
        """
        
        if s1.find(s2) != -1:
            return s1
        if s2.find(s1) != -1:
            return s2

        n = len(s1)
        m = len(s2)
        for length in range(min(n, m) - 1, 0, -1):
            if s1[n - length:] == s2[:length]:
                return s1 + s2[length:]
            if s2[m - length:] == s1[:length]:
                return s2 + s1[length:]
        
        return s1 + s2
```
