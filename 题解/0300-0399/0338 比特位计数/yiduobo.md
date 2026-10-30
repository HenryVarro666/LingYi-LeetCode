---
title: "338. 比特位计数"
aliases: ["yiduobo的每日leetcode 338.比特位计数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/162685936"
zhihu_id: "162685936"
zhihu_title: "yiduobo的每日leetcode 338.比特位计数"
question_id: "338"
question: "比特位计数"
problem_url: "https://leetcode.cn/problems/counting-bits/"
created: "2020-07-21T20:40:54+08:00"
updated: "2020-07-21T20:40:54+08:00"
upvotes: 1
comments: 0
---

# 338. 比特位计数

> **[yiduobo的每日leetcode 338.比特位计数](https://zhuanlan.zhihu.com/p/162685936) · 知乎 · 2020-07-21 · 赞同 1**
> 力扣：[338. 比特位计数](https://leetcode.cn/problems/counting-bits/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

338.比特位计数<https://leetcode-cn.com/problems/counting-bits/>

我们首先考察几个小数字二进制下的情况：

0 - > 000

1 - > 001

2 - > 010

3 - > 011

4 - > 100

5 - > 101

6 - > 110

7 - > 111

我们首先看0和1，可以发现，1是将0从右往左数的第一位从0变成了1。

接下来，将0、1和2、3拎出来看，可以发现，实际上2和3分别就是将0和1从右往左数第二位上的0变成了1。

再然后看0、1、2、3与4、5、6、7，可以发现，4、5、6、7则是将0、1、2、3从右往左数第三位上的0变成了1。

更一般的，对于0、1、2、...、2^k - 1与2^k、2^k +1、2^k + 2、...、2^(k + 1) - 1，如果用后面的数减去前面的数，都刚好是2^k，对应到二进制上就是从右往左数第(k + 1)位从0变成了1，这也就意味着，2^k比0多出在第(k + 1)上的1，而2^k + 1比1同样是多出第(k + 1)上的1，依次类推。

于是，我们可以先设f数组为[0]，代表0的二进制表示中有0个1。

接下来，考察1，由于1 - 0 \= 2^0，因此1应该比0多出一个1，即f[1] \= f[0] + 1。

再往后考察2和3，可以得到，2 - 0 \= 3 - 1 \= 2^1，因此2比0多出一个1，3比1多出一个1，于是有f[2] \= f[0] + 1，f[3] \= f[1] + 1。

以此类推，那么对于f[2^k]到f[2^(k + 1) - 1]，其应该等于f[0]到f[2^k - 1]分别加一。

于是我们可以通过上面的规律每次倍增f，直到f的长度到底n为止。每次迭代遍历的次数分别为1、2、4、8、...、2^k，其中2^(k + 1)>\=n，于是最终的时间复杂度为O(n)。

最后附上python代码：

```python
class Solution(object):
    def countBits(self, num):
        """
        :type num: int
        :rtype: List[int]
        """

        f = [0]
        while len(f) < num + 1:
            f.extend([x + 1 for x in f])

        return f[:num + 1]
```
