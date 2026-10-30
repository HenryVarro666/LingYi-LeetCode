---
title: "1573. 分割字符串的方案数"
aliases: ["yiduobo的每日leetcode 1573.分割字符串的方案数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/429093284"
zhihu_id: "429093284"
zhihu_title: "yiduobo的每日leetcode 1573.分割字符串的方案数"
question_id: "1573"
question: "分割字符串的方案数"
problem_url: "https://leetcode.cn/problems/number-of-ways-to-split-a-string/"
created: "2021-11-03T20:11:50+08:00"
updated: "2021-11-03T20:11:50+08:00"
upvotes: 0
comments: 0
---

# 1573. 分割字符串的方案数

> **[yiduobo的每日leetcode 1573.分割字符串的方案数](https://zhuanlan.zhihu.com/p/429093284) · 知乎 · 2021-11-03 · 赞同 0**
> 力扣：[1573. 分割字符串的方案数](https://leetcode.cn/problems/number-of-ways-to-split-a-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1573.分割字符串的方案数

[力扣](https://leetcode-cn.com/problems/number-of-ways-to-split-a-string/)

题目要求将字符串分成三个部分，每个部分中的1的数目一致。

先考察边界情况。若字符串里面全部都是0，那么就相当于将n个球放到3个盒子里面，盒子里面不能为空，问有多少种做法。简单理解可以认为是在n个球之间的n - 1个间隔之间插入两块板子，此时的答案就是C(n - 1, 2)，即(n - 1) \* (n - 2) / 2。

接下来考虑一般的情况，不妨设字符串中1的个数为cnt。

若cnt不是3的倍数，那么答案必然为0。若cnt是3的倍数，则可以从两侧开始，向中间分别数cnt/3个1，此时可以得到两个位置l和r。接下来找出l下一个1的位置l_next，以及r的前一个位置r_prev，而最终的操作空间就是l + 1到l_next - 1之间的0，以及r_prev + 1到r - 1之间的0，即l + 1到l_next - 1之间的0应该归第一段还是第二段，以及r_prev + 1到r - 1之间的0应该归第二段还是第三段。

l + 1到l_next - 1之间一共有l_next - l - 1个0，那么分配给第一段的0的数目可以是0到l_next - l - 1中的某一种，一共有l_next - l种方案。类似的，r_prev + 1到r - 1之间的0一共有r - r_prev种分配方案，因此此时的方案数一共是(l_next - l) \* (r - r_prev)。

最后附上python代码：

```python
class Solution(object):
    def numWays(self, s):
        """
        :type s: str
        :rtype: int
        """

        cnt = 0
        for char in s:
            if char == '1':
                cnt += 1
        
        n = len(s)
        mod = 10 ** 9 + 7
        if cnt == 0:
            return (n - 1) * (n - 2) / 2 % mod
        
        if cnt % 3 != 0:
            return 0
        
        cnt /= 3
        now = 0
        for index in range(n):
            if s[index] == '1':
                now += 1
                if now == cnt:
                    break
        
        p = index + 1
        while s[p] != '1':
            p += 1

        l_cnt = p - index - 1

        now = 0
        for index in range(n - 1, -1, -1):
            if s[index] == '1':
                now += 1
                if now == cnt:
                    break
        
        p = index - 1
        while s[p] != '1':
            p -= 1
        
        r_cnt = index - p - 1

        return (l_cnt + 1) * (r_cnt + 1) % mod
```
