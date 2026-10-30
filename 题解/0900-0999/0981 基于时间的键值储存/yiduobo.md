---
title: "981. 基于时间的键值储存"
aliases: ["yiduobo的每日leetcode 981.基于时间的键值储存"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/363369726"
zhihu_id: "363369726"
zhihu_title: "yiduobo的每日leetcode 981.基于时间的键值储存"
question_id: "981"
question: "基于时间的键值储存"
problem_url: "https://leetcode.cn/problems/time-based-key-value-store/"
created: "2021-04-08T23:33:07+08:00"
updated: "2021-04-08T23:33:07+08:00"
upvotes: 0
comments: 0
---

# 981. 基于时间的键值储存

> **[yiduobo的每日leetcode 981.基于时间的键值储存](https://zhuanlan.zhihu.com/p/363369726) · 知乎 · 2021-04-08 · 赞同 0**
> 力扣：[981. 基于时间的键值储存](https://leetcode.cn/problems/time-based-key-value-store/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

981.基于时间的键值储存

[力扣](https://leetcode-cn.com/problems/time-based-key-value-store/)

根据题意我们需要将每个key在每个时间点上的值都保存下来。注意到每次查询都是通过key来查询，因此可以使用一个dict来储存每个key的时间戳列表。又注意到时间戳单调递增，那么可以之间使用一个list来储存key对应的时间戳，然后在查询时就可以通过二分查找key对应的时间戳列表来迅速找到答案。

最后附上python代码：

```python
class TimeMap(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.kt = {}
        self.kv = {}

    def set(self, key, value, timestamp):
        """
        :type key: str
        :type value: str
        :type timestamp: int
        :rtype: None
        """
        if key not in self.kt:
            self.kt[key] = []
            self.kv[key] = []
        
        self.kt[key].append(timestamp)
        self.kv[key].append(value)

    def get(self, key, timestamp):
        """
        :type key: str
        :type timestamp: int
        :rtype: str
        """
        if key not in self.kt:
            return ""
        
        if timestamp < self.kt[key][0]:
            return ""
        
        if timestamp >= self.kt[key][-1]:
            return self.kv[key][-1]
        
        l = 0
        r = len(self.kt[key])
        while l < r:
            mid = (l + r) >> 1
            if self.kt[key][mid] < timestamp:
                l = mid + 1
            else:
                r = mid
            
        if self.kt[key][l] == timestamp:
            return self.kv[key][l]
        else:
            return self.kv[key][l - 1]
                

# Your TimeMap object will be instantiated and called as such:
# obj = TimeMap()
# obj.set(key,value,timestamp)
# param_2 = obj.get(key,timestamp)
```
