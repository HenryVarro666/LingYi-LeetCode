---
title: "483. 最小好进制"
aliases: ["yiduobo的每日leetcode 483.最小好进制"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/248999289"
zhihu_id: "248999289"
zhihu_title: "yiduobo的每日leetcode 483.最小好进制"
question_id: "483"
question: "最小好进制"
problem_url: "https://leetcode.cn/problems/smallest-good-base/"
created: "2020-09-16T22:00:17+08:00"
updated: "2020-09-16T22:00:17+08:00"
upvotes: 1
comments: 0
---

# 483. 最小好进制

> **[yiduobo的每日leetcode 483.最小好进制](https://zhuanlan.zhihu.com/p/248999289) · 知乎 · 2020-09-16 · 赞同 1**
> 力扣：[483. 最小好进制](https://leetcode.cn/problems/smallest-good-base/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

483.最小好进制<https://leetcode-cn.com/problems/smallest-good-base/>

如果一个数n可以写成k进制下的111...1，那么就有

n \= 1 + k + k^2 + ... + k^p

根据等比数列求和公式，那么就有

n \= (k^(p + 1) - 1) / (k - 1)

变形后可以得到

nk - n + 1 \= k^(p + 1)

那么就有

nk \= k^(p + 1) + n - 1 > k^(p + 1)

约掉一个k然后开方后就有

n^(1/p) > k

另外，对于(k + 1)^p，有

(k + 1)^p \* (k - 1) > k^(p + 1) - 1

因此就有

(k + 1) ^ p > n

开放后有

k + 1 > n^(1/p)

综上就有n^(1/p) - 1 \< k \< n^(1/p)

对于这个p，存在一个上界，即最多为n在2进制下的位数，于是我们可以枚举这里的p，然后通过上面这个不等式确定k，最后确认k和p是否符合条件。

最后附上python代码：

```python
class Solution(object):
    def smallestGoodBase(self, n):
        """
        :type n: str
        :rtype: str
        """

        max_p = int(log(float(n)) / log(2))
        for p in range(max_p, 1, -1):
            k = int(float(n) ** (1 / float(p)))
            if (k ** (p + 1) - 1) == int(n) * (k - 1):
                return str(k)

        return str(int(n) - 1)
```
