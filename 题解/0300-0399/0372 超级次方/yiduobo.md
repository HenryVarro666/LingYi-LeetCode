---
title: "372. 超级次方"
aliases: ["yiduobo的每日leetcode 372.超级次方"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/165391440"
zhihu_id: "165391440"
zhihu_title: "yiduobo的每日leetcode 372.超级次方"
question_id: "372"
question: "超级次方"
problem_url: "https://leetcode.cn/problems/super-pow/"
created: "2020-07-30T21:17:16+08:00"
updated: "2020-07-30T21:17:16+08:00"
upvotes: 0
comments: 0
---

# 372. 超级次方

> **[yiduobo的每日leetcode 372.超级次方](https://zhuanlan.zhihu.com/p/165391440) · 知乎 · 2020-07-30 · 赞同 0**
> 力扣：[372. 超级次方](https://leetcode.cn/problems/super-pow/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

72.超级次方<https://leetcode-cn.com/problems/super-pow/>

乍一看感觉是经典的快速幂问题，但是这里的幂次很大，因此不能用经典的方法处理。

注意到这里的幂次已经按十进制切分好了，而题目中要求的

a^(b[n] \* 10^n + b[n - 1] \* 10^(n - 1) + ... + b[0] \* 10^0)

按照秦九韶公式合并10的幂次之后，可以写成

a^(((((((b[n] \* 10) + b[n - 1]) \* 10) + b[n - 2]) \* 10) + ...) \* 10 + b[0])

幂次的括号打开之后，就是

(((((a^b[n]) ^ 10) \* (a^b[n - 1])) ^ 10 \* (a^b[n - 2])) ^ 10 \* ...) ^ 10) \* (a^b[0])

于是，我们可以将b从左往右一趟扫描，按上面这个式子逐步计算即可。

这里的幂次必然在0到10之间，因此用不用快速幂差别应该不大。

注意到最终答案需要模1337，因此可以使用一个1337\*10的数组来记录0到1136中每个数的0到10次方模1337之后等于多少，可以起到一定的优化作用。

最后附上python代码：

```python
class Solution(object):
    def superPow(self, a, b):
        """
        :type a: int
        :type b: List[int]
        :rtype: int
        """

        f = [[None] * 11 for _ in range(1337)]

        res = 1
        a %= 1337
        for p in b:
            res = self.get_pow(res, 10, f) * self.get_pow(a, p, f) % 1337

        return res

    def get_pow(self, a, b, f):
        if f[a][b] is None:
            if b == 0:
                f[a][b] = 1
            elif b == 1:
                f[a][b] = a
            else:
                tmp = self.get_pow(a, b/2, f)
                if b & 1:
                    f[a][b] = tmp * tmp * a % 1337
                else:
                    f[a][b] = tmp * tmp

        return f[a][b]
```
