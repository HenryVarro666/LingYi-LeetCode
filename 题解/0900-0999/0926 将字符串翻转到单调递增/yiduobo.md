---
title: "926. 将字符串翻转到单调递增"
aliases: ["yiduobo的每日leetcode 926.将字符串翻转到单调递增"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/356682784"
zhihu_id: "356682784"
zhihu_title: "yiduobo的每日leetcode 926.将字符串翻转到单调递增"
question_id: "926"
question: "将字符串翻转到单调递增"
problem_url: "https://leetcode.cn/problems/flip-string-to-monotone-increasing/"
created: "2021-03-12T18:50:12+08:00"
updated: "2021-03-12T18:50:12+08:00"
upvotes: 0
comments: 0
---

# 926. 将字符串翻转到单调递增

> **[yiduobo的每日leetcode 926.将字符串翻转到单调递增](https://zhuanlan.zhihu.com/p/356682784) · 知乎 · 2021-03-12 · 赞同 0**
> 力扣：[926. 将字符串翻转到单调递增](https://leetcode.cn/problems/flip-string-to-monotone-increasing/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

926.将字符串翻转到单调递增

[力扣](https://leetcode-cn.com/problems/flip-string-to-monotone-increasing/)

我们不妨从后往前来看这个问题。

对于最后一个字符：

1、若其值为1，那么其前面的字符都不会应该该字符破坏单调性，因此可以往前考虑倒数第二个字符。

2、若其值为0，那么要么将其修改为1，此时就回到了情况1，需要往前考虑倒数第二个字符，同时此时已经进行了1次修改；要么将其前面的所有字符都置为0，此时整个字符串就是单调递增的了，但是需要将前面所有的1修改成0，那么此时修改的次数就是前面所有1的个数。

接下来对于倒数第二个字符，也是如法炮制。更进一步的，对于每个字符，只有当该字符为0的时候才需要考虑如何进行修改，否则都可以直接考虑更前面的字符。

对于情况2中用到的前面所有1的个数，则可以从头到尾一趟扫描，预处理出一个前缀中1的数量来提高效率。

最后附上python代码：

```python
class Solution(object):
    def minFlipsMonoIncr(self, S):
        """
        :type S: str
        :rtype: int
        """

        one = [0]
        for char in S:
            if char == '0':
                one.append(one[-1])
            else:
                one.append(one[-1] + 1)
        
        res = len(S) + 1
        cnt = 0
        for index in range(len(S) - 1, -1, -1):
            if S[index] == '1':
                continue
            res = min(res, cnt + one[index])
            cnt += 1
        
        return min(res, cnt)
```
