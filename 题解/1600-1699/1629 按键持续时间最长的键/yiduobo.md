---
title: "1629. 按键持续时间最长的键"
aliases: ["yiduobo的每日leetcode 1629.按键持续时间最长的键"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/437403606"
zhihu_id: "437403606"
zhihu_title: "yiduobo的每日leetcode 1629.按键持续时间最长的键"
question_id: "1629"
question: "按键持续时间最长的键"
problem_url: "https://leetcode.cn/problems/slowest-key/"
created: "2021-11-24T23:45:26+08:00"
updated: "2021-11-24T23:45:26+08:00"
upvotes: 0
comments: 0
---

# 1629. 按键持续时间最长的键

> **[yiduobo的每日leetcode 1629.按键持续时间最长的键](https://zhuanlan.zhihu.com/p/437403606) · 知乎 · 2021-11-24 · 赞同 0**
> 力扣：[1629. 按键持续时间最长的键](https://leetcode.cn/problems/slowest-key/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1629.按键持续时间最长的键

[力扣](https://leetcode-cn.com/problems/slowest-key/)

比较基础的题目。初始化答案为第0个键，并记录当前最长持续时间为第0个键的松开时间，然后从第1个键开始向后扫描，每次计算当前键松开时间与上一个键松开时间的差值，根据这个差值与当前最长持续时间的大小来更新答案以及当前最长持续时间即可。

最后附上python代码：

```python
class Solution(object):
    def slowestKey(self, releaseTimes, keysPressed):
        """
        :type releaseTimes: List[int]
        :type keysPressed: str
        :rtype: str
        """

        res = keysPressed[0]
        max_time = releaseTimes[0]
        for index in range(1, len(releaseTimes)):
            delta_time = releaseTimes[index] - releaseTimes[index - 1]
            if delta_time > max_time or (delta_time == max_time and keysPressed[index] > res):
                max_time = delta_time
                res = keysPressed[index]
        
        return res
```
