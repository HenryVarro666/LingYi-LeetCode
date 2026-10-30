---
title: "848. 字母移位"
aliases: ["yiduobo的每日leetcode 848.字母移位"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/348102852"
zhihu_id: "348102852"
zhihu_title: "yiduobo的每日leetcode 848.字母移位"
question_id: "848"
question: "字母移位"
problem_url: "https://leetcode.cn/problems/shifting-letters/"
created: "2021-01-31T21:38:01+08:00"
updated: "2021-01-31T21:38:01+08:00"
upvotes: 0
comments: 0
---

# 848. 字母移位

> **[yiduobo的每日leetcode 848.字母移位](https://zhuanlan.zhihu.com/p/348102852) · 知乎 · 2021-01-31 · 赞同 0**
> 力扣：[848. 字母移位](https://leetcode.cn/problems/shifting-letters/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

848.字母移位

[力扣](https://leetcode-cn.com/problems/shifting-letters/)

我们先来分析一下样例。对于样例中的a，其在第一次操作中移位3次，在第二次操作中移位5次，在最后一次操作中移位9次；对于样例中的b，其在第二次操作中移位5次，在最后一次操作中移位9次；对于样例中的c，其只在最后一次操作中移位9次。

a: 3 + 5 + 9

b: 5 + 9

c: 9

可以发现，这里每个字母的总移位实际上是一个后缀和问题，于是我们可以转换思路，从后往前一趟扫描，每次先按后缀和的方式计算移位的值，然后对当前字母进行移位。

最后附上python代码：

```python
class Solution(object):
    def shiftingLetters(self, S, shifts):
        """
        :type S: str
        :type shifts: List[int]
        :rtype: str
        """

        n = len(S)
        res = []
        now = 0
        for index in range(n - 1, -1, -1):
            now = (now + shifts[index]) % 26
            res.append(chr((ord(S[index]) - 97 + now) % 26 + 97))

        return ''.join(res[::-1])
```
