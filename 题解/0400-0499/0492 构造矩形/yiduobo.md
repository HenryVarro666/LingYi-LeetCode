---
title: "492. 构造矩形"
aliases: ["yiduobo的每日leetcode 492.构造矩形"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/255113939"
zhihu_id: "255113939"
zhihu_title: "yiduobo的每日leetcode 492.构造矩形"
question_id: "492"
question: "构造矩形"
problem_url: "https://leetcode.cn/problems/construct-the-rectangle/"
created: "2020-09-19T19:48:42+08:00"
updated: "2020-09-19T19:48:42+08:00"
upvotes: 0
comments: 0
---

# 492. 构造矩形

> **[yiduobo的每日leetcode 492.构造矩形](https://zhuanlan.zhihu.com/p/255113939) · 知乎 · 2020-09-19 · 赞同 0**
> 力扣：[492. 构造矩形](https://leetcode.cn/problems/construct-the-rectangle/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

492.构造矩形<https://leetcode-cn.com/problems/construct-the-rectangle/>

为了使得W小于等于L且W和L尽可能接近，那么应该从sqrt(area)开始，逐个往下枚举W。当area模W为0时，L为area/W，此时的W和L即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def constructRectangle(self, area):
        """
        :type area: int
        :rtype: List[int]
        """

        W = int(sqrt(area))
        while area % W != 0:
            W -= 1
        return [area / W, W]
```
