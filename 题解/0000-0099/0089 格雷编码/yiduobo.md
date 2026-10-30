---
title: "89. 格雷编码"
aliases: ["yiduobo的每日leetcode 89.格雷编码"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/134184282"
zhihu_id: "134184282"
zhihu_title: "yiduobo的每日leetcode 89.格雷编码"
question_id: "89"
question: "格雷编码"
problem_url: "https://leetcode.cn/problems/gray-code/"
created: "2020-04-25T20:49:52+08:00"
updated: "2020-04-25T20:49:52+08:00"
upvotes: 0
comments: 0
---

# 89. 格雷编码

> **[yiduobo的每日leetcode 89.格雷编码](https://zhuanlan.zhihu.com/p/134184282) · 知乎 · 2020-04-25 · 赞同 0**
> 力扣：[89. 格雷编码](https://leetcode.cn/problems/gray-code/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

89.格雷编码<https://leetcode-cn.com/problems/gray-code/>

比较有意思的题目。我在这里运用了一种类似动态规划的做法。

首先对于一种合法的格雷码，例如样例中的

00 - 0

01 - 1

11 - 3

10 - 2

我们将其反过来写，也一定是合法的，即：

10 - 2

11 - 3

01 - 1

00 - 0

那么，对于k位格雷码来说，可以在最高位上补0，看做k + 1位的格雷码作为前半部分，然后将这个k位格雷码反过来，在最高位补1作为k + 1位格雷码的后半部分。

还是样例中的2位的格雷码：

00 - 0

01 - 1

11 - 3

10 - 2

接下来要计算3位的格雷码，首先前半部分，照搬2位的格雷码然后在最高位补0：

0 00 - 0

0 01 - 1

0 11 - 3

0 10 - 2

然后后半部分，将2位格雷码反过来，然后在最高位补1：

1 10 - 6

1 11 - 7

1 01 - 5

1 00 - 4

这里主要就是利用了上面将格雷码反过来写依然合法这个原理。

具体实现时，先计算出最高位的值weight，也就是2的幂次，然后直接将上一轮的res反过来，加上这个最高位的值之后接在后面即可。

最后附上python代码：

```python
class Solution(object):
    def grayCode(self, n):
        """
        :type n: int
        :rtype: List[int]
        """

        res = [0]

        for index in range(n):
            if index == 0:
                weight = 1
            else:
                weight += weight
            res.extend([res[pos] + weight for pos in range(len(res) - 1, -1, -1)])

        return res
```
