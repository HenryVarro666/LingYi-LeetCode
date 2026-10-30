---
title: "252. 会议室"
aliases: ["yiduobo的每日leetcode 252.会议室"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/592627429"
zhihu_id: "592627429"
zhihu_title: "yiduobo的每日leetcode 252.会议室"
question_id: "252"
question: "会议室"
problem_url: "https://leetcode.cn/problems/meeting-rooms/"
created: "2022-12-18T03:37:42+08:00"
updated: "2022-12-18T03:37:42+08:00"
upvotes: 0
comments: 0
---

# 252. 会议室

> **[yiduobo的每日leetcode 252.会议室](https://zhuanlan.zhihu.com/p/592627429) · 知乎 · 2022-12-18 · 赞同 0**
> 力扣：[252. 会议室](https://leetcode.cn/problems/meeting-rooms/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

252.会议室

[力扣](https://leetcode.cn/problems/meeting-rooms/)

题目给出了若干区间，问是否存在相加的区间。

对于区间i和区间j，不妨设start[i] >\= start[j]，那么当end[j] > start[i]时，这两个区间才会相交。

根据这个结论，就可以先将所有区间按start从小到大进行排序，然后一趟遍历。对于当前遍历到的区间\[start\[i\], end\[i\]\]，若存在某个j \< i满足end\[j\] > start\[i\]，那么区间i和区间j就是相交的。因此可以使用一个变量max_end记录当前遍历过的区间中最大的end，然后通过max_end和当前遍历到的start判断区间是否相交，若相交，返回false，否则就是用当前区间的end来更新max_end然后继续向后遍历。

最后附上python代码：

```python
class Solution(object):
    def canAttendMeetings(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: bool
        """

        if not intervals:
            return True

        intervals.sort(key=lambda d:d[0])
        max_end = intervals[0][1]
        for start, end in intervals[1:]:
            if start < max_end:
                return False
            max_end = max(end, max_end)
        
        return True
```
