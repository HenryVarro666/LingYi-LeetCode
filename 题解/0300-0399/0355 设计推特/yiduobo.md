---
title: "355. 设计推特"
aliases: ["yiduobo的每日leetcode 355.设计推特"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/163793827"
zhihu_id: "163793827"
zhihu_title: "yiduobo的每日leetcode 355.设计推特"
question_id: "355"
question: "设计推特"
problem_url: "https://leetcode.cn/problems/design-twitter/"
created: "2020-07-26T15:22:38+08:00"
updated: "2020-07-26T15:22:39+08:00"
upvotes: 0
comments: 0
---

# 355. 设计推特

> **[yiduobo的每日leetcode 355.设计推特](https://zhuanlan.zhihu.com/p/163793827) · 知乎 · 2020-07-26 · 赞同 0**
> 力扣：[355. 设计推特](https://leetcode.cn/problems/design-twitter/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

355.设计推特<https://leetcode-cn.com/problems/design-twitter/>

对于这里面的几种功能，可以这样来进行分析：

1、发送推文。由于题目没有删除推文的操作，因此可以使用某种线性的数据结构来储存每个用户发出的推文内容。同时注意到推文需要按时间顺序从近到远排序，因此自然而然就想到使用栈来维护每个用户发过的推文。另外，由于题目只要求用户每次能刷到十条推文，因此对于每个用户实际上只需要保留最近的十条推文，因此使用栈底可移动的栈是最好的。不过我没找到现成的，因此也可以维护首尾元素的下标，通过循环队列的方式在数组中模拟这个“循环栈”。我在这里是直接使用的list来作为栈使用。另外，由于之后的检索需要知道发推的时间，因此需要将发推时间连通推文内容一并保存起来。这一步的时间复杂度为O(1)。

2、检索推文。这一步相当于对用户自身以及其关注的人，以发推时间为key，进行十次多路归并。对于多路归并问题，使用堆来处理是经典的做法。这一步的时间复杂度为O(10logk)，其中k表示用户关注人的数量。

3、关注用户与取关用户。这里直接使用set来记录已关注列表即可。这一步的时间复杂度也是O(1)。

另外，需要注意一些细节，例如检索推文时需要带上自己发过的推文，以及取关用户时可能之前并未关注过对应的用户等。

最后附上python代码：

```python
import heapq

class Twitter(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.tweet_dict = {}
        self.time_cnt = 0 
        self.follow_dict = {}

    def postTweet(self, userId, tweetId):
        """
        Compose a new tweet.
        :type userId: int
        :type tweetId: int
        :rtype: None
        """
        if userId not in self.tweet_dict:
            self.tweet_dict[userId] = []
        
        self.tweet_dict[userId].append([-self.time_cnt, tweetId])

        self.time_cnt += 1

    def getNewsFeed(self, userId):
        """
        Retrieve the 10 most recent tweet ids in the user's news feed. Each item in the news feed must be posted by users who the user followed or by the user herself. Tweets must be ordered from most recent to least recent.
        :type userId: int
        :rtype: List[int]
        """

        merge_id_list = []
        pos_list = []
        heap = []
        target_set = self.follow_dict.get(userId, set())
        target_set.add(userId)
        for followee in target_set:
            if followee in self.tweet_dict:
                merge_id_list.append(followee)
                heap.append(self.tweet_dict[followee][-1] + [len(merge_id_list) - 1])
                pos_list.append(len(self.tweet_dict[followee]) - 2)

        heapq.heapify(heap)
        
        res = []
        while len(res) < 10 and heap:
            author_time, tweetId, fromId = heapq.heappop(heap)
            res.append(tweetId)
            if pos_list[fromId] >= 0:
                heapq.heappush(heap, self.tweet_dict[merge_id_list[fromId]][pos_list[fromId]] + [fromId])
                pos_list[fromId] -= 1
        return res

    def follow(self, followerId, followeeId):
        """
        Follower follows a followee. If the operation is invalid, it should be a no-op.
        :type followerId: int
        :type followeeId: int
        :rtype: None
        """
        if followerId not in self.follow_dict:
            self.follow_dict[followerId] = set()
        self.follow_dict[followerId].add(followeeId)

    def unfollow(self, followerId, followeeId):
        """
        Follower unfollows a followee. If the operation is invalid, it should be a no-op.
        :type followerId: int
        :type followeeId: int
        :rtype: None
        """
        if followeeId in self.follow_dict.get(followerId, set()):
            self.follow_dict[followerId].remove(followeeId)

# Your Twitter object will be instantiated and called as such:
# obj = Twitter()
# obj.postTweet(userId,tweetId)
# param_2 = obj.getNewsFeed(userId)
# obj.follow(followerId,followeeId)
# obj.unfollow(followerId,followeeId)
```
