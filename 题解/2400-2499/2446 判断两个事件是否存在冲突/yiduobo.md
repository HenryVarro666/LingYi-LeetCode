---
title: "2446. 判断两个事件是否存在冲突"
aliases: ["yiduobo的每日leetcode 2446.判断两个事件是否存在冲突"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string", "leetcode/qu-jian"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/584787822"
zhihu_id: "584787822"
zhihu_title: "yiduobo的每日leetcode 2446.判断两个事件是否存在冲突"
question_id: "2446"
question: "判断两个事件是否存在冲突"
problem_url: "https://leetcode.cn/problems/determine-if-two-events-have-conflict/"
difficulty: "Easy"
created: "2022-11-19T04:00:51+08:00"
updated: "2022-11-19T04:00:51+08:00"
upvotes: 0
comments: 0
---

# 2446. 判断两个事件是否存在冲突

> **[yiduobo的每日leetcode 2446.判断两个事件是否存在冲突](https://zhuanlan.zhihu.com/p/584787822) · 知乎 · 2022-11-19 · 赞同 0**
> 力扣：[2446. 判断两个事件是否存在冲突](https://leetcode.cn/problems/determine-if-two-events-have-conflict/) · Easy · 灵茶山艾府：[一行代码：比较两对字符串（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2446.判断两个事件是否存在冲突

[力扣](https://leetcode.cn/problems/determine-if-two-events-have-conflict/)

先将题目给出的两个时间区间从小时：分钟的表示方法转化为全部由分钟表示，此时问题就变成了给出两个区间，判断二者是否相交，那么只需判断是否存在某个区间的起点位于另一个区间的起点和终点之间即可。

最后附上python代码：

```python
class Solution(object):
    def haveConflict(self, event1, event2):
        """
        :type event1: List[str]
        :type event2: List[str]
        :rtype: bool
        """

        start_hour1, start_minute1 = event1[0].split(':')
        end_hour1, end_minute1 = event1[1].split(':')

        start1 = int(start_hour1) * 60 + int(start_minute1)
        end1 = int(end_hour1) * 60 + int(end_minute1)

        start_hour2, start_minute2 = event2[0].split(':')
        end_hour2, end_minute2 = event2[1].split(':')

        start2 = int(start_hour2) * 60 + int(start_minute2)
        end2 = int(end_hour2) * 60 + int(end_minute2)

        return start2 <= start1 <= end2 or start1 <= start2 <= end1
```
