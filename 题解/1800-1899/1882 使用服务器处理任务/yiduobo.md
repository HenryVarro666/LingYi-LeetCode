---
title: "1882. 使用服务器处理任务"
aliases: ["yiduobo的每日leetcode 1882.使用服务器处理任务"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/476787928"
zhihu_id: "476787928"
zhihu_title: "yiduobo的每日leetcode 1882.使用服务器处理任务"
question_id: "1882"
question: "使用服务器处理任务"
problem_url: "https://leetcode.cn/problems/process-tasks-using-servers/"
created: "2022-03-07T00:08:05+08:00"
updated: "2022-03-07T00:08:05+08:00"
upvotes: 0
comments: 0
---

# 1882. 使用服务器处理任务

> **[yiduobo的每日leetcode 1882.使用服务器处理任务](https://zhuanlan.zhihu.com/p/476787928) · 知乎 · 2022-03-07 · 赞同 0**
> 力扣：[1882. 使用服务器处理任务](https://leetcode.cn/problems/process-tasks-using-servers/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1882.使用服务器处理任务

[力扣](https://leetcode-cn.com/problems/process-tasks-using-servers/)

对于任务处理的顺序，题目要求优先处理下标较小的任务，因此可以一趟遍历，每次先想办法处理了当前的任务然后再继续向后处理。

而对于处理任务的服务器的选择，则需要从当前时刻空闲的服务器中选出权重最小的服务器。这也就意味着需要用堆维护当期空闲的服务器，其中堆的key是服务器的权重。

当然，这个堆并不是只出不进的，当某台服务器完成工作后，还需要返回到堆中，而每台服务器都有自己完成工作的时间，也就是说还需要使用另一个堆维护当前正在工作中的服务器，key为完成工作的时间。

除了上面的两个堆，还可能出现当前任务到达时没有空闲服务器的情况，因此还需要使用一个变量now来表示从当前时刻开始最早出现空闲服务器的时间。

那么对于一个需要处理的任务：

1、首先使用当前的时间index来更新now

2、接下来若没有空闲的服务器，则需要等待，直到最早完成工作的服务器回到空闲状态。此时就应该使用工作服务器堆顶的时间来更新now。now就是当前任务开始执行的时间。

3、接下来则需要考察now这一时刻，有多少服务器完成了工作，需要将这些服务器从工作堆中弹出并重新加入空闲堆

4、最后用空闲堆的堆顶来执行当前的任务，更新答案并将其从空闲堆中弹出，加入到工作堆中

重复上面的过程直到最后一个任务被执行。

最后附上python代码：

```python
class Solution(object):
    def assignTasks(self, servers, tasks):
        """
        :type servers: List[int]
        :type tasks: List[int]
        :rtype: List[int]
        """

        working_server = []
        idle_server = []
        for index, weight in enumerate(servers):
            heapq.heappush(idle_server, [weight, index])
        
        res = []
        now = 0
        for index, t in enumerate(tasks):
            if now < index:
                now = index
            
            if not idle_server:
                if working_server[0][0] > now:
                    now = working_server[0][0]
            
            while working_server and working_server[0][0] == now:
                _, server_id = heapq.heappop(working_server)
                heapq.heappush(idle_server, [servers[server_id], server_id])

            _, server_id = heapq.heappop(idle_server)
            res.append(server_id)
            heapq.heappush(working_server, [now + t, server_id])

        return res
```
