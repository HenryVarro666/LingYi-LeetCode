---
title: "1745. 回文串分割IV"
aliases: ["yiduobo的每日leetcode 1745.回文串分割IV"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "题单/动态规划", "题单/字符串", "题单/动态规划/五-划分型-DP", "题单/字符串/三-Manacher-算法-回文串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/454628517"
zhihu_id: "454628517"
zhihu_title: "yiduobo的每日leetcode 1745.回文串分割IV"
question_id: "1745"
question: "分割回文串 IV"
problem_url: "https://leetcode.cn/problems/palindrome-partitioning-iv/"
difficulty: "Hard"
created: "2022-01-07T23:49:27+08:00"
updated: "2022-01-07T23:49:27+08:00"
upvotes: 1
comments: 0
---

# 1745. 回文串分割IV

> **[yiduobo的每日leetcode 1745.回文串分割IV](https://zhuanlan.zhihu.com/p/454628517) · 知乎 · 2022-01-07 · 赞同 1**
> 力扣：[1745. 分割回文串 IV](https://leetcode.cn/problems/palindrome-partitioning-iv/) · Hard · 灵茶山艾府：[直接调用 1278 题代码（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1745.回文串分割IV

[力扣](https://leetcode-cn.com/problems/palindrome-partitioning-iv/)

看这个数据规模是很容易想到O(n^2)的算法的。令f[l][r]表示l到r这一段是否为回文串，那么对于f[l][r]，就有：

1、若l \= r，那么f[l][r] \= true

2、若l \= r - 1，那么当s[l]等于s[r]时，f[l][r] \= ture，否则f[l][r] \= false

3、其他情况下，若f[l + 1][r - 1]为true，其s[l]等于s[r]时，f[l][r] \= true，否则f[l][r] \= false

这样一来，就可以在O(n^2)的时间复杂度得到f。接下来只需要枚举第一个回文串的右边界p1以及第二个回文串的右边界p2，那么此时枚举到的三个子串分别为[0, p1]，[p1 + 1, p2]，[p2 + 1, len(s) - 1]，然后通过f判断这三个子串是否都是回文串即可。

感觉应该存在O(n)的算法，但是并没有想出来。首先对于f[l][r]的求解，可以使用马拉车算法替代，从而在O(n)的时间复杂度内求出以每个字符为中心的最长回文串是什么。接下来枚举回文串的中心，在这里卡住了。因为随着第一个回文串中心向后推移，第二个回文串的中心并不一定也会向后移动，在这里失去了单调性，因此不能在O(n)的时间复杂度内确定三个回文串的中心位置。

简单想了一下，并没有找出什么有效的枚举方案，猜测可能可以从后缀方面去做文章。实际上对于回文串另一个经典的求法就是将s倒过来接在s的后面，中间使用分隔符进行分割，然后利用后缀数组来求解。不过在这里我就没有继续往下想了。

最后附上python代码：

```python
class Solution(object):
    def checkPartitioning(self, s):
        """
        :type s: str
        :rtype: bool
        """

        n = len(s)
        f = [[False] * n for _ in range(n)]
        for l in range(1, n + 1):
            for left in range(n):
                right = left + l - 1
                if left + l - 1 >= n:
                    continue
                if l == 1:
                    f[left][right] = True
                elif l == 2:
                    if s[left] == s[right]:
                        f[left][right] = True
                    else:
                        f[left][right] = False
                else:
                    f[left][right] = f[left + 1][right - 1] and s[left] == s[right]
        
        for p1 in range(n - 2):
            if f[0][p1]:
                for p2 in range(p1 + 1, n - 1):
                    if f[p1 + 1][p2] and f[p2 + 1][n - 1]:
                        return True
        
        return False
```
