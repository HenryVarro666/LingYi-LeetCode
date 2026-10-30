---
title: "1688. 比赛中的配对次数"
aliases: ["yiduobo的每日leetcode 1688.比赛中的配对次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/446386259"
zhihu_id: "446386259"
zhihu_title: "yiduobo的每日leetcode 1688.比赛中的配对次数"
question_id: "1688"
question: "比赛中的配对次数"
problem_url: "https://leetcode.cn/problems/count-of-matches-in-tournament/"
created: "2021-12-17T00:25:01+08:00"
updated: "2021-12-17T00:25:01+08:00"
upvotes: 0
comments: 0
---

# 1688. 比赛中的配对次数

> **[yiduobo的每日leetcode 1688.比赛中的配对次数](https://zhuanlan.zhihu.com/p/446386259) · 知乎 · 2021-12-17 · 赞同 0**
> 力扣：[1688. 比赛中的配对次数](https://leetcode.cn/problems/count-of-matches-in-tournament/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1688.比赛中的配对次数

[力扣](https://leetcode-cn.com/problems/count-of-matches-in-tournament/)

脑筋急转弯的题目。由于一场比赛只会淘汰掉一只队伍，要从n支队伍中决出冠军，就需要淘汰掉n - 1只队伍，因此一共需要安排n - 1场比赛，答案就是n - 1。

最后附上python代码：

```python
class Solution(object):
    def numberOfMatches(self, n):
        """
        :type n: int
        :rtype: int
        """

        return n - 1
```
