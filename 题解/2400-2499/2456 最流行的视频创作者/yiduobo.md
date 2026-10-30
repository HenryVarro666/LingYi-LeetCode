---
title: "2456. 最流行的视频创作者"
aliases: ["yiduobo的每日leetcode 2456.最流行的视频创作者"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/586151900"
zhihu_id: "586151900"
zhihu_title: "yiduobo的每日leetcode 2456.最流行的视频创作者"
question_id: "2456"
question: "最流行的视频创作者"
problem_url: "https://leetcode.cn/problems/most-popular-video-creator/"
difficulty: "Medium"
created: "2022-11-23T22:52:44+08:00"
updated: "2022-11-23T22:52:44+08:00"
upvotes: 0
comments: 0
---

# 2456. 最流行的视频创作者

> **[yiduobo的每日leetcode 2456.最流行的视频创作者](https://zhuanlan.zhihu.com/p/586151900) · 知乎 · 2022-11-23 · 赞同 0**
> 力扣：[2456. 最流行的视频创作者](https://leetcode.cn/problems/most-popular-video-creator/) · Medium · 灵茶山艾府：[遍历](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2456.最流行的视频创作者

[力扣](https://leetcode.cn/problems/most-popular-video-creator/)

一趟遍历，以作者名称作为哈希表的key，利用哈希表统计每个作者所有视频流行程度之和，同时记录每个作者最受欢迎的视频的id。

接下来只需从哈希表中选出流行度最高的作者们，返回这些作者以及他们最受欢迎的视频即可。

最后附上python代码：

```python
class Solution(object):
    def mostPopularCreator(self, creators, ids, views):
        """
        :type creators: List[str]
        :type ids: List[str]
        :type views: List[int]
        :rtype: List[List[str]]
        """

        user_dict = {}
        n = len(creators)
        for index in range(n):
            name = creators[index]
            if name not in user_dict:
                user_dict[name] = [0, None]
            
            user_dict[name][0] += views[index]
            if user_dict[name][1] is None or views[user_dict[name][1]] < views[index] or (views[user_dict[name][1]] == views[index] and ids[user_dict[name][1]] > ids[index]):
                user_dict[name][1] = index
        
        res = None
        for name in user_dict:
            if res is None or user_dict[res[0]][0] < user_dict[name][0]:
                res = [name]
            elif user_dict[res[0]][0] == user_dict[name][0]:
                res.append(name)
        
        return [[x, ids[user_dict[x][1]]] for x in res]
```
