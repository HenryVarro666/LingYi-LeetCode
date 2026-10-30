---
title: "4020. 电梯请求I"
aliases: ["yiduobo的每日leetcode 4020.电梯请求I"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2072836723609022555"
zhihu_id: "2072836723609022555"
zhihu_title: "yiduobo的每日leetcode 4020.电梯请求I"
question_id: "4020"
question: "电梯请求 I"
problem_url: "https://leetcode.cn/problems/elevator-requests-i/"
difficulty: "Easy"
created: "2026-08-18T00:10:50+08:00"
updated: "2026-08-18T00:10:52+08:00"
upvotes: 1
comments: 0
---

# 4020. 电梯请求I

> **[yiduobo的每日leetcode 4020.电梯请求I](https://zhuanlan.zhihu.com/p/2072836723609022555) · 知乎 · 2026-08-18 · 赞同 1**
> 力扣：[4020. 电梯请求 I](https://leetcode.cn/problems/elevator-requests-i/) · Easy · 灵茶山艾府：[遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4020.电梯请求I

<https://leetcode.cn/problems/elevator-requests-i/>

给出一个整数n，表示一栋楼房的楼层数，楼层编号从0到n - 1。

同时给出一个整数数组requests，其中requests表示楼层请求的序列。

一部电梯初始在第0层，遵循以下规则：

- 电梯每秒移动一层
- 电梯按照给定的顺序处理请求
- 如果电梯已经在请求的楼层，则不需要移动
- 处理完一个请求后，电梯立即开始向下一个请求的楼层移动

返回处理请求所需的总时间，以秒为单位

活了三十多年，第一次见到有0层的电梯。

本题中需要计算的实际上就是request中相邻元素之差的和，于是可以使用pre记录上一个元素，初始值为0，然后对request进行一趟遍历，对于当前元素v，先将abs(v - pre)累加到答案中，然后将pre更新为v即可。

最后附上python代码：

```python
class Solution(object):
    def elevatorRequests(self, n, requests):
        """
        :type n: int
        :type requests: List[int]
        :rtype: int
        """
        
        pre = 0
        res = 0
        for v in requests:
            res += abs(v - pre)
            pre = v
        
        return res
```
