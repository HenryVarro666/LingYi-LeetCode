---
title: "1291. 顺次数"
aliases: ["yiduobo的每日leetcode 1291.顺次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration", "leetcode/sliding-window"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/389779003"
zhihu_id: "389779003"
zhihu_title: "yiduobo的每日leetcode 1291.顺次数"
question_id: "1291"
question: "顺次数"
problem_url: "https://leetcode.cn/problems/sequential-digits/"
difficulty: "Medium"
created: "2021-07-14T22:54:35+08:00"
updated: "2021-07-14T22:54:35+08:00"
upvotes: 0
comments: 0
---

# 1291. 顺次数

> **[yiduobo的每日leetcode 1291.顺次数](https://zhuanlan.zhihu.com/p/389779003) · 知乎 · 2021-07-14 · 赞同 0**
> 力扣：[1291. 顺次数](https://leetcode.cn/problems/sequential-digits/) · Medium · 灵茶山艾府：[枚举子串 / 定长滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1291.顺次数

[力扣](https://leetcode-cn.com/problems/sequential-digits/)

题目看上去很复杂，且low和high之间相差很大，不过实际上可以成为答案的数值并不多。

首先考察两位数，此时有

12，23，34，45，56，67，78，89

而对于三位数，则有

123，234，345，456，567，678，789

可以发现三位数的可行解就是两位数中的

12，23，34，45，56，67，78

分别乘以10，然后将原来的最后一位复制之后加上1之后得来的

那么实际上，最多也就只有8 + 7 + ... + 1一共是36个可能的解，于是我们可以先将这些数按顺序生成出来，然后根据给出的low和high找出合法的最小解和最大解即可。

最后附上python代码：

```python
class Solution(object):
    def sequentialDigits(self, low, high):
        """
        :type low: int
        :type high: int
        :rtype: List[int]
        """
        
        q = range(1, 9)
        l = 0
        r = len(q)
        while l < r:
            now = q[l]
            l += 1
            last = now % 10
            if last != 9:
                next = now * 10 + last + 1
                if next > high:
                    break
                q.append(next)
                r += 1
        
        l = 0
        while l < r and q[l] < low:
            l += 1

        return q[l : r]
```
