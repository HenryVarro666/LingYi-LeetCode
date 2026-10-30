---
title: "1311. 获取你好友已观看的视频"
aliases: ["yiduobo的每日leetcode 1311.获取你好友已观看的视频"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/392281640"
zhihu_id: "392281640"
zhihu_title: "yiduobo的每日leetcode 1311.获取你好友已观看的视频"
question_id: "1311"
question: "获取你好友已观看的视频"
problem_url: "https://leetcode.cn/problems/get-watched-videos-by-your-friends/"
created: "2021-07-22T22:56:01+08:00"
updated: "2021-07-22T22:56:01+08:00"
upvotes: 0
comments: 0
---

# 1311. 获取你好友已观看的视频

> **[yiduobo的每日leetcode 1311.获取你好友已观看的视频](https://zhuanlan.zhihu.com/p/392281640) · 知乎 · 2021-07-22 · 赞同 0**
> 力扣：[1311. 获取你好友已观看的视频](https://leetcode.cn/problems/get-watched-videos-by-your-friends/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1311.获取你好友已观看的视频

[力扣](https://leetcode-cn.com/problems/get-watched-videos-by-your-friends/)

根据题目的提示，我们可以将每个人看做图中的一个点，而两个人之间若存在朋友关系，我们就在这两个人中间连上一条边，这样一来，问题就转化成了求与id最短距离为level的所有节点看过的视频以及对应的次数。

于是我们可以从id开始进行bfs，每一轮都将当前这样一轮处理的人所有未访问过的好友加入到bfs队列中，那么第level轮处理的人所观看的视频就是要求的答案。于是我们可以在处理到这一轮时，使用一个dict来储存这些视频以及观看的次数，那么处理完这一轮后，将dict按频率和字母从小到大排序后输出即可。

最后附上python代码：

```python
class Solution(object):
    def watchedVideosByFriends(self, watchedVideos, friends, id, level):
        """
        :type watchedVideos: List[List[str]]
        :type friends: List[List[int]]
        :type id: int
        :type level: int
        :rtype: List[str]
        """

        n = len(watchedVideos)
        used = [False] * n
        q = [id]
        used[id] = True
        l = 0
        r = 1
        step = 0
        cnt_dict = {}
        while l < r and step < level:
            step += 1
            for now in q[l : r]:
                for f in friends[now]:
                    if not used[f]:
                        q.append(f)
                        used[f] = True
                        if step == level:
                            for v in watchedVideos[f]:
                                cnt_dict[v] = cnt_dict.get(v, 0) + 1
            
            l, r = r, len(q)

        return [x[0] for x in sorted(cnt_dict.items(), key=lambda d:(d[1], d[0]))]
```
