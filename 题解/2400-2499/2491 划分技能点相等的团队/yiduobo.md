---
title: "2491. 划分技能点相等的团队"
aliases: ["yiduobo的每日leetcode 2491.划分技能点相等的团队"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/590392651"
zhihu_id: "590392651"
zhihu_title: "yiduobo的每日leetcode 2491.划分技能点相等的团队"
question_id: "2491"
question: "划分技能点相等的团队"
problem_url: "https://leetcode.cn/problems/divide-players-into-teams-of-equal-skill/"
difficulty: "Medium"
created: "2022-12-08T23:25:45+08:00"
updated: "2022-12-08T23:25:45+08:00"
upvotes: 0
comments: 0
---

# 2491. 划分技能点相等的团队

> **[yiduobo的每日leetcode 2491.划分技能点相等的团队](https://zhuanlan.zhihu.com/p/590392651) · 知乎 · 2022-12-08 · 赞同 0**
> 力扣：[2491. 划分技能点相等的团队](https://leetcode.cn/problems/divide-players-into-teams-of-equal-skill/) · Medium · 灵茶山艾府：[两种做法：排序 / 哈希表](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2491.划分技能点相等的团队

[力扣](https://leetcode.cn/problems/divide-players-into-teams-of-equal-skill/)

题目要求将数组划分成若干个二元组，且这些二元组中的两个数之和都相等，那么就可以先通过数组的总和处理数组长度的一半来计算出每个二元组中两个数之和应该等于多少，记这个数为target。若这里数组之和不是数组长度一半的倍数，那么就说明无法划分，此时直接返回-1。

接下来只需一趟遍历，使用哈希表记录当前还没有配对的数。对于当前遍历到的数sk，若哈希表中存在target - sk，那么就将其与当前的sk配对并更新答案，否则就将sk加入到哈希表中。

遍历完成后，若划分的二元组数量不等于数组长度的一半，说明有些数无法划分，此时同样是返回-1。

最后附上python代码：

```python
class Solution(object):
    def dividePlayers(self, skill):
        """
        :type skill: List[int]
        :rtype: int
        """

        n = len(skill)
        s = sum(skill)

        if (s + s) % n != 0:
            return -1

        res = 0
        target = (s + s) / n

        skill_cnt = {}
        pairs = 0
        for sk in skill:
            if skill_cnt.get(target - sk, 0) > 0:
                res += (target - sk) * sk
                skill_cnt[target - sk] -= 1
                pairs += 1
            else:
                skill_cnt[sk] = skill_cnt.get(sk, 0) + 1
        
        if pairs != n / 2:
            return -1
        return res
```
