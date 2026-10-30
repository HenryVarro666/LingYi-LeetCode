---
title: "2753. 计算一个环形街道上的房屋数量II"
aliases: ["yiduobo的每日leetcode 2753.计算一个环形街道上的房屋数量II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/brainteaser", "leetcode/interactive", "题单/贪心算法", "题单/贪心算法/八-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/654322582"
zhihu_id: "654322582"
zhihu_title: "yiduobo的每日leetcode 2753.计算一个环形街道上的房屋数量II"
question_id: "2753"
question: "计算一个环形街道上的房屋数量 II"
problem_url: "https://leetcode.cn/problems/count-houses-in-a-circular-street-ii/"
difficulty: "Hard"
created: "2023-09-05T03:49:07+08:00"
updated: "2023-09-05T03:49:07+08:00"
upvotes: 1
comments: 3
---

# 2753. 计算一个环形街道上的房屋数量II

> **[yiduobo的每日leetcode 2753.计算一个环形街道上的房屋数量II](https://zhuanlan.zhihu.com/p/654322582) · 知乎 · 2023-09-05 · 赞同 1**
> 力扣：[2753. 计算一个环形街道上的房屋数量 II](https://leetcode.cn/problems/count-houses-in-a-circular-street-ii/) · Hard · 灵茶山艾府：[线性做法（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2753.计算一个环形街道上的房屋数量II

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/count-houses-in-a-circular-street-ii/)

之前环形街道房屋数量问题的加强版，本题没有向左走的操作，也没有开门的操作，这也就意味着需要利用开着的门作为标记。

对于一扇开着的门，如果从这扇门右侧开始向右走，那么这扇门将是一轮遍历中最后一扇被访问到的开着的门，在这里就可以利用这一点。首先从当前位置开始不断向右走，直到遇到一扇开着的门。接下来从这扇门右侧的门开始不断向右走，期间将路过的开着的门关闭，同时记录下最后一次关门时走过的步数。

当行走k步后，至少走过了一圈，过程中关闭的最后那扇门就是最开始那扇开着的门，换言之，这个步数就是从最开始开着的门右侧开始向右走到这扇门的步数，也就是环形街道上房屋的数量。

最后附上python代码：

```python
# Definition for a street.
# class Street:
#     def closeDoor(self):
#         pass
#     def isDoorOpen(self):
#         pass
#     def moveRight(self):
#         pass
class Solution(object):
    def houseCount(self, street, k):
        """
        :type street: Street
        :type k: int
        :rtype: int
        """

        while not street.isDoorOpen():
            street.moveRight()
        
        street.moveRight()
        res = None
        for index in range(1, k + 1):
            if street.isDoorOpen():
                res = index
                street.closeDoor()
            
            street.moveRight()

        return res
```
