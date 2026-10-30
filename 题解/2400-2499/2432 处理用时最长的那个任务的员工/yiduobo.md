---
title: "2432. 处理用时最长的那个任务的员工"
aliases: ["yiduobo的每日leetcode 2432.处理用时最长的那个任务的员工"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/582829480"
zhihu_id: "582829480"
zhihu_title: "yiduobo的每日leetcode 2432.处理用时最长的那个任务的员工"
question_id: "2432"
question: "处理用时最长的那个任务的员工"
problem_url: "https://leetcode.cn/problems/the-employee-that-worked-on-the-longest-task/"
difficulty: "Easy"
created: "2022-11-12T17:23:28+08:00"
updated: "2022-11-12T17:23:28+08:00"
upvotes: 0
comments: 0
---

# 2432. 处理用时最长的那个任务的员工

> **[yiduobo的每日leetcode 2432.处理用时最长的那个任务的员工](https://zhuanlan.zhihu.com/p/582829480) · 知乎 · 2022-11-12 · 赞同 0**
> 力扣：[2432. 处理用时最长的那个任务的员工](https://leetcode.cn/problems/the-employee-that-worked-on-the-longest-task/) · Easy · 灵茶山艾府：[阅读理解（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2432.处理用时最长的那个任务的员工

[力扣](https://leetcode.cn/problems/the-employee-that-worked-on-the-longest-task/)

可以发现，第一个任务的用时就是leaveTime[0]，而后续第i个任务的用时则是leaveTime[i] - leaveTime[i - 1]，于是只需要一趟遍历，计算每个任务的用时，然后取用时最长的任务对应的员工作为最终答案即可。如果用时相同，则取用户id最小的员工。

最后附上python代码：

```python
class Solution(object):
    def hardestWorker(self, n, logs):
        """
        :type n: int
        :type logs: List[List[int]]
        :rtype: int
        """

        res, ma = logs[0]
        for index in range(1, len(logs)):
            if logs[index][1] - logs[index - 1][1] > ma:
                ma = logs[index][1] - logs[index - 1][1]
                res = logs[index][0]
            elif logs[index][1] - logs[index - 1][1] == ma and logs[index][0] < res:
                res = logs[index][0]
        
        return res
```
