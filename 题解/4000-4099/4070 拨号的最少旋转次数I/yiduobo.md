---
title: "4070. 拨号的最少旋转次数I & 4071. 拨号的最少旋转次数II"
aliases: ["yiduobo的每日leetcode 4070.拨号的最少旋转次数I && 4071.拨号的最少旋转次数II", "4070. 拨号的最少旋转次数I", "4071. 拨号的最少旋转次数II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2090606813800670943"
zhihu_id: "2090606813800670943"
zhihu_title: "yiduobo的每日leetcode 4070.拨号的最少旋转次数I && 4071.拨号的最少旋转次数II"
question_id: ["4070", "4071"]
question: ["拨号的最少旋转次数I", "拨号的最少旋转次数II"]
problem_url: ["https://leetcode.cn/problems/minimum-rotations-to-dial-a-number-i/", "https://leetcode.cn/problems/minimum-rotations-to-dial-a-number-ii/"]
created: "2026-10-06T01:24:02+08:00"
updated: "2026-10-06T01:24:06+08:00"
upvotes: 0
comments: 0
---

# 4070. 拨号的最少旋转次数I & 4071. 拨号的最少旋转次数II

> **[yiduobo的每日leetcode 4070.拨号的最少旋转次数I && 4071.拨号的最少旋转次数II](https://zhuanlan.zhihu.com/p/2090606813800670943) · 知乎 · 2026-10-06 · 赞同 0**
> 力扣：[4070. 拨号的最少旋转次数I](https://leetcode.cn/problems/minimum-rotations-to-dial-a-number-i/)
> 力扣：[4071. 拨号的最少旋转次数II](https://leetcode.cn/problems/minimum-rotations-to-dial-a-number-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4070.拨号的最少旋转次数I

<https://leetcode.cn/problems/minimum-rotations-to-dial-a-number-i/description/>

4071.拨号的最少旋转次数II

<https://leetcode.cn/problems/minimum-rotations-to-dial-a-number-ii/description/>

题目给出一个拨号盘，其中的数字从0到9按顺序排列，同时这个拨号盘是环形的，因此0号9相邻。拨号盘上的指针最初指向0。

接下来给出一个由数字组成的字符串s，表示需要拨的号码。

现在要求按顺序拨s中的每个数字，即旋转拨号盘上的指针，直到指向目标数字。每次旋转只能将指针移动到一个相邻的数字，同时可以向任意一个方向旋转。若指针已经指向了目标数字，则无需旋转。

4070题问的是最少需要旋转多少次才能完成拨号。

4071题则可以在拨号前执行以下操作至多一次：选择s中任意后缀并进行反转。问此时最少需要旋转的次数。

首先来考虑4070题。4070题处理起来相对简单，就是一趟遍历，计算拨号盘上指针移动所需的最少次数之和就行了。对于从pre移动到c的一次移动，记diff \= abs(c - pre)，那么这次移动的最少移动次数就是min(10 - diff, diff)，即按照顺时针或者逆时针过去所需移动次数的较小值。一趟遍历，计算这个值并累加即可。

接下来考虑4071题。本题可以反转s中的任意后缀，不妨设反转的是s[k:]，那么：

在反转之前，需要计算的就是从s[k - 1]或者0到s[k]所需的移动次数(当k \= 0时，不存在s[k - 1]，取的是指针初始指向的0)，以及从s[k]到s[k + 1]、s[k + 1]到s[k + 2]、...、s[n - 2]到s[n - 1]的所需移动次数之和。

在反转之后，需要计算的就是从s[k - 1]或者0到s[n - 1]，然后从s[n - 1]到s[n - 2]、...、s[k + 1]到s[k]所需的移动次数之和。

由于对于一组(a, b)，从a到b所需的旋转次数与从b到a所需的旋转次数是相同的，因此对于上面反转与不反转这两种情况，唯一的差别仅在于从s[k - 1]或者0到达的是s[k]还是s[n - 1]，因此在这里需要计算这两次行动所需旋转次数的差值，就是反转后可以节省的步数。取其中最小且小于0的那一种，累加到之前正常翻转所需的操作数上即为最终答案。

最后附上python代码：

4070题：

```python
class Solution(object):
    def minRotations(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        pre = 0
        res = 0
        for c in s:
            c = int(c)
            diff = abs(pre - c)
            res += min(diff, 10 - diff)
            pre = c
        
        return res
```

4071题:

```python
class Solution(object):
    def minRotations(self, n, s):
        """
        :type n: int
        :type s: str
        :rtype: int
        """
        
        pre = 0
        res = 0
        delta = 0
        last = int(s[-1])

        for c in s:
            c = int(c)
            diff = abs(c - pre)
            dis = min(diff, 10 - diff)
            res += dis

            diff_last = abs(last - pre)
            dis_last = min(diff_last, 10 - diff_last)
            if delta > dis_last - dis:
                delta = dis_last - dis
            
            pre = c
        
        return res + delta
```
