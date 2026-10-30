---
title: "1381. 设计一个支持增量操作的栈"
aliases: ["yiduobo的每日leetcode 1381.设计一个支持增量操作的栈"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/402189820"
zhihu_id: "402189820"
zhihu_title: "yiduobo的每日leetcode 1381.设计一个支持增量操作的栈"
question_id: "1381"
question: "设计一个支持增量操作的栈"
problem_url: "https://leetcode.cn/problems/design-a-stack-with-increment-operation/"
created: "2021-08-21T20:23:48+08:00"
updated: "2021-08-21T20:23:48+08:00"
upvotes: 0
comments: 0
---

# 1381. 设计一个支持增量操作的栈

> **[yiduobo的每日leetcode 1381.设计一个支持增量操作的栈](https://zhuanlan.zhihu.com/p/402189820) · 知乎 · 2021-08-21 · 赞同 0**
> 力扣：[1381. 设计一个支持增量操作的栈](https://leetcode.cn/problems/design-a-stack-with-increment-operation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1381.设计一个支持增量操作的栈

[力扣](https://leetcode-cn.com/problems/design-a-stack-with-increment-operation/)

题目要求弄一个栈，除了栈原本的功能之外，还需要支持一个inc操作，具体为同时对栈底的k个元素加上val这个操作。很明显，如果直接使用朴素的做法，每次都老老实实对栈底k个元素加上val的话，时间复杂度是非常高的。

注意到栈先进后出的特性，我们可以利用延迟更新来做这个inc。

使用一个数组add_list来维护inc操作中的k和val。当新来一个inc操作时，若k大于此时栈中的元素那么，那么先将k重新置为栈中元素的数目。接下来，我们就将add_list[k]加上val，表示之后我们需要将栈底的k个元素加上val。

当出现进栈操作时，我们不做任何特殊处理，而出现一个出栈操作时，我们可以先获取当前栈中元素的数目l。若此时的add_list[l]不等于，那么说明之前出现过inc操作需要将栈底的l个元素都加上add_list[l]，那么我们需要将此时的栈顶元素加上add_list[l]之后再弹出。这里需要注意的是，此时我们只是将栈底的第l个元素加上了add_list[l]，那么剩下的l - 1个元素依然需要加上add_list[l]，于是此时我们可以让add_list[l - 1]加上add_list[l]，表示需要对剩下的l - 1个元素执行inc操作，并将add_list[l]置为0即可。

这样做不会出问题的原因则是利用了栈先进后出的特性，即在栈底的l - 1个元素出栈之前，第l个元素必然是需要先出栈的，因此在第l个元素出栈时处理之前的inc操作，这些inc操作就必然能有效作用在栈底的l - 1个元素上，保证了正确性。

最后附上python代码：

```python
class CustomStack(object):

    def __init__(self, maxSize):
        """
        :type maxSize: int
        """
        self.maxSize = maxSize
        self.stack = []
        self.add_list = [0] * maxSize

    def push(self, x):
        """
        :type x: int
        :rtype: None
        """
        if len(self.stack) < self.maxSize:
            self.stack.append(x)

    def pop(self):
        """
        :rtype: int
        """
        l = len(self.stack) - 1
        if l < 0:
            return -1

        delta = self.add_list[l]
        if l > 0:
            self.add_list[l - 1] += delta
        self.add_list[l] = 0
        return self.stack.pop() + delta

    def increment(self, k, val):
        """
        :type k: int
        :type val: int
        :rtype: None
        """
        if k > len(self.stack):
            k = len(self.stack)
        if k > 0:
            self.add_list[k - 1] += val

# Your CustomStack object will be instantiated and called as such:
# obj = CustomStack(maxSize)
# obj.push(x)
# param_2 = obj.pop()
# obj.increment(k,val)
```
