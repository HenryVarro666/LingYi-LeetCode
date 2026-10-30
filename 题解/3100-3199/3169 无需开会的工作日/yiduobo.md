---
title: "3169. 无需开会的工作日"
aliases: ["yiduobo的每日leetcode 3169.无需开会的工作日"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/二-区间贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/705000298"
zhihu_id: "705000298"
zhihu_title: "yiduobo的每日leetcode 3169.无需开会的工作日"
question_id: "3169"
question: "无需开会的工作日"
problem_url: "https://leetcode.cn/problems/count-days-without-meetings/"
difficulty: "Medium"
rating: 1483
created: "2024-06-23T23:01:15+08:00"
updated: "2024-06-23T23:01:15+08:00"
upvotes: 0
comments: 0
---

# 3169. 无需开会的工作日

> **[yiduobo的每日leetcode 3169.无需开会的工作日](https://zhuanlan.zhihu.com/p/705000298) · 知乎 · 2024-06-23 · 赞同 0**
> 力扣：[3169. 无需开会的工作日](https://leetcode.cn/problems/count-days-without-meetings/) · Medium · 灵茶山艾府：[正难则反+合并区间（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3169.无需开会的工作日

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-days-without-meetings/description/)

题目给出一个正整数days以及一个二维数组meetings，其中meetings\[i\] \= \[start\[i\], end\[i\]\]，表示在start\[i\]到end\[i\]这一段时间内需要开会。问从1到days这一段时间内，有几天是不用开会的。

非常标准的区间合并问题，先将meeting按start从小到达排序，然后一趟遍历。过程中使用一组变量[x, y]记录当前考察的区间，对于当前遍历到的[start, end]，若y >\= start，说明这两个区间是重叠的，若end大于y，那么就应该将y更新为end；反之，若y \< start，说明这两个区间不重叠，又由于区间是按起点排序的，因此后续的区间起点也必然大于y，也就是说[x, y]不会与后续区间重叠。此时就应该将区间之间的间隔，即start - y - 1累加到答案中，然后将[x, y]更新为[start, end]。

除了上面计算的会议之间的时间外，还需要将第一场会议开始前的日期，以及最后一场会议结束后的日期也累加到答案中。

最后附上python代码：

```python
class Solution(object):
    def countDays(self, days, meetings):
        """
        :type days: int
        :type meetings: List[List[int]]
        :rtype: int
        """

        meetings.sort()
        x, y = meetings[0]
        res = x - 1
        for start, end in meetings[1:]:
            if start <= y:
                y = max(y, end)
            else:
                res += start - y - 1
                x, y = start, end

        res += days - y
    
        return res
```
