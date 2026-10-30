---
title: "1152. 用户网站访问行为分析"
aliases: ["yiduobo的每日leetcode 1152.用户网站访问行为分析"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/611158152"
zhihu_id: "611158152"
zhihu_title: "yiduobo的每日leetcode 1152.用户网站访问行为分析"
question_id: "1152"
question: "用户网站访问行为分析"
problem_url: "https://leetcode.cn/problems/analyze-user-website-visit-pattern/"
created: "2023-03-03T22:53:27+08:00"
updated: "2023-03-03T22:53:27+08:00"
upvotes: 0
comments: 0
---

# 1152. 用户网站访问行为分析

> **[yiduobo的每日leetcode 1152.用户网站访问行为分析](https://zhuanlan.zhihu.com/p/611158152) · 知乎 · 2023-03-03 · 赞同 0**
> 力扣：[1152. 用户网站访问行为分析](https://leetcode.cn/problems/analyze-user-website-visit-pattern/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1152.用户网站访问行为分析

[力扣](https://leetcode.cn/problems/analyze-user-website-visit-pattern/)

题目将按时间顺序排列的三次访问称作一种访问模式，不过需要注意的是，这里的访问模式并不要求连续，也就是说对于a->b->c->c这个访问序列而言，可以形成两组a->b->c的访问模式。

由于题目的数据规模很小，因此可以先一趟遍历，将每个用户的访问序列收集起来，接下来三重循环枚举a、b、c，并使用哈希表将所有枚举的访问模式记录下来，最后通过哈希表来找出访问频率最大的模式即可。

在具体实现上，由于题目中的访问过的网站不超过50个，因此可以使用3位的50进制来对访问模式进行编码来进行哈希。

最后附上python代码：

```python
class Solution(object):
    def mostVisitedPattern(self, username, timestamp, website):
        """
        :type username: List[str]
        :type timestamp: List[int]
        :type website: List[str]
        :rtype: List[str]
        """

        user2uid = {}
        web2wid = {}
        wid2web = {}

        user_watch = {}

        for user, t, web in zip(username, timestamp, website):
            if user not in user2uid:
                user2uid[user] = len(user2uid)
            uid = user2uid[user]
            
            if uid not in user_watch:
                user_watch[uid] = []
            
            if web not in web2wid:
                web2wid[web] = len(web2wid)
                
            wid = web2wid[web]
            wid2web[wid] = web

            user_watch[uid].append([t, wid])

        freq = {}
        for user in user_watch:
            watch_list = user_watch[user]
            watch_list.sort()
            pattern = set()
            for first in range(len(watch_list) - 2):
                for second in range(first + 1, len(watch_list) - 1):
                    for third in range(second + 1, len(watch_list)):
                        key = watch_list[first][1] * 2500 + watch_list[second][1] * 50 + watch_list[third][1]
                        pattern.add(key)
            
            for key in pattern:
                freq[key] = freq.get(key, 0) + 1
        
        res = None
        max_f = 0

        for key, f in freq.items():
            if f >= max_f:
                first_id = key / 2500
                second_id = key / 50 % 50
                third_id = key % 50
                candidate = [wid2web[first_id], wid2web[second_id], wid2web[third_id]]

                if f > max_f or candidate < res:
                    max_f = f
                    res = candidate[:]
        
        return res
```
