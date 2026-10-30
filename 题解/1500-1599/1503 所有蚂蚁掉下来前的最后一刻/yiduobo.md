---
title: "1503. 所有蚂蚁掉下来前的最后一刻"
aliases: ["yiduobo的每日leetcode 1503.所有蚂蚁掉下来前的最后一刻"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/419250157"
zhihu_id: "419250157"
zhihu_title: "yiduobo的每日leetcode 1503.所有蚂蚁掉下来前的最后一刻"
question_id: "1503"
question: "所有蚂蚁掉下来前的最后一刻"
problem_url: "https://leetcode.cn/problems/last-moment-before-all-ants-fall-out-of-a-plank/"
created: "2021-10-08T23:04:07+08:00"
updated: "2021-10-08T23:04:07+08:00"
upvotes: 1
comments: 0
---

# 1503. 所有蚂蚁掉下来前的最后一刻

> **[yiduobo的每日leetcode 1503.所有蚂蚁掉下来前的最后一刻](https://zhuanlan.zhihu.com/p/419250157) · 知乎 · 2021-10-08 · 赞同 1**
> 力扣：[1503. 所有蚂蚁掉下来前的最后一刻](https://leetcode.cn/problems/last-moment-before-all-ants-fall-out-of-a-plank/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1503.所有蚂蚁掉下来前的最后一刻

[力扣](https://leetcode-cn.com/problems/last-moment-before-all-ants-fall-out-of-a-plank/)

经典的脑筋急转弯问题，但两只蚂蚁相遇时，虽然题目描述是二者各自开始反向行走，但是也可以认为是两只蚂蚁各走各的互不影响，那么这里就只需要统计向右走的蚂蚁距离n的最远距离，以及向左走的蚂蚁距离0的最远距离，取二者的最大值即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def getLastMoment(self, n, left, right):
        """
        :type n: int
        :type left: List[int]
        :type right: List[int]
        :rtype: int
        """

        if len(left) == 0:
            l = 0
        else:
            l = max(left)
        
        if len(right) == 0:
            r = 0
        else:
            r = n - min(right)
        
        return max(l, r)
```
