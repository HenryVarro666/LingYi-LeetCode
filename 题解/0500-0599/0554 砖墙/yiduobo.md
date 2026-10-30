---
title: "554. 砖墙"
aliases: ["yiduobo的每日leetcode 554.砖墙"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/265208949"
zhihu_id: "265208949"
zhihu_title: "yiduobo的每日leetcode 554.砖墙"
question_id: "554"
question: "砖墙"
problem_url: "https://leetcode.cn/problems/brick-wall/"
created: "2020-10-12T23:15:57+08:00"
updated: "2020-10-12T23:15:57+08:00"
upvotes: 0
comments: 0
---

# 554. 砖墙

> **[yiduobo的每日leetcode 554.砖墙](https://zhuanlan.zhihu.com/p/265208949) · 知乎 · 2020-10-12 · 赞同 0**
> 力扣：[554. 砖墙](https://leetcode.cn/problems/brick-wall/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

554.砖墙<https://leetcode-cn.com/problems/brick-wall/>

对于一条竖线x\=k，要判断其是否穿过了第m层的砖，那么就是检测第m层从左边开始的前n块砖长度之和是否恰好等于k，这个前n块砖的长度之和很明显是一个前缀和。

注意到各层之间互不影响，因此可以分别计算出每一层砖块的前缀和，其中出现次数最多的那一个就是答案。

需要注意在计算前缀和的时候不应该计算最后一个砖块，因为答案不能是最右边的竖线。

最后附上python代码：

```python
class Solution(object):
    def leastBricks(self, wall):
        """
        :type wall: List[List[int]]
        :rtype: int
        """

        sum_dict = {}
        res = 0
        for i in range(len(wall)):
            prefix_sum = 0
            for j in range(len(wall[i]) - 1):
                prefix_sum += wall[i][j]
                sum_dict[prefix_sum] = sum_dict.get(prefix_sum, 0) + 1
                res = max(res, sum_dict[prefix_sum])

        return len(wall) - res
```
