---
title: "3563. 移除相邻字符后字典序最小的字符串"
aliases: ["yiduobo的每日leetcode 3563.移除相邻字符后字典序最小的字符串"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/八-区间-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1910533464102503832"
zhihu_id: "1910533464102503832"
zhihu_title: "yiduobo的每日leetcode 3563.移除相邻字符后字典序最小的字符串"
question_id: "3563"
question: "移除相邻字符后字典序最小的字符串"
problem_url: "https://leetcode.cn/problems/lexicographically-smallest-string-after-adjacent-removals/"
difficulty: "Hard"
rating: 2585
created: "2025-05-29T22:23:00+08:00"
updated: "2025-05-29T22:23:00+08:00"
upvotes: 0
comments: 0
---

# 3563. 移除相邻字符后字典序最小的字符串

> **[yiduobo的每日leetcode 3563.移除相邻字符后字典序最小的字符串](https://zhuanlan.zhihu.com/p/1910533464102503832) · 知乎 · 2025-05-29 · 赞同 0**
> 力扣：[3563. 移除相邻字符后字典序最小的字符串](https://leetcode.cn/problems/lexicographically-smallest-string-after-adjacent-removals/) · Hard · 灵茶山艾府：[字符消消乐：区间 DP + 线性 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3563.移除相邻字符后字典序最小的字符串

[3563. 移除相邻字符后字典序最小的字符串 - 力扣（LeetCode）](https://leetcode.cn/problems/lexicographically-smallest-string-after-adjacent-removals/description/)

题目给出一个由小写字符组成的字符串s，s的长度不超过250。

接下来每一轮操作，都可以从s中任选两个相邻的连续字符，将这两个字符从s中移除，并将剩余的字符左移以填补空隙。

连续字符指的是字母表中相邻的两个字符，不管是正序或者是逆序。另外'a'和'z'也算是连续字符。

问执行任意次移除操作(也可以不执行)可以得到的字典序最小的字符串是什么。

本题中关于连续字符的定义与之前的3561题相同，但是本题中的移除位置是可以任选的，同时通过样例3可以知道，并不是所有移除操作都应该被执行，直观上应该想办法往动态规划上去靠。

为了使得最终的字典序最小，在这里就应该倒序执行动态规划，理由也很简单，越靠前的位置对字典序的影响越大，这一点与基数排序需要从低位到高位执行时一个道理。

令g[index]表示后缀s[index:]执行操作后可以得到的最小字典序字符串，方便期间，在这里置g[n]为空字符串。那么对于g[index]：

1、可以考虑保留s[index]，那么就有g[index] \= s[index] + g[index + 1]。

2、如果需要移除s[index]，则需要考虑移除子串的终点cut_pos，那么就有g[index] \= min(g[index], g[cut_pos + 1]。其中s[index: cut_pos + 1]必须可以通过若干次操作移除掉。

全部计算完成后，g[0]即为最终答案。

接下来的问题就是如果计算s的某个子串是否可以通过操作移除掉，在这里可以考虑使用区间动态规划进行求解。令f[start][end]表示s[start: end + 1]这个子串是否可以被移除掉，那么对于f[start][end]：

1、若start和end相邻：

这种情况下只需要考虑s[start]和s[end]是否连续，可以通过检测这两个字符ascii码之差是否为1或者25来进行检测。若连续，那么f[start][end]为true，否则为false

2、若start和end不相邻：

此时有两种可能。

第一种可能是中间的start + 1到end - 1这一段可以被先行消除，然后s[start]和s[end]配对消除。也就是s[start]和s[end]连续，且f[start + 1][end - 1]为true时，有f[start][end]为true。

第二种可能是将start到end划分为start到cut_pos，以及cut_pos + 1到end这两段，若f[start][cut_pos]以及f[cut_pos + 1][end]都为true，那么就有f[start][end]为ture。

若都不满足，那么f[start][end]为false

在具体实现上，由于需要先计算段的子区间对应的f，因此可以先枚举子区间的长度length，然后枚举起点start，通过start + length - 1计算出对应的end，再计算对应的f[start][end]。

最后附上python代码：

```python
class Solution(object):
    def lexicographicallySmallestString(self, s):
        """
        :type s: str
        :rtype: str
        """
        
        n = len(s)
        f = [[None] * n for _ in range(n)]
        for length in range(2, n + 1, 2):
            for start in range(n):
                end = start + length - 1
                if end >= n:
                    break
                
                diff = abs(ord(s[start]) - ord(s[end]))
                if length == 2:
                    if diff == 1 or diff == 25:
                        f[start][end] = True
                    else:
                        f[start][end] = False
                
                else:
                    f[start][end] = False

                    if (diff == 1 or diff == 25) and f[start + 1][end - 1]:
                        f[start][end] = True
                    else:
                        for cut_pos in range(start + 1, end, 2):
                            if f[start][cut_pos] and f[cut_pos + 1][end]:
                                f[start][end] = True
                                break
                    
        g = [""] * (n + 1)
        for index in range(n - 1, -1, -1):
            g[index] = s[index] + g[index + 1]
            for cut_pos in range(index + 1, n, 2):
                if f[index][cut_pos]:
                    g[index] = min(g[index], g[cut_pos + 1])

        return g[0]
```
