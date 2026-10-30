---
title: "911. 在线选举"
aliases: ["yiduobo的每日leetcode 911.在线选举"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/354691519"
zhihu_id: "354691519"
zhihu_title: "yiduobo的每日leetcode 911.在线选举"
question_id: "911"
question: "在线选举"
problem_url: "https://leetcode.cn/problems/online-election/"
created: "2021-03-04T23:26:10+08:00"
updated: "2021-03-04T23:26:10+08:00"
upvotes: 0
comments: 0
---

# 911. 在线选举

> **[yiduobo的每日leetcode 911.在线选举](https://zhuanlan.zhihu.com/p/354691519) · 知乎 · 2021-03-04 · 赞同 0**
> 力扣：[911. 在线选举](https://leetcode.cn/problems/online-election/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

911.在线选举

[力扣](https://leetcode-cn.com/problems/online-election/)

由于我们只关心最终的结果而不关心票数，因此我们可以按时间遍历整个投票过程，记录下每次投票结果产生改变的时间点，那么就可以得到一个单调递增的数组，该数组记录了每次投票结果改变的时间点以及这一时刻的投票结果。

接下来对于每次查询，我们只需要找到数组中小于查询的时间点，且离查询时间点最近的票选结果即可。单调数组的查询自然就想到使用二分法，不过需要特别判断查询的时间点恰好等于某个数组中的时间点的情况，此时投票结果是正好产生了变更的。

最后附上python代码：

```python
class TopVotedCandidate(object):

    def __init__(self, persons, times):
        """
        :type persons: List[int]
        :type times: List[int]
        """
        cnt_dict = {}
        max_cnt = 0
        winner = None
        self.candidate_list = []
        for p, t in zip(persons, times):
            cnt_dict[p] = cnt_dict.get(p, 0) + 1
            if cnt_dict[p] >= max_cnt:
                max_cnt = cnt_dict[p]
                if winner != p:
                    self.candidate_list.append([p, t])
                    winner = p

    def q(self, t):
        """
        :type t: int
        :rtype: int
        """
        if t >= self.candidate_list[-1][1]:
            return self.candidate_list[-1][0]
        else:
            l = 0
            r = len(self.candidate_list) - 1
            while l < r:
                mid = (l + r) >> 1
                if t > self.candidate_list[mid][1]:
                    l = mid + 1
                else:
                    r = mid
            
            if self.candidate_list[l][1] == t:
                return self.candidate_list[l][0]
            else:
                return self.candidate_list[l - 1][0]

# Your TopVotedCandidate object will be instantiated and called as such:
# obj = TopVotedCandidate(persons, times)
# param_1 = obj.q(t)
```
