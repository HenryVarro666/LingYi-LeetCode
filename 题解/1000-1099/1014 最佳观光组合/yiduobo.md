---
title: "1014. 最佳观光组合"
aliases: ["yiduobo的每日leetcode 1014.最佳观光组合"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bian-li", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/367793161"
zhihu_id: "367793161"
zhihu_title: "yiduobo的每日leetcode 1014.最佳观光组合"
question_id: "1014"
question: "最佳观光组合"
problem_url: "https://leetcode.cn/problems/best-sightseeing-pair/"
difficulty: "Medium"
rating: 1730
created: "2021-04-25T21:33:20+08:00"
updated: "2021-04-25T21:33:20+08:00"
upvotes: 0
comments: 0
---

# 1014. 最佳观光组合

> **[yiduobo的每日leetcode 1014.最佳观光组合](https://zhuanlan.zhihu.com/p/367793161) · 知乎 · 2021-04-25 · 赞同 0**
> 力扣：[1014. 最佳观光组合](https://leetcode.cn/problems/best-sightseeing-pair/) · Medium · 灵茶山艾府：[枚举右，维护左，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

1014.最佳观光组合

[力扣](https://leetcode-cn.com/problems/best-sightseeing-pair/)

题目要求找出一个组合(i, j)，其中i \< j且values[i] + values[j] + i - j最大。

那么对于i而言，不妨设后续有两个位置p和q，那么(i, p)和(i, q)的收益分别为

values[i] + values[p] + i - p \= (values[i] + i) + (values[p] - p)

values[i] + values[q] + i - q \= (values[i] + i) + (values[q] - q)

对比下来可以发现，从i出发时最优的终点与i自身无关，而是要找到从i + 1开始values[j] - j最大的位置j。

于是我们可以从后往前进行一趟扫描枚举起点i，同时维护一个变量candidate表示当前最大的values[j] - j是多少。那么对于位置i而言，我们首先使用(values[i] + i) + candidate更新答案，然后再用values[i] - i更新candidate即可。

最后附上python代码：

```python
class Solution(object):
    def maxScoreSightseeingPair(self, values):
        """
        :type values: List[int]
        :rtype: int
        """

        res = 0
        candidate = values[-1] - len(values) + 1
        for index in range(len(values) - 2, -1, -1):
            res = max(res, values[index] + index + candidate)
            candidate = max(candidate, values[index] - index)
        
        return res
```
