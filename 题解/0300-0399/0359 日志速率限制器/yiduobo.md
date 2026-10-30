---
title: "359. 日志速率限制器"
aliases: ["yiduobo的每日leetcode 359.日志速率限制器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/597516254"
zhihu_id: "597516254"
zhihu_title: "yiduobo的每日leetcode 359.日志速率限制器"
question_id: "359"
question: "日志速率限制器"
problem_url: "https://leetcode.cn/problems/logger-rate-limiter/"
created: "2023-01-08T18:35:08+08:00"
updated: "2023-01-08T18:35:08+08:00"
upvotes: 0
comments: 0
---

# 359. 日志速率限制器

> **[yiduobo的每日leetcode 359.日志速率限制器](https://zhuanlan.zhihu.com/p/597516254) · 知乎 · 2023-01-08 · 赞同 0**
> 力扣：[359. 日志速率限制器](https://leetcode.cn/problems/logger-rate-limiter/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

359.日志速率限制器

[力扣](https://leetcode.cn/problems/logger-rate-limiter/)

与之前的346题很像，同样是利用队列处理数据流的问题。

对于本题，使用队列记录日志以及其对应的时间戳。当一条新的日志到达时，先通过当前日志的时间戳减去10，将队列中过期的日志和时间戳弹出。接下来，若当前日志依然存在于队列中，那么就返回false，否则将当前日志和时间戳加入到队列中。

为了高效判断日志是否出现在队列中，则还需要使用一个集合来储存当前位于队列中的日志，这个集合需要随着日志的进出队列进行同步维护。

最后附上python代码：

```python
class Logger(object):

    def __init__(self):
        self.head = self.tail = 0
        self.q = []
        self.used = set()

    def shouldPrintMessage(self, timestamp, message):
        """
        :type timestamp: int
        :type message: str
        :rtype: bool
        """
        while self.head < self.tail and timestamp - self.q[self.head][0] >= 10:
            self.used.remove(self.q[self.head][1])
            self.head += 1
        
        if message in self.used:
            return False
        
        self.used.add(message)
        self.q.append([timestamp, message])
        self.tail += 1
        return True

# Your Logger object will be instantiated and called as such:
# obj = Logger()
# param_1 = obj.shouldPrintMessage(timestamp,message)
```
