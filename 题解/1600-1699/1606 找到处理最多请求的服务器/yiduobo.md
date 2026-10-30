---
title: "1606. 找到处理最多请求的服务器"
aliases: ["yiduobo的每日leetcode 1606.找到处理最多请求的服务器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/434122558"
zhihu_id: "434122558"
zhihu_title: "yiduobo的每日leetcode 1606.找到处理最多请求的服务器"
question_id: "1606"
question: "找到处理最多请求的服务器"
problem_url: "https://leetcode.cn/problems/find-servers-that-handled-most-number-of-requests/"
created: "2021-11-17T00:07:13+08:00"
updated: "2021-11-17T00:07:13+08:00"
upvotes: 1
comments: 0
---

# 1606. 找到处理最多请求的服务器

> **[yiduobo的每日leetcode 1606.找到处理最多请求的服务器](https://zhuanlan.zhihu.com/p/434122558) · 知乎 · 2021-11-17 · 赞同 1**
> 力扣：[1606. 找到处理最多请求的服务器](https://leetcode.cn/problems/find-servers-that-handled-most-number-of-requests/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1606.找到处理最多请求的服务器

[力扣](https://leetcode-cn.com/problems/find-servers-that-handled-most-number-of-requests/)

对于题目中arrival每一轮的请求来说，都需要做两件事情：

1、把已经完成工作的服务器从working状态变为pending状态：

对于当前请求到达的时间arrival[index]而言，需要找出之前有哪些请求执行结束的时间小于等于这个arrival[index]，那么一个自然的想法就是维护一个小根堆，堆中记录所有处于working状态的服务器以及其处理完请求的时间，以这个时间为key。当一个请求过来时，只需比较当前堆顶的时间是否小于等于请求到达的时间，若小于等于，说明堆顶对应的服务器已经处理完了对应的请求，需要将其回归到pending状态，因此需要将其从堆中弹出。重复此过程直到堆为空或者堆顶对应的时间大于请求到达的时间为止。

2、从所有pending状态的服务器当中选择一台符合要求的执行当前的请求，即将其从pending状态变为working状态：

这个选择的过程实际上可以看做两个部分。对于第index个请求，其第一目标的服务器target为index % k这一台，那么第一个部分就是查询target到k - 1之间的这些机器中编号最小的处于pending状态的机器。若找到了，那么这就是这一次请求使用的机器，否则需要进行第二部分的查询，也就是0到target - 1之间的这些机器中编号最小的处于pending状态的机器。

可以发现，这是两个区间最小值问题，可以使用线段树平衡树之类的数据结构来解决。另外，由于这两个区间的边界实际上是随着index在循环移动的，因此使用两个小根堆并不断维护边界也是可行的做法。

当然，也存在更简洁的做法。这里需要两个区间最小值的原因是对于当前目标机器target而言，可能存在0到target - 1之间，因为上一次请求完成而回归到pending队列中的机器。对于这些机器而言，可以发现其下一次使用的时期取决于其回归的时间节点。对于一台编号为p的机器而言，若其回归时这一轮的目标机器target的编号满足p \< target，那么说明p只有等到target到k - 1之间所有pending的机器都被用掉才有可能通过第二部分的查询被选中，换言之，如果将从0开始到k - 1这些机器全部使用一遍视为一轮的话，那么对于p \< target的机器而言，就必须等到target的下一轮了，那么就可以在p回归时对其进行处理。

若p \< target，其将被排到下一轮。当前轮次为index / k，那么下一轮就是index / k + 1，因此p在下一轮的编号就是p + (index / k + 1) \* k

若p >\= target，那么p下一次使用就会是target这一轮，因此p的编号就是p + index / k \* k

进行上面的处理之后，就只需从pending状态的机器中选出编号最小的那一台执行请求了，这里同样是使用一个小根堆，维护所有机器的轮次编号即可。

最后附上python代码：

```python
class Solution(object):
    def busiestServers(self, k, arrival, load):
        """
        :type k: int
        :type arrival: List[int]
        :type load: List[int]
        :rtype: List[int]
        """

        n = len(arrival)
        working = []
        pending = range(k)
        cnt = [0] * k

        for index, t in enumerate(arrival):
            target = index % k
            while working and working[0][0] <= t:
                num = working[0][1]
                if num < target:
                    num += (index / k + 1) * k
                else:
                    num += index / k * k 
                
                heapq.heappush(pending, num)
                heapq.heappop(working)

            if pending:
                choose = heapq.heappop(pending)
                cnt[choose % k] += 1
                heapq.heappush(working, [t + load[index], choose % k])

        res = [0]
        for index in range(1, k):
            if cnt[index] > cnt[res[0]]:
                res = [index]
            elif cnt[index] == cnt[res[0]]:
                res.append(index)
        
        return res
```
