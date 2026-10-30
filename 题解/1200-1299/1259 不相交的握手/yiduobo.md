---
title: "1259. 不相交的握手"
aliases: ["yiduobo的每日leetcode 1259.不相交的握手"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/615024674"
zhihu_id: "615024674"
zhihu_title: "yiduobo的每日leetcode 1259.不相交的握手"
question_id: "1259"
question: "不相交的握手"
problem_url: "https://leetcode.cn/problems/handshakes-that-dont-cross/"
created: "2023-03-18T15:16:57+08:00"
updated: "2023-03-18T15:16:57+08:00"
upvotes: 0
comments: 0
---

# 1259. 不相交的握手

> **[yiduobo的每日leetcode 1259.不相交的握手](https://zhuanlan.zhihu.com/p/615024674) · 知乎 · 2023-03-18 · 赞同 0**
> 力扣：[1259. 不相交的握手](https://leetcode.cn/problems/handshakes-that-dont-cross/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1259.不想交的握手

[力扣](https://leetcode.cn/problems/handshakes-that-dont-cross/)

首先，奇数个人的握手方案数必然为0。接下来，当一次握手发生后，这些人将被分为不相交的两个部分，也就是说转化成了两个子问题，因此在这里可以使用规划来求解。

令f[i]表示i个人合法的握手方案数，那么对于f[i]，首先有边界情况f[0] \= 1，而当i为奇数时，有f[i] \= 0，因此只需要考虑i为偶数的情况。不妨考虑这i个人中编号最小的那个人的握手的情况，其握手的对象只能是编号大小从小到大排序在第1、3、5、...、i - 1位的人握手，否则就会将这i个人划分为奇数的两个部分。而对于上面这些位置，设选择的握手对象是第j位的人，那么剩下的人就被分成了j - 1以及i - 2 - (j - 1)这两个部分，因此就有

f[i] \= sum(f[j - 1] \* f[i - j - 1])，其中1 \<\= j \<\= i - 1，且j为奇数

更进一步的，在这里可以直接从握手对的角度来考虑问题。令f[i]表示i对人可行的握手方案数，那么对于f[i]，同样是边界f[0] \= 1，而对于i > 1，则可以枚举被切分出去的握手对数j，那么就有

f[i] \= sum(f[j] \* f[i - j - 1])

另外，上面这个式子是标准的卡特兰数递推式，可以使用组合数学的方法求解，时间复杂度更优。

最后附上python代码：

```python
class Solution(object):
    def numberOfWays(self, numPeople):
        """
        :type numPeople: int
        :rtype: int
        """

        mod = 10 ** 9 + 7
        n = numPeople / 2

        f = [0] * (n + 1)
        f[0] = 1
        for i in range(1, n + 1):
            for j in range(i):
                f[i] += f[j] * f[i - j - 1]
                f[i] %= mod
        
        return f[n]
```
