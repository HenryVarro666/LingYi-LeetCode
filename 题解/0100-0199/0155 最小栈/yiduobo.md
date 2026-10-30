---
title: "155. 最小栈"
aliases: ["yiduobo的每日leetcode 155.最小栈"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "题单/常用数据结构", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/常用数据结构/三-栈", "题单/LeetCode-热题-100/栈", "题单/面试经典-150-题/栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/143778380"
zhihu_id: "143778380"
zhihu_title: "yiduobo的每日leetcode 155.最小栈"
question_id: "155"
question: "最小栈"
problem_url: "https://leetcode.cn/problems/min-stack/"
difficulty: "Medium"
created: "2020-05-26T20:03:25+08:00"
updated: "2020-05-26T20:03:25+08:00"
upvotes: 1
comments: 0
---

# 155. 最小栈

> **[yiduobo的每日leetcode 155.最小栈](https://zhuanlan.zhihu.com/p/143778380) · 知乎 · 2020-05-26 · 赞同 1**
> 力扣：[155. 最小栈](https://leetcode.cn/problems/min-stack/) · Medium · 灵茶山艾府：[两种方法：保存前缀最小值 / 保存差值，不用辅助栈（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

155.最小栈<https://leetcode-cn.com/problems/min-stack/>

栈操作的题目。对于push，pop和top三种操作，就按栈的常规操作即可，这里主要是要解决在常数时间内求最小值。

一个自然的想法是使用一个变量维护当前栈的最小值，然后每次当新的数入栈时，更新这个最小值。但是这样做有一个问题，当栈pop掉最小值时，这个最小值无法更新。于是可以想办法维护住每个数入栈时的最小值，即加入另一个栈min_stack，每次当有数push进入stack时，将当前的最小值push到min_stack中；当有数从stack顶pop出来时，将min_stack的顶也pop掉即可。

最后附上python代码：

```python
class MinStack(object):

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.stack = []
        self.min_stack = []

    def push(self, x):
        """
        :type x: int
        :rtype: None
        """
        if not self.min_stack or self.min_stack[-1] > x:
            self.min_stack.append(x)
        else:
            self.min_stack.append(self.min_stack[-1])
        self.stack.append(x)

    def pop(self):
        """
        :rtype: None
        """
        self.min_stack.pop()
        return self.stack.pop()

    def top(self):
        """
        :rtype: int
        """
        return self.stack[-1]

    def getMin(self):
        """
        :rtype: int
        """
        return self.min_stack[-1]

# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(x)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
```
