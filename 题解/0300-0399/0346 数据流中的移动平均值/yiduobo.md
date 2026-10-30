---
title: "346. 数据流中的移动平均值"
aliases: ["yiduobo的每日leetcode 346.数据流中的移动平均值"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/596942093"
zhihu_id: "596942093"
zhihu_title: "yiduobo的每日leetcode 346.数据流中的移动平均值"
question_id: "346"
question: "数据流中的移动平均值"
problem_url: "https://leetcode.cn/problems/moving-average-from-data-stream/"
created: "2023-01-06T02:43:20+08:00"
updated: "2023-01-06T02:43:20+08:00"
upvotes: 0
comments: 0
---

# 346. 数据流中的移动平均值

> **[yiduobo的每日leetcode 346.数据流中的移动平均值](https://zhuanlan.zhihu.com/p/596942093) · 知乎 · 2023-01-06 · 赞同 0**
> 力扣：[346. 数据流中的移动平均值](https://leetcode.cn/problems/moving-average-from-data-stream/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

346.数据流中的移动平均值

[力扣](https://leetcode.cn/problems/moving-average-from-data-stream/)

使用一个容量为k的队列维护这个数据流，同时使用一个变量s记录当前队列中数值的总和。当next操作出现时，首先判断当前队列是否已满。若当前队列满了，那么就将队首元素弹出，同时更新s。接下来，将新来的数加入到队列的末尾并更新s，然后通过s和队列中元素的数目就可以计算平均值了。

最后附上python代码：

```python
import Queue

class MovingAverage(object):

    def __init__(self, size):
        """
        :type size: int
        """
        self.q = Queue.Queue(size)
        self.s = 0

    def next(self, val):
        """
        :type val: int
        :rtype: float
        """
        if self.q.full():
            self.s -= self.q.get()
        self.q.put(val)
        self.s += val
        
        return self.s * 1.0 / self.q.qsize()

# Your MovingAverage object will be instantiated and called as such:
# obj = MovingAverage(size)
# param_1 = obj.next(val)
```
