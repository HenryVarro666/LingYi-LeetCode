---
title: "636. 函数的独占时间"
aliases: ["yiduobo的每日leetcode 636.函数的独占时间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/270971924"
zhihu_id: "270971924"
zhihu_title: "yiduobo的每日leetcode 636.函数的独占时间"
question_id: "636"
question: "函数的独占时间"
problem_url: "https://leetcode.cn/problems/exclusive-time-of-functions/"
created: "2020-11-01T15:55:25+08:00"
updated: "2020-11-01T15:55:25+08:00"
upvotes: 1
comments: 0
---

# 636. 函数的独占时间

> **[yiduobo的每日leetcode 636.函数的独占时间](https://zhuanlan.zhihu.com/p/270971924) · 知乎 · 2020-11-01 · 赞同 1**
> 力扣：[636. 函数的独占时间](https://leetcode.cn/problems/exclusive-time-of-functions/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

636.函数的独占时间

[力扣](https://leetcode-cn.com/problems/exclusive-time-of-functions/)

按题目要求用栈来模拟运行过程，使用两个变量now和last_time分别记录当前正在运行函数的fid以及起始运行时间，初始状态下当前没有正在执行的函数，起始时间为空：

当遇到start时，若now不为空，说明有正在运行的函数，此时应该计算now运行的时间，将其加入到now的独占时间当中，然后将now压入栈中。由于有新的start出现，那么此时的now就应该是新来的函数，同时应该重置起始时间。

当遇到end时，说明now的运行暂时告一段落，此时应该计算now运行的时间，将其加入到now的独占时间当中。若栈不为空，说明now是被栈顶函数调用的，因此当now结束后，应该回到栈顶的函数，同时应该重置起始时间。若栈为空，那么在now执行完之后没有函数再执行，因此now应该置为空，同时起始时间也置为空。

最后附上python代码：

```python
class Solution(object):
    def exclusiveTime(self, n, logs):
        """
        :type n: int
        :type logs: List[str]
        :rtype: List[int]
        """

        res = [0] * n
        stack = []
        now = None
        last_time = None
        for log in logs:
            fid, status, time = log.split(':')
            fid = int(fid)
            time = int(time)
            if status == 'start':
                if now is not None:
                    res[now] += time - last_time
                    stack.append(now)
                now = fid
                last_time = time
            else:
                res[now] += time - last_time + 1
                if stack:
                    now = stack.pop()
                    last_time = time + 1
                else:
                    now = None
                    last_time = None

        return res
```
