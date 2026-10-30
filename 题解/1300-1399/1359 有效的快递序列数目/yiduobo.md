---
title: "1359. 有效的快递序列数目"
aliases: ["yiduobo的每日leetcode 1359.有效的快递序列数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/399216229"
zhihu_id: "399216229"
zhihu_title: "yiduobo的每日leetcode 1359.有效的快递序列数目"
question_id: "1359"
question: "有效的快递序列数目"
problem_url: "https://leetcode.cn/problems/count-all-valid-pickup-and-delivery-options/"
created: "2021-08-12T23:12:26+08:00"
updated: "2021-08-12T23:12:26+08:00"
upvotes: 1
comments: 0
---

# 1359. 有效的快递序列数目

> **[yiduobo的每日leetcode 1359.有效的快递序列数目](https://zhuanlan.zhihu.com/p/399216229) · 知乎 · 2021-08-12 · 赞同 1**
> 力扣：[1359. 有效的快递序列数目](https://leetcode.cn/problems/count-all-valid-pickup-and-delivery-options/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1359.有效的快递序列数目

[力扣](https://leetcode-cn.com/problems/count-all-valid-pickup-and-delivery-options/)

设f[n]表示n笔订单时有效的快递序列数目，由于每件快递之间互相独立，那么我们不妨考察在n - 1笔订单的基础上，新增一笔快递的有效订单数目。

由于我们并不关心前n - 1笔订单的排序方式，那么不妨使用X代替D和P，对于n - 1笔订单，一个可行的排布为

X X X X ... X

一共有(n - 1) \* 2个X

此时我们需要将一个新的P和D插入到这个串中。首先，P一共有(n - 1) \* 2 + 1中可插入的位置，即

P X X ... X

X P X ... X

X X P ... X

...

X X ... X P

分别考察这些情况

P X X ... X

此时我们可以把D插入到P后面，或者两个X之间，或者序列的最后。这里一共有(n - 1) \* 2个X，那么插入到两个X之间一共有(n - 1) \* 2 - 1种方案，加上首位两种，那么合法方案的数目就是

(n - 1) \* 2 + 1

X P X ... X

与上面类似，但是这里两个X之间只能插在后面(n - 1) \* 2 - 1个X之间，因此合法方案的数目只有

(n - 1) \* 2

X X P ... X

同样与上面类似，这里后面可插入的X进一步减少，只有(n - 1) \* 2 - 2个，因此合法方案数为

(n - 1) \* 2 - 1

依次类推，直到最后X X ... X P这种情况时，只剩下将D插入到最后这一种可行的方案，因此一共有

s[n] \= ((n - 1) \* 2 + 1) + ((n - 1) \* 2) + ... + 2 + 1

\= (n \* 2 - 1) + (n \* 2 - 2) + ... + 1

\= (n \* 2 - 1 +1) \* (n \* 2 - 1) / 2

\= n \* (n \* 2 - 1)

\= 2 \* n^2 - n

那么就有

f[n] \= f[n - 1] \* s[n]

在这里可以每次都计算s[n]，不过我在这里采用的方法是对比s[n]与s[n - 1]之间的差值，随着n的增大同步更新s[n]。具体来说就是

s[n] \= 2 \* n^2 - n

s[n - 1] \= 2 \* (n - 1)^2 - (n - 1)

\= 2 \* (n^2 - n \* 2 + 1) - n + 1

\= 2 \* n^2 - n \* 5 + 3

那么就有s[n] \= s[n - 1] + n \* 4 - 3

由于这里的s和f每一步都只与上一轮状态有关，因此可以两个变量迭代，而不需要使用数组。

最后附上python代码：

```python
class Solution(object):
    def countOrders(self, n):
        """
        :type n: int
        :rtype: int
        """

        mod = 10 ** 9 + 7
        res = 1
        s = 1
        for num in range(2, n + 1):
            s += num * 4 - 3
            res = res * s % mod
        
        return res
```
