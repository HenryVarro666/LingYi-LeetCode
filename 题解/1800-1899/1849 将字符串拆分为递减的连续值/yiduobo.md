---
title: "1849. 将字符串拆分为递减的连续值"
aliases: ["yiduobo的每日leetcode 1849.将字符串拆分为递减的连续值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "leetcode/enumeration", "leetcode/bao-li", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/四-回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/471046444"
zhihu_id: "471046444"
zhihu_title: "yiduobo的每日leetcode 1849.将字符串拆分为递减的连续值"
question_id: "1849"
question: "将字符串拆分为递减的连续值"
problem_url: "https://leetcode.cn/problems/splitting-a-string-into-descending-consecutive-values/"
difficulty: "Medium"
rating: 1747
created: "2022-02-22T23:32:20+08:00"
updated: "2022-02-22T23:32:20+08:00"
upvotes: 0
comments: 0
---

# 1849. 将字符串拆分为递减的连续值

> **[yiduobo的每日leetcode 1849.将字符串拆分为递减的连续值](https://zhuanlan.zhihu.com/p/471046444) · 知乎 · 2022-02-22 · 赞同 0**
> 力扣：[1849. 将字符串拆分为递减的连续值](https://leetcode.cn/problems/splitting-a-string-into-descending-consecutive-values/) · Medium · 灵茶山艾府：[枚举第一个数，时间复杂度 O(N^2)](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1849.将字符串拆分为递减的连续值

[力扣](https://leetcode-cn.com/problems/splitting-a-string-into-descending-consecutive-values/)

由于题目要求的是逐一递减的连续值，那么在确定了第一个数之后，后面的每一个数也就确定下来了。于是可以从头开始向后枚举第一个数，然后根据上一个数的数值判断当前剩余字符串的前缀能否构成下一个数，直到末尾。

另外，字符串中的零需要注意处理。首先前导零是完全可以忽略的，因此在枚举第一个数之前可以先跳过字符串的前导零。另一方面，当递减数列的最后一个数为零时，若字符串还没有到达末尾，此时就需要判断字符串中剩余的字符是否都为零，这样就能让一长串零形成需要的零。

最后附上python代码：

```python
class Solution(object):
    def splitString(self, s):
        """
        :type s: str
        :rtype: bool
        """

        n = len(s)
        start = 0
        while start < n and s[start] == '0':
            start += 1
        
        if start >= n - 1:
            return False
        
        first = 0
        for index in range(start, n - 1):
            first = first * 10 + int(s[index])
            last = first
            p = index + 1
            flag = True
            while p < n:
                if last == 0:
                    while p < n and s[p] == '0':
                        p += 1
                    if p != n:
                        flag = False
                    break

                now = int(s[p])
                p += 1
                while p < n and now < last - 1:
                    now = now * 10 + int(s[p])
                    p += 1

                if now != last - 1:
                    flag = False
                    break
                last = now

            if flag:
                return True
        
        return False
```
