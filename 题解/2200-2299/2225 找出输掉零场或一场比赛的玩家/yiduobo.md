---
title: "2225. 找出输掉零场或一场比赛的玩家"
aliases: ["yiduobo的每日leetcode 2225.找出输掉零场或一场比赛的玩家"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/sorting", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/542707753"
zhihu_id: "542707753"
zhihu_title: "yiduobo的每日leetcode 2225.找出输掉零场或一场比赛的玩家"
question_id: "2225"
question: "找出输掉零场或一场比赛的玩家"
problem_url: "https://leetcode.cn/problems/find-players-with-zero-or-one-losses/"
difficulty: "Medium"
created: "2022-07-17T18:35:36+08:00"
updated: "2022-07-17T18:35:36+08:00"
upvotes: 0
comments: 0
---

# 2225. 找出输掉零场或一场比赛的玩家

> **[yiduobo的每日leetcode 2225.找出输掉零场或一场比赛的玩家](https://zhuanlan.zhihu.com/p/542707753) · 知乎 · 2022-07-17 · 赞同 0**
> 力扣：[2225. 找出输掉零场或一场比赛的玩家](https://leetcode.cn/problems/find-players-with-zero-or-one-losses/) · Medium · 灵茶山艾府：[哈希表+排序（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2225.找出输掉零场或一场比赛的玩家

[力扣](https://leetcode.cn/problems/find-players-with-zero-or-one-losses/)

使用哈希表统计每个玩家输掉的场次，然后从小到大遍历出现的所有玩家，利用哈希表判断当前玩家是否没输过或者只输了一场，然后更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def findWinners(self, matches):
        """
        :type matches: List[List[int]]
        :rtype: List[List[int]]
        """

        candidate = set()
        cnt_dict = {}
        for winner, loser in matches:
            candidate.add(winner)
            candidate.add(loser)
            cnt_dict[loser] = cnt_dict.get(loser, 0) + 1
        
        res = [[], []]
        for index in sorted(list(candidate)):
            cnt = cnt_dict.get(index, 0)
            if cnt <= 1:
                res[cnt].append(index)
        
        return res
```
