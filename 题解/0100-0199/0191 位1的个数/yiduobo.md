---
title: "191. 位1的个数"
aliases: ["yiduobo的每日leetcode 191.位1的个数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/145932885"
zhihu_id: "145932885"
zhihu_title: "yiduobo的每日leetcode 191.位1的个数"
question_id: "191"
question: "位1的个数"
problem_url: "https://leetcode.cn/problems/number-of-1-bits/"
created: "2020-06-04T21:27:39+08:00"
updated: "2020-06-04T21:27:39+08:00"
upvotes: 0
comments: 0
---

# 191. 位1的个数

> **[yiduobo的每日leetcode 191.位1的个数](https://zhuanlan.zhihu.com/p/145932885) · 知乎 · 2020-06-04 · 赞同 0**
> 力扣：[191. 位1的个数](https://leetcode.cn/problems/number-of-1-bits/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

191.位1的个数<https://leetcode-cn.com/problems/number-of-1-bits/>

位运算的题目。依然是可以每次通过n&1取出最后一位，然后n>>\=1移动一位来做。不过这里有一种更好的写法，对于一个大于0的n，其中至少有一位是1，那么n一定可以写成

XXXXXXX 1 0000...000的形式，这里0可能有多个，也可能一个都没有

此时的n - 1为

XXXXXXX 0 1111...111，这里1的数量与上面0的数量相同，而XXXXXXX的部分与n一样

于是n &\= n - 1之后，就只剩下XXXXXXX的部分了，此时已经将最后一位1以及之后的0划掉了。这样做一定程度上可以起到优化的效果，但是总体的时间复杂度不变。

最后附上python代码：

```python
class Solution(object):
    def hammingWeight(self, n):
        """
        :type n: int
        :rtype: int
        """

        res = 0
        while n:
            res += 1
            n &= n - 1

        return res
```
