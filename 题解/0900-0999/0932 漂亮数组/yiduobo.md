---
title: "932. 漂亮数组"
aliases: ["yiduobo的每日leetcode 932.漂亮数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/357352007"
zhihu_id: "357352007"
zhihu_title: "yiduobo的每日leetcode 932.漂亮数组"
question_id: "932"
question: "漂亮数组"
problem_url: "https://leetcode.cn/problems/beautiful-array/"
created: "2021-03-15T22:33:44+08:00"
updated: "2021-03-15T22:33:44+08:00"
upvotes: 1
comments: 3
---

# 932. 漂亮数组

> **[yiduobo的每日leetcode 932.漂亮数组](https://zhuanlan.zhihu.com/p/357352007) · 知乎 · 2021-03-15 · 赞同 1**
> 力扣：[932. 漂亮数组](https://leetcode.cn/problems/beautiful-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

932.漂亮数组

[力扣](https://leetcode-cn.com/problems/beautiful-array/)

首先可以分析一下A[k] \* 2 \= A[i] + A[j]这个条件。

显然，若A[i]为奇数、A[j]为偶数，或者A[i]为偶数、A[j]为奇数，那么必然是不存在A[k]的，因此一个自然的想法就是将奇数和偶数分开对待。

接下来，若存在一个数组A为漂亮数组，那么将A中每个数乘以2，得到的也必然是漂亮数组。具体的证明也很简单。

设A中每个数乘以2之后得到的数组为A'：

若A'中存在一组i、j、k满足i \< k \< j且A'[i] + A'[j] \= 2 \* A'[k]，那么

A'[i] + A'[j] \= A[i] \* 2 + A[j] \* 2 \= 2 \* (A[i] + A[j]) \= 2 \* A'[k] \= 2 \* (2 \* A[k])

约掉一个2之后就有A[i] + A[j] \= 2 \* A[k]，这就与A是漂亮数组产生了矛盾。

同样的，若存在一个数组A为漂亮数组，那么将A中每个数乘以2再减1，得到的也必然是漂亮数组。

于是此时就有了一种构造的方法。

1、首先初始化A为[1]。

2、接下来每一轮，先将A中每个数乘以2得到E，然将A中每个数乘以2减去1得到O。根据上面的结论，此时得到的E和O都是漂亮数组。设当前轮次为k，那么E中包含了2到2^k中的所有偶数，而O中则包含了1到2^k - 1中的所有奇数。接下来将E和O拼起来，得到新的A。根据上面的结论，此时新的A也是漂亮数组，且新的A是1到2^k的一个排列。

重复这个过程直到A的长度大于等于N，然后按顺序选择A中小于等于N的数作为答案即可。

最后附上python代码：

```python
class Solution(object):
    def beautifulArray(self, N):
        """
        :type N: int
        :rtype: List[int]
        """

        l = 1
        now = [1]
        while l < N:
            now = [x + x - 1 for x in now] + [x + x for x in now]
            l += l
        
        res = []
        for num in now:
            if num <= N:
                res.append(num)
        
        return res
```
