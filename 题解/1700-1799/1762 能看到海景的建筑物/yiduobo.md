---
title: "1762. 能看到海景的建筑物"
aliases: ["yiduobo的每日leetcode 1762.能看到海景的建筑物"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/620883985"
zhihu_id: "620883985"
zhihu_title: "yiduobo的每日leetcode 1762.能看到海景的建筑物"
question_id: "1762"
question: "能看到海景的建筑物"
problem_url: "https://leetcode.cn/problems/buildings-with-an-ocean-view/"
created: "2023-04-10T21:58:30+08:00"
updated: "2023-04-10T21:58:30+08:00"
upvotes: 0
comments: 0
---

# 1762. 能看到海景的建筑物

> **[yiduobo的每日leetcode 1762.能看到海景的建筑物](https://zhuanlan.zhihu.com/p/620883985) · 知乎 · 2023-04-10 · 赞同 0**
> 力扣：[1762. 能看到海景的建筑物](https://leetcode.cn/problems/buildings-with-an-ocean-view/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1762.能看到海景的建筑物

[力扣](https://leetcode.cn/problems/buildings-with-an-ocean-view/)

对于一栋建筑，其能否看到海景取决于其右侧最高的建筑物高度是否比该建筑要矮，于是只需从后向前一趟遍历，首先判断当前建筑是否能看到海景，然后使用当前建筑的高度更新右侧最高建筑的高度。

最后附上python代码：

```python
class Solution(object):
    def findBuildings(self, heights):
        """
        :type heights: List[int]
        :rtype: List[int]
        """

        n = len(heights)
        res = [n - 1]
        now = heights[-1]
        for index in range(n - 2, -1, -1):
            if heights[index] > now:
                res.append(index)
                now = heights[index]
        
        res.reverse()
        return res
```
