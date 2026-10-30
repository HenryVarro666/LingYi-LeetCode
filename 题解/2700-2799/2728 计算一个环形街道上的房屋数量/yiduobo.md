---
title: "2728. 计算一个环形街道上的房屋数量"
aliases: ["yiduobo的每日leetcode 2728.计算一个环形街道上的房屋数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/652182593"
zhihu_id: "652182593"
zhihu_title: "yiduobo的每日leetcode 2728.计算一个环形街道上的房屋数量"
question_id: "2728"
question: "计算一个环形街道上的房屋数量"
problem_url: "https://leetcode.cn/problems/count-houses-in-a-circular-street/"
created: "2023-08-24T22:13:48+08:00"
updated: "2023-08-24T22:13:48+08:00"
upvotes: 0
comments: 0
---

# 2728. 计算一个环形街道上的房屋数量

> **[yiduobo的每日leetcode 2728.计算一个环形街道上的房屋数量](https://zhuanlan.zhihu.com/p/652182593) · 知乎 · 2023-08-24 · 赞同 0**
> 力扣：[2728. 计算一个环形街道上的房屋数量](https://leetcode.cn/problems/count-houses-in-a-circular-street/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2718.计算一个环形街道上的房屋数量

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/count-houses-in-a-circular-street/)

由于街道上的房屋数量不超过k，那么可以先向右移动k轮，并将过程中所有开着的房门都关上。这样一来，街道上的房屋必然都是关着门的。接下来，打开当前这扇门然后向右移动一步。接下来不断向右移动，直到遇到开着的房门，也就是之前打开的这张门，换言之，目前刚好经过了所有房子一次，而房屋的数量就是向右移动的步数之和再加上1。

最后附上python代码：

```python
# Definition for a street.
# class Street:
#     def openDoor(self):
#         pass
#     def closeDoor(self):
#         pass
#     def isDoorOpen(self):
#         pass
#     def moveRight(self):
#         pass
#     def moveLeft(self):
#         pass
class Solution(object):
    def houseCount(self, street, k):
        """
        :type street: Street
        :type k: int
        :rtype: int
        """

        for i in range(k):
            if street.isDoorOpen():
                street.closeDoor()
            street.moveRight()
        
        street.openDoor()
        street.moveRight()
        res = 1
        while not street.isDoorOpen():
            street.moveRight()
            res += 1
        
        return res
```
