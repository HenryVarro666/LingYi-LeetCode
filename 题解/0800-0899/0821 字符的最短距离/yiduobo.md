---
title: "821. 字符的最短距离"
aliases: ["yiduobo的每日leetcode 821.字符的最短距离"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/343858467"
zhihu_id: "343858467"
zhihu_title: "yiduobo的每日leetcode 821.字符的最短距离"
question_id: "821"
question: "字符的最短距离"
problem_url: "https://leetcode.cn/problems/shortest-distance-to-a-character/"
created: "2021-01-17T19:10:49+08:00"
updated: "2021-01-17T19:10:49+08:00"
upvotes: 0
comments: 0
---

# 821. 字符的最短距离

> **[yiduobo的每日leetcode 821.字符的最短距离](https://zhuanlan.zhihu.com/p/343858467) · 知乎 · 2021-01-17 · 赞同 0**
> 力扣：[821. 字符的最短距离](https://leetcode.cn/problems/shortest-distance-to-a-character/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

821.字符的最短距离

[力扣](https://leetcode-cn.com/problems/shortest-distance-to-a-character/)

对于字符串中的每个字符，设其下标为index，那么只需要找出从0到index这一段中C最后一次出现的位置prev[index]，以及从index到n - 1这一段中C最早一次出现的位置next[index]，然后取index - prev[index]以及next[index] - index中较小的那个即可。

为了得到next和prev，则可以从头到尾一趟扫描然后再从尾到头一趟扫描分别得到。

最后附上python代码：

```python
class Solution(object):
    def shortestToChar(self, S, C):
        """
        :type S: str
        :type C: str
        :rtype: List[int]
        """

        n = len(S)

        if S[0] == C:
            prev = [0]
        else:
            prev = [-1]
        for index in range(1, n):
            if S[index] == C:
                prev.append(index)
            else:
                prev.append(prev[-1])
        
        if S[n - 1] == C:
            next = [n - 1]
        else:
            next = [-1]
        for index in range(n - 2, -1, -1):
            if S[index] == C:
                next.append(index)
            else:
                next.append(next[-1])
        next.reverse()

        res = []
        for index in range(n):
            if prev[index] == -1:
                res.append(next[index] - index)
            elif next[index] == -1:
                res.append(index - prev[index])
            else:
                res.append(min(next[index] - index, index - prev[index]))
        
        return res
```
