---
title: "985. 查询后的偶数和"
aliases: ["yiduobo的每日leetcode 985.查询后的偶数和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/363810550"
zhihu_id: "363810550"
zhihu_title: "yiduobo的每日leetcode 985.查询后的偶数和"
question_id: "985"
question: "查询后的偶数和"
problem_url: "https://leetcode.cn/problems/sum-of-even-numbers-after-queries/"
created: "2021-04-10T18:52:54+08:00"
updated: "2021-04-10T18:52:54+08:00"
upvotes: 0
comments: 0
---

# 985. 查询后的偶数和

> **[yiduobo的每日leetcode 985.查询后的偶数和](https://zhuanlan.zhihu.com/p/363810550) · 知乎 · 2021-04-10 · 赞同 0**
> 力扣：[985. 查询后的偶数和](https://leetcode.cn/problems/sum-of-even-numbers-after-queries/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

985.查询后的偶数和

[力扣](https://leetcode-cn.com/problems/sum-of-even-numbers-after-queries/)

由于每一次操作最多只会影响一个数的奇偶性，那么我们可以首先预先计算出A中所有偶数的和s，然后依次遍历queries。对于当前的操作index，val，有下面几种情况：

1、A[index]为偶数，且val为偶数：

A[index]为偶数，已经被计算在s当中。A[index]加上val后依然为偶数，也应当被计算在s当中，那么就有

s \= A[index] + other

s' \= other + (A[index] + val)

其中other表示除A[index]外的其他偶数。

通过这两个式子就可以得到s' \= s + val

2、A[index]为偶数，且val为奇数：

A[index]为偶数，已经被计算在s当中。A[index]加上val后为奇数，不应当被计算在s当中，那么就有

s \= A[index] + other

s' \= other

于是有s' \= s - A[index]

3、A[index]为奇数，val为偶数：

A[index]为奇数，没有被计算在s当中。A[index]加上val后依然为奇数，不应当被计算在s当中，于是此时无事发生

4、A[index]为奇数，val为奇数：

A[index]为奇数，没有被计算在s当中。A[index]加上val后偶数，应当被计算在s当中，那么就有

s' \= s + (A[index] + val)

根据上面的结论每次操作持续更新A[index]以及当前的s即可。

最后附上python代码：

```python
class Solution(object):
    def sumEvenAfterQueries(self, A, queries):
        """
        :type A: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        now = 0
        for num in A:
            if num % 2 == 0:
                now += num
        
        res = []
        for delta, index in queries:
            if A[index] % 2 == 0:
                if delta % 2 == 0:
                    now += delta
                else:
                    now -= A[index]
                
                res.append(now)
                A[index] += delta
            
            else:
                A[index] += delta
                if A[index] % 2 == 0:
                    now += A[index]
                
                res.append(now)

        return res
```
