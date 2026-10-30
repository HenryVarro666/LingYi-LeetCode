---
title: "933. 最近的请求次数"
aliases: ["yiduobo的每日leetcode 933.最近的请求次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/357358595"
zhihu_id: "357358595"
zhihu_title: "yiduobo的每日leetcode 933.最近的请求次数"
question_id: "933"
question: "最近的请求次数"
problem_url: "https://leetcode.cn/problems/number-of-recent-calls/"
created: "2021-03-15T22:38:36+08:00"
updated: "2021-03-15T22:38:36+08:00"
upvotes: 1
comments: 0
---

# 933. 最近的请求次数

> **[yiduobo的每日leetcode 933.最近的请求次数](https://zhuanlan.zhihu.com/p/357358595) · 知乎 · 2021-03-15 · 赞同 1**
> 力扣：[933. 最近的请求次数](https://leetcode.cn/problems/number-of-recent-calls/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

933.最近的请求次数

[力扣](https://leetcode-cn.com/problems/number-of-recent-calls/)

题目要求找到最近3000ms的请求次数。由于请求是按时间顺序排好过来的，因此我们可以使用一个数组将这些时间节点储存起来，同时维护一个滑动窗口，其右边界为当前时间节点，而左边界则根据3000ms来进行更新。

每新来一个时间节点，则通过移动窗口左边界将窗口内距离当前时间点超过3000ms的节点移出窗口，然后当前窗口的大小即可。

最后附上python代码：

```python
class RecentCounter(object):

    def __init__(self):
        self.q = []
        self.l = 0

    def ping(self, t):
        """
        :type t: int
        :rtype: int
        """
        self.q.append(t)
        while self.l < len(self.q) and self.q[self.l] < t - 3000:
            self.l += 1
        
        return len(self.q) - self.l

# Your RecentCounter object will be instantiated and called as such:
# obj = RecentCounter()
# param_1 = obj.ping(t)
```
