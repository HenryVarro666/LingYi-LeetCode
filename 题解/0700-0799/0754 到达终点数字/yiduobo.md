---
title: "754. 到达终点数字"
aliases: ["yiduobo的每日leetcode 754.到达终点数字"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/zheng-ming", "leetcode/fen-lei-tao-lun", "题单/贪心算法", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/338170643"
zhihu_id: "338170643"
zhihu_title: "yiduobo的每日leetcode 754.到达终点数字"
question_id: "754"
question: "到达终点数字"
problem_url: "https://leetcode.cn/problems/reach-a-number/"
difficulty: "Medium"
rating: 2000
created: "2020-12-20T00:01:15+08:00"
updated: "2020-12-20T00:01:15+08:00"
upvotes: 0
comments: 0
---

# 754. 到达终点数字

> **[yiduobo的每日leetcode 754.到达终点数字](https://zhuanlan.zhihu.com/p/338170643) · 知乎 · 2020-12-20 · 赞同 0**
> 力扣：[754. 到达终点数字](https://leetcode.cn/problems/reach-a-number/) · Medium · 灵茶山艾府：[分类讨论+详细证明+简洁写法+优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

754.到达终点数字

[力扣](https://leetcode-cn.com/problems/reach-a-number/)

题目中描述的向左向右，可以看做对于1到n这n个数，在每个数前面添加加号或者减号，然后计算这个表达式的和，使其等于target。

首先，target与-target实际上是等价的。如果可以得到target，那么将当前式子所有的加减号反过来，那么就可以得到-target。因此，对于target为负的情况，我们可以反过来考虑-target，即保证此时的目标为正数。

接下来，1到n的和为s \= (1 + n) \* n / 2，那么至少要走到满足s >\= target的n才能停下。不妨设delta \= s - target，那么此时我们的目标就是从1到n中找出一些数，使得这些数的和为delta / 2。于是，这里的delta就必须为偶数。若不为偶数，则需要将n变为n + 1或者n + 2。

最后，当delta为偶数时，必然是可以从1到n中找出某些数使得这些数的和为delta / 2的。

证明的话可以先证明对于1到n，其中某些数的和可以覆盖0到(1 + n) \* n / 2。

这里可以使用数学归纳法，若1到n - 1中某些数的和可以覆盖0到n \* (n - 1) / 2，就意味着某些数的和可以覆盖n \* (n - 1) / 2 - n + 1到n \* (n - 1) / 2这一段。那么在这个基础上加入n，就可以覆盖n \* (n - 1) / 2到n \* (n + 1) / 2这一段。边界条件n \= 1时，可以覆盖0到1。

根据上面的结论，现在的做法就是

1、通过对target开根号找出满足s >\= target的最小的n

2、判断delta \= s - target的奇偶性，若delta为偶数，那么答案为n；若delta为奇数，则考察n + 1对应delta的奇偶性。

此时n对应delta为奇数，那么n + 1对应的delta的奇偶性取决于n + 1自身的奇偶性，若n + 1为奇数，那么n + 1对应delta为偶数，否则奇数。

于是此时可以判断若n为奇数，那么最终答案为n + 2，否则为n + 1。

最后附上python代码：

```python
class Solution(object):
    def reachNumber(self, target):
        """
        :type target: int
        :rtype: int
        """

        if target < 0:
            target = -target
        res = int(sqrt(target))
        s = (1 + res) * res / 2
        while s < target:
            res += 1
            s += res
        
        delta = s - target
        if delta % 2 == 0:
            return res
        elif res % 2 == 1:
            return res + 2
        else:
            return res + 1
```
