---
title: "2323. 完成所有工作的最短时间"
aliases: ["yiduobo的每日leetcode 2323.完成所有工作的最短时间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/629652995"
zhihu_id: "629652995"
zhihu_title: "yiduobo的每日leetcode 2323.完成所有工作的最短时间"
question_id: "2323"
question: "完成所有工作的最短时间"
problem_url: "https://leetcode.cn/problems/find-minimum-time-to-finish-all-jobs-ii/"
created: "2023-05-16T02:47:10+08:00"
updated: "2023-05-16T02:47:10+08:00"
upvotes: 0
comments: 0
---

# 2323. 完成所有工作的最短时间

> **[yiduobo的每日leetcode 2323.完成所有工作的最短时间](https://zhuanlan.zhihu.com/p/629652995) · 知乎 · 2023-05-16 · 赞同 0**
> 力扣：[2323. 完成所有工作的最短时间](https://leetcode.cn/problems/find-minimum-time-to-finish-all-jobs-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2323.完成所有工作的最短时间

[力扣](https://leetcode.cn/problems/find-minimum-time-to-finish-all-jobs-ii/)

由于题目要求所有人完成工作的最长时间最短，就应该将最难的工作分配给最能干的工人。证明也很简单，对于i和j两个工人，不妨设workers[i] > workers[j]，那么对于一组工作x和y，设x > y，那么如果让工人i处理x，工人j处理y，所需时间就是max(x / workers[i]，y / workers[j])，反之则需要max(x / workers[j]，y / workers[i])。

可以发现，x / workers[j] > x / workers[i]，理由是分母中workers[j]较小。另一方面，x / workers[j] > y / workers[j]，理由是分子中x较大。综合起来就可以发现，交换之后的方案中完成任务x所需的时间比原始方案中完成两个任务的时间都要长，显然是不优的。

根据上面这个结论，就只需要将workers以及jobs都按小从大排序，然后一一对应分配，计算所需时间并取其中的最大值作为最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def minimumTime(self, jobs, workers):
        """
        :type jobs: List[int]
        :type workers: List[int]
        :rtype: int
        """

        res = 0
        for j, w in zip(sorted(jobs), sorted(workers)):
            t = j / w
            if j % w != 0:
                t += 1
            
            res = max(res, t)
        
        return res
```
