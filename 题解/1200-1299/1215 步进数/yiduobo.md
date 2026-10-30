---
title: "1215. 步进数"
aliases: ["yiduobo的每日leetcode 1215.步进数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/613236467"
zhihu_id: "613236467"
zhihu_title: "yiduobo的每日leetcode 1215.步进数"
question_id: "1215"
question: "步进数"
problem_url: "https://leetcode.cn/problems/stepping-numbers/"
created: "2023-03-11T21:57:13+08:00"
updated: "2023-03-11T21:57:13+08:00"
upvotes: 0
comments: 0
---

# 1215. 步进数

> **[yiduobo的每日leetcode 1215.步进数](https://zhuanlan.zhihu.com/p/613236467) · 知乎 · 2023-03-11 · 赞同 0**
> 力扣：[1215. 步进数](https://leetcode.cn/problems/stepping-numbers/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1215.步进数

[力扣](https://leetcode.cn/problems/stepping-numbers/)

看上去应该是数位动态规划的问题，不过注意到low和high最多只有10位，而每一位在上一轮的基础上最多只有两种可行的选择，因此可以直接从最高位开始向后进行搜索回溯。

需要注意的是，最高位的取值只能是1到9。

最后附上python代码：

```python
class Solution(object):
    def countSteppingNumbers(self, low, high):
        """
        :type low: int
        :type high: int
        :rtype: List[int]
        """

        global res
        res = []
        if low == 0:
            res.append(0)
        

        def dfs(now, level):
            if low <= now <= high:
                res.append(now)
            
            if level == 10:
                return
            
            last = now % 10
            if last > 0:
                dfs(now * 10 + last - 1, level + 1)
            if last < 9:
                dfs(now * 10 + last + 1, level + 1)

        for first in range(1, 10):
            dfs(first, 1)
        
        return sorted(res)
```
