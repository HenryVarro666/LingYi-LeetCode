---
title: "1352. 最后K个数的乘积"
aliases: ["yiduobo的每日leetcode 1352.最后K个数的乘积"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/398066739"
zhihu_id: "398066739"
zhihu_title: "yiduobo的每日leetcode 1352.最后K个数的乘积"
question_id: "1352"
question: "最后K个数的乘积"
problem_url: "https://leetcode.cn/problems/product-of-the-last-k-numbers/"
created: "2021-08-09T22:53:34+08:00"
updated: "2021-08-09T22:53:34+08:00"
upvotes: 0
comments: 0
---

# 1352. 最后K个数的乘积

> **[yiduobo的每日leetcode 1352.最后K个数的乘积](https://zhuanlan.zhihu.com/p/398066739) · 知乎 · 2021-08-09 · 赞同 0**
> 力扣：[1352. 最后K个数的乘积](https://leetcode.cn/problems/product-of-the-last-k-numbers/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1352.最后K个数的乘积

[力扣](https://leetcode-cn.com/problems/product-of-the-last-k-numbers/)

题目要求最后k个数的乘积，一个可行的做法就是利用前缀乘积来处理，即

a[0] \* a[1] \* ... \* a[n - 1] \= (a[0] \* a[1] \* ... \* a[n - k - 1]) \* (a[n - k] \* ... \* a[n - 1])

可以发现，等号左侧是当前数组中所有数的乘积，右侧的前半部分是数组中前n - k个数的乘积，而后半部分则是要求的最后k个数的乘积，那么我们可以使用一个数组m来储存前缀乘积，每新来一个数，就使用同步更新前缀乘积数组，而我们需要求解最后k个数的乘积时，就可以使用m[n - 1] / m[n - k - 1]来求解了。

需要注意的是，题目中可能出现0的情况，那么上面的除法有可能会失效，于是对于0的情况我们需要特殊处理。

首先，若最后k个数中就有0，那么此时答案为0。为了处理这种情况，我们需要记录下最后一个0出现的位置。若这个位置大于等于n - k，那么说明最后k个数中有0。

接下来，当新来一个0时，前缀乘积数组就需要重启。一般情况下，m[n - 1] \= m[n - 2] \* a[n]，而当某一时刻a[n - 2] \= 0时，我们需要置m[n - 2] \= 0，而此时的m[n]就不应该再通过上面的乘法计算得来，而是应该直接置m[n - 1]为a[n - 1]。

同时，由于上面对于0的特殊处理，那么若最后一个0的位置是第m - k - 1位，那么说明此时的前缀乘积数组从第n - k位开始进行了重置，于是最终答案不应该是m[n - 1] / m[n - k - 1]，而是m[n - 1]。

最后附上python代码：

```python
class ProductOfNumbers(object):

    def __init__(self):
        self.last_zero = -1
        self.m = [1]

    def add(self, num):
        """
        :type num: int
        :rtype: None
        """
        if num == 0:
            self.last_zero = len(self.m)
            self.m.append(0)
        elif self.m[-1] == 0:
            self.m.append(num)
        else:
            self.m.append(self.m[-1] * num)

    def getProduct(self, k):
        """
        :type k: int
        :rtype: int
        """

        print len(self.m) - k

        if self.last_zero >= len(self.m) - k:
            return 0
        elif self.last_zero == len(self.m) - k - 1:
            return self.m[-1]
        else:
            return self.m[-1] / self.m[len(self.m) - k - 1]

# Your ProductOfNumbers object will be instantiated and called as such:
# obj = ProductOfNumbers()
# obj.add(num)
# param_2 = obj.getProduct(k)
```
