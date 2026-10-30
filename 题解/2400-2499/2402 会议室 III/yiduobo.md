---
title: "2402. 会议室III"
aliases: ["yiduobo的每日leetcode 2402.会议室III"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/sorting", "leetcode/simulation", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/567648312"
zhihu_id: "567648312"
zhihu_title: "yiduobo的每日leetcode 2402.会议室III"
question_id: "2402"
question: "会议室 III"
problem_url: "https://leetcode.cn/problems/meeting-rooms-iii/"
difficulty: "Hard"
rating: 2093
created: "2022-09-24T04:32:40+08:00"
updated: "2022-09-24T04:32:40+08:00"
upvotes: 0
comments: 0
---

# 2402. 会议室III

> **[yiduobo的每日leetcode 2402.会议室III](https://zhuanlan.zhihu.com/p/567648312) · 知乎 · 2022-09-24 · 赞同 0**
> 力扣：[2402. 会议室 III](https://leetcode.cn/problems/meeting-rooms-iii/) · Hard · 灵茶山艾府：[双堆模拟（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2402.会议室III

[力扣](https://leetcode.cn/problems/meeting-rooms-iii/)

比较复杂的堆模拟问题。首先分析题目给的三个条件：

1、每场会议使用未被占用的编号最小的会议室。在这里就需要使用一个堆来维护当前没有被占用的会议室，这样一来就可以高效得到其中编号最小的会议室是哪一个

2、如果没有可用的会议室，那么会议将延期，直到有空闲会议室为止。会议延期，意味着还需要使用某种数据结构来维护延期的会议，具体的放在条件三来说明。另外，会议的延期会一直到有空闲的会议室出现，这里的隐藏需求就是对于正在进行的会议，必须能高效地知道这些会议完结时间的最小值，因为最早空闲的会议室将提供给延期的会议使用。因此在这里需要使用第二个，来维护正在进行的会议的完结时间以及会议室编号

3、当会议室空闲时，将提供给原定召开时间最早的会议。那么在这里则需要使用第三个堆，来维护延期会议的原定起始时间和原定结束时间。在这里维护原定结束时间的理由时会议召开时需要通过原定的起始和结束时间计算会议具体需要花费的时间，用来更新2里面堆中维护的会议完结时间。当然，在这里也可以直接维护会议的起始时间和花费时间

综合起来，就是三个堆idle，min_time和pending，具体作用如上所述。其中idle初始化为[0, 1, ..., n - 1]，即一开始所有会议室都是空闲的，而min_time和pending则初始化为空。

接下来将会议按起始时间从小到大排序，然后一趟遍历。对于当前遍历到的会议，不妨设其开始和结束时间分别为start_time和end_time，那么：

首先，若min_time不为空，且min_time[0][0]，也就是最早完结的会议的时间小于等于start_time，那么就应该先将这些会议室释放出来。即将min_time的堆顶弹出，然后将其中对应的会议室编号重新加入到idle当中。在这里需要注意的是，每当一个会议完结，若此时pending非空，说明有延期的会议在等会议室，那么就应该立即安排pending中原定时间最早的会议在刚空出来的会议室召开，召开的时间就是上一场会议完结的时间。

这里有一个隐藏条件是pending中的会议都是被迫延期的，即pending中的会议在其原计划召开的时刻是找不到空闲会议室的，而当前刚完结的会议其完结时间必然大于原计划召开的时间，否则的话这场会议就无须pending了。也就是说，会议室空出来的时间总是大于原计划召开的时间，因此在这里召开的时间就必然是上一次会议完结的时间。记刚完结的会议其完结时间为now，在会议室num召开，那么这里就应该立刻安排pending[0]表示的会议在now时刻，num会议室召开，此时应该将pending的堆顶弹出，记为meeting_info。那么该会议的持续时间就是meeting_info[1] - meeting_info[0]，因此这场会议的完结时间就是now + meeting_info[1] - meeting_info[0]，将这个时间和会议室编号num加入到min_time中，并更新会议室num的使用次数。

接下来，若存在空闲的会议室，那么就用其中编号最小的来召开当前这场从start_time到end_time的会议，否则就将当前这场会议加入到pending中

遍历完成后，可能出现的一种情况是所有会议室都占满了，但还有会议在等待中，此时就需要等待正在进行的会议逐个完结，并在完结的时刻立即安排等待的会议召开。具体来说，就是当pending非空时：

若idle为空，即没有空闲的会议室，那么就需要等到所有正在进行的会议中结束时间最早的会议结束。记这个时间为now，那么当min_time的堆顶记录的时间恰好为now时，就将其弹出。重复此过程直到min_time为空或者堆顶记录的时间大于now为止。

接下来，就必然有了至少一个空闲的会议室，那么将其安排给pending堆顶的会议即可。

注意到题目中多次出现将idle堆顶的会议室安排给pending堆顶的会议，那么在具体实现的时候可以将这个会议开始的行为抽象出来，更进一步的，对于可以正常召开的会议，也可以先将其加入到pending中再立马将其安排在idle堆顶的会议室。

所有的会议都召开之后，返回使用次数最多的会议室即可。

最后附上python代码：

```python
class Solution(object):
    def mostBooked(self, n, meetings):
        """
        :type n: int
        :type meetings: List[List[int]]
        :rtype: int
        """

        meetings.sort(key=lambda d:d[0])
        idle = range(n)
        min_time = []
        pending = []

        def start_meeting(idle, cnt, pending, min_time, now):
            room = heapq.heappop(idle)
            cnt[room] += 1
            meeting_info = heapq.heappop(pending)
            heapq.heappush(min_time, [now + meeting_info[1] - meeting_info[0], room])

        cnt = [0] * n
        for start_time, end_time in meetings:
            while min_time and min_time[0][0] <= start_time:
                now, num = heapq.heappop(min_time)
                heapq.heappush(idle, num)
                if pending:
                    start_meeting(idle, cnt, pending, min_time, now)
            
            heapq.heappush(pending, [start_time, end_time])
            if idle:
                start_meeting(idle, cnt, pending, min_time, start_time)

        while pending:
            if not idle:
                now = min_time[0][0]
                while min_time and min_time[0][0] == now:
                    _, num = heapq.heappop(min_time)
                    heapq.heappush(idle, num)
            
            start_meeting(idle, cnt, pending, min_time, now)
        
        res = 0
        for index in range(1, n):
            if cnt[index] > cnt[res]:
                res = index
        
        return res
```
