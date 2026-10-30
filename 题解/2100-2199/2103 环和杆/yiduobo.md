---
title: "2103. 环和杆"
aliases: ["yiduobo的每日leetcode 2103.环和杆"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/522287841"
zhihu_id: "522287841"
zhihu_title: "yiduobo的每日leetcode 2103.环和杆"
question_id: "2103"
question: "环和杆"
problem_url: "https://leetcode.cn/problems/rings-and-rods/"
created: "2022-05-30T23:49:09+08:00"
updated: "2022-05-30T23:49:09+08:00"
upvotes: 0
comments: 0
---

# 2103. 环和杆

> **[yiduobo的每日leetcode 2103.环和杆](https://zhuanlan.zhihu.com/p/522287841) · 知乎 · 2022-05-30 · 赞同 0**
> 力扣：[2103. 环和杆](https://leetcode.cn/problems/rings-and-rods/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2103.环和杆

[力扣](https://leetcode.cn/problems/rings-and-rods/)

由于杆子只有10根，那么可以使用哈希表记录下每种颜色分别套在哪些杆子上。接下来只需遍历所有的杆子，判断该杆子上是否三种颜色齐备即可。

最后附上python代码：

```python
class Solution(object):
    def countPoints(self, rings):
        """
        :type rings: str
        :rtype: int
        """

        red = set()
        green = set()
        blue = set()

        for index in range(0, len(rings), 2):
            color = rings[index]
            pos = int(rings[index + 1])
            if color == 'R':
                red.add(pos)
            elif color == 'G':
                green.add(pos)
            else:
                blue.add(pos)
        
        res = 0
        for index in range(10):
            if index in red and index in green and index in blue:
                res += 1
        
        return res
```
