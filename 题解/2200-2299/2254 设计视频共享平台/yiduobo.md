---
title: "2254. 设计视频共享平台"
aliases: ["yiduobo的每日leetcode 2254.设计视频共享平台"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/628735352"
zhihu_id: "628735352"
zhihu_title: "yiduobo的每日leetcode 2254.设计视频共享平台"
question_id: "2254"
question: "设计视频共享平台"
problem_url: "https://leetcode.cn/problems/design-video-sharing-platform/"
created: "2023-05-12T00:19:44+08:00"
updated: "2023-05-12T00:19:44+08:00"
upvotes: 0
comments: 0
---

# 2254. 设计视频共享平台

> **[yiduobo的每日leetcode 2254.设计视频共享平台](https://zhuanlan.zhihu.com/p/628735352) · 知乎 · 2023-05-12 · 赞同 0**
> 力扣：[2254. 设计视频共享平台](https://leetcode.cn/problems/design-video-sharing-platform/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2254.设计视频共享平台

[力扣](https://leetcode.cn/problems/design-video-sharing-platform/)

题目描述看上去一大堆，但是抽象出来可以分成两大类需求：

1、视频的增删。对于新增视频，需要找出当前未使用的最小自然数作为视频id，将这个视频与这个自然数关联起来。而对于删除，则只需解出这个关联。

2、对视频的行为，包括观看、点赞、点踩、获取观看次数、获取点赞和点踩次数。

对于第一类操作，建立关联自然是使用哈希表，而找出最小未使用的自然数则可以利用堆来解决。使用一个堆来储存之前被使用过，但目前已经限制的id，同时使用一个变量记录下一个从未使用过的自然数。

对于新增操作，首先检查堆是否为空，若不为空，那么堆顶数字就是当前未使用的最小自然数，否则就应该选择下一个从未使用过的自然数。接下来只需以这个自然数为key，视频为value加入到哈希表中即可。

对于删除操作，则需要将对应的id重新加入到堆中，然后将其从哈希表中删除。

对于第二类操作，则可以简单构造一个video类，其中包含视频内容、播放量、点赞数以及点踩数。接下来对于观看、点赞以及点踩操作，只需更新对应的成员变量，而对于获取次数的操作则只需返回对应的成员变量值即可。

最后附上python代码：

```python
class Video(object):

    def __init__(self, content):
        self.content = content
        self.content_len = len(content)
        self.views = 0
        self.likes = 0
        self.dislikes = 0

class VideoSharingPlatform(object):

    def __init__(self):
        self.next_id = 0
        self.idle_id = []
        self.videos = {}

    def upload(self, video):
        """
        :type video: str
        :rtype: int
        """
        if self.idle_id:
            id = heapq.heappop(self.idle_id)
        else:
            id = self.next_id
            self.next_id += 1
        
        self.videos[id] = Video(video)
        return id

    def remove(self, videoId):
        """
        :type videoId: int
        :rtype: None
        """
        if videoId in self.videos:
            self.videos.pop(videoId)
            heapq.heappush(self.idle_id, videoId)

    def watch(self, videoId, startMinute, endMinute):
        """
        :type videoId: int
        :type startMinute: int
        :type endMinute: int
        :rtype: str
        """
        if videoId not in self.videos:
            return "-1"
        
        video = self.videos[videoId]
        video.views += 1
        return video.content[startMinute : min(endMinute + 1, video.content_len)]

    def like(self, videoId):
        """
        :type videoId: int
        :rtype: None
        """
        if videoId not in self.videos:
            return -1
        
        video = self.videos[videoId]
        video.likes += 1

    def dislike(self, videoId):
        """
        :type videoId: int
        :rtype: None
        """
        if videoId not in self.videos:
            return -1
        
        video = self.videos[videoId]
        video.dislikes += 1

    def getLikesAndDislikes(self, videoId):
        """
        :type videoId: int
        :rtype: List[int]
        """
        if videoId not in self.videos:
            return [-1]
        
        video = self.videos[videoId]
        return [video.likes, video.dislikes]

    def getViews(self, videoId):
        """
        :type videoId: int
        :rtype: int
        """

        if videoId not in self.videos:
            return -1
        
        video = self.videos[videoId]
        return video.views

# Your VideoSharingPlatform object will be instantiated and called as such:
# obj = VideoSharingPlatform()
# param_1 = obj.upload(video)
# obj.remove(videoId)
# param_3 = obj.watch(videoId,startMinute,endMinute)
# obj.like(videoId)
# obj.dislike(videoId)
# param_6 = obj.getLikesAndDislikes(videoId)
# param_7 = obj.getViews(videoId)
```
