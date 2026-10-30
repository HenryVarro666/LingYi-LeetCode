---
title: "1348. 推文计数"
aliases: ["yiduobo的每日leetcode 1348.推文计数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/397323690"
zhihu_id: "397323690"
zhihu_title: "yiduobo的每日leetcode 1348.推文计数"
question_id: "1348"
question: "推文计数"
problem_url: "https://leetcode.cn/problems/tweet-counts-per-frequency/"
created: "2021-08-07T15:00:53+08:00"
updated: "2021-08-07T15:00:53+08:00"
upvotes: 0
comments: 0
---

# 1348. 推文计数

> **[yiduobo的每日leetcode 1348.推文计数](https://zhuanlan.zhihu.com/p/397323690) · 知乎 · 2021-08-07 · 赞同 0**
> 力扣：[1348. 推文计数](https://leetcode.cn/problems/tweet-counts-per-frequency/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1348.推文计数

[力扣](https://leetcode-cn.com/problems/tweet-counts-per-frequency/)

首先，对于每个不同的tweetName，我们都应该储存这个tweetName发出的推文。题目要求找出一个时间段内的推文数目，那么这里主要就是考察如何高效储存并读取推文。高级一点的做法应该是以时间为key，使用平衡二叉树来储存。我在这里采用的低配的做法，即按时间从小到大储存一个list。

对于一条新推文，我们先在list中进行二分，找出这条新推文应该插入的位置，然后将其插入到list当中。

对于一个请求，我们则在list中二分请求的startTime和endTime，找出其在list中对应的子数组，然后按给出的时间粒度计数。

最后附上python代码：

```python
class TweetCounts(object):

    def __init__(self):
        self.time_dict = {}

    def bSearch(self, tweetName, time):
        l = 0
        r = len(self.time_dict[tweetName])
        while l < r:
            mid = (l + r) / 2
            if self.time_dict[tweetName][mid][0] < time:
                l = mid + 1
            else:
                r = mid
        
        return l

    def recordTweet(self, tweetName, time):
        """
        :type tweetName: str
        :type time: int
        :rtype: None
        """
        if tweetName not in self.time_dict:
            self.time_dict[tweetName] = [[time, 1]]
        else:
            if time > self.time_dict[tweetName][-1][0]:
                self.time_dict[tweetName].append([time, 1])
            elif time < self.time_dict[tweetName][0][0]:
                self.time_dict[tweetName] = [[time, 1]]+ self.time_dict[tweetName]
            else:
                p = self.bSearch(tweetName, time)
                
                if self.time_dict[tweetName][p][0] == time:
                    self.time_dict[tweetName][p][1] += 1
                else:
                    self.time_dict[tweetName] = self.time_dict[tweetName][:p] + [[time, 1]] + self.time_dict[tweetName][p:]

    def getTweetCountsPerFrequency(self, freq, tweetName, startTime, endTime):
        """
        :type freq: str
        :type tweetName: str
        :type startTime: int
        :type endTime: int
        :rtype: List[int]
        """
        delta = endTime - startTime + 1
        if freq == 'minute':
            freq = 60
        elif freq == 'hour':
            freq = 3600
        else:
            freq = 86400

        n = delta / freq
        if delta % freq != 0:
            n += 1
        res = [0] * n

        if startTime > endTime:
            return res
        
        if tweetName not in self.time_dict:
            return res

        if startTime > self.time_dict[tweetName][-1][0] or endTime < self.time_dict[tweetName][0][0]:
            return res
        
        if startTime <= self.time_dict[tweetName][0][0]:
            left = 0
        else:
            left = self.bSearch(tweetName, startTime)
        
        if endTime >= self.time_dict[tweetName][-1][0]:
            right = len(self.time_dict[tweetName])
        else:
            right = self.bSearch(tweetName, endTime)

        for index in range(left, right):
            delta = self.time_dict[tweetName][index][0] - startTime
            p = delta / freq
            res[p] += self.time_dict[tweetName][index][1]
        
        return res
            

# Your TweetCounts object will be instantiated and called as such:
# obj = TweetCounts()
# obj.recordTweet(tweetName,time)
# param_2 = obj.getTweetCountsPerFrequency(freq,tweetName,startTime,endTime)
```
