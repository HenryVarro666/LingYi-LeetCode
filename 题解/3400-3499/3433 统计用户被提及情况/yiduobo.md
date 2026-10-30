---
title: "3433. 统计用户被提及情况"
aliases: ["yiduobo的每日leetcode 3433.统计用户被提及情况"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/prefix-sum", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1890912712223081831"
zhihu_id: "1890912712223081831"
zhihu_title: "yiduobo的每日leetcode 3433.统计用户被提及情况"
question_id: "3433"
question: "统计用户被提及情况"
problem_url: "https://leetcode.cn/problems/count-mentions-per-user/"
difficulty: "Medium"
created: "2025-04-03T00:44:47+08:00"
updated: "2025-04-03T00:44:47+08:00"
upvotes: 0
comments: 0
---

# 3433. 统计用户被提及情况

> **[yiduobo的每日leetcode 3433.统计用户被提及情况](https://zhuanlan.zhihu.com/p/1890912712223081831) · 知乎 · 2025-04-03 · 赞同 0**
> 力扣：[3433. 统计用户被提及情况](https://leetcode.cn/problems/count-mentions-per-user/) · Medium · 灵茶山艾府：[非暴力做法：计算离线期间被提及的次数（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3433.统计用户被提及情况

[3433. 统计用户被提及情况 - 力扣（LeetCode）](https://leetcode.cn/problems/count-mentions-per-user/description/)

题目给出一个整数numberOfUsers表示用户总数，数量在1到100之间。另有一个大小为n \* 3的数组events，每个events[index]都属于下面两种类型之一：

1、消息事件\['MESSAGE', timestamp\[index\], mentions_string\[index\]\]：

表示在timestamp[index]这一时刻，有一组用户被消息提及。其中：

若mentions_string[index]为'ALL'，则表示提及所有用户；

若其为'HERE'，则表示提及所有在线用户；

否则其为一个由空格分隔，由0到numberOfUsers - 1之内的整数组成的字符串，这些整数表示被提及的用户的id，id可以重复，且可能提交离线用户。需要注意最后这种情况下，单个用户可能会被提及多次，每次提及都需要被分别统计。

2、离线事件['OFFLINE', timestamp[index], id[index]：

表示用户id[index]在时刻timestamp[index]变为离线状态，持续60个时间单位，该用户会在timestamp[index] + 60自动再次上线。保证此操作中的id[index]在当前时刻是在线的。

要求返回一个数组mentions，其中mentions[index]表示id为index的用户被提及的次数。

将所有时间按照时间戳从小到大进行排序，接下来一趟遍历，按照题目要求模拟。

为了统计每个用户被提及的次数，那么自然需要一个数组mentions。接下来：

1、对于message：

如果是here，那么就需要知道现在哪些用户在线，于是还需要一个集合online记录在线的用户。online一开始包含所有的用户，当出现离线和连回时则需要调整online，具体的处理方法在下面处理离线消息时在展开，在这里只需将online中用户对应的mentions加上1就行了

如果是all，则可以使用一个变量all_cnt记录all出现了几次，在最后再将all_cnt累加到每个用户的mentions中

如果是id组成的字符串，那么则需要分离出其中所有的id，然后依次将对应的mentions加上1

2、对于offline：

由于离线的时间统一为60，且只会作用在当前在线的用户上，那么就意味着先离线的用户必然先重新连接。于是可以使用一个队列offline记录当前离线的用户以及离线的时间。对于当前用户，将用户id和时间戳加上60加入到offline中，然后将其从集合online中移除。

为了处理连回，则需要在每个message和每个offline之前，都不断检测队首的用户是否已经连回来了，如果是，则将其从队首弹出，并重新加入到online中，然后继续检测下一个队首用户，直到队列为空或者队首用户还没有到连回的时间为止。

最后附上python代码：

```python
class Solution(object):
    def countMentions(self, numberOfUsers, events):
        """
        :type numberOfUsers: int
        :type events: List[List[str]]
        :rtype: List[int]
        """
        
        offline = deque()
        online = set([index for index in range(numberOfUsers)])
        mentions = [0] * numberOfUsers
        all_cnt = 0

        for e in sorted(events, key=lambda d:(-int(d[1]), d[0]), reverse=True):
            while offline and offline[0][0] <= int(e[1]):
                uid = offline[0][1]
                offline.popleft()
                online.add(uid)
            
            if e[0] == 'MESSAGE':
                if e[2] == 'HERE':
                    for uid in online:
                        mentions[uid] += 1
                elif e[2] == 'ALL':
                    all_cnt += 1
                else:
                    for uid in e[2].split():
                        mentions[int(uid[2:])] += 1
            
            else:
                uid = int(e[2])
                online.remove(uid)
                offline.append((int(e[1]) + 60, uid))

        for index in range(numberOfUsers):
            mentions[index] += all_cnt
        
        return mentions
```
