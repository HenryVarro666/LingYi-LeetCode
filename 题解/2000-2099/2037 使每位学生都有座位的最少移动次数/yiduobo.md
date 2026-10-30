---
title: "2037. 使每位学生都有座位的最少移动次数"
aliases: ["yiduobo的每日leetcode 2037.使每位学生都有座位的最少移动次数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/math", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/509202678"
zhihu_id: "509202678"
zhihu_title: "yiduobo的每日leetcode 2037.使每位学生都有座位的最少移动次数"
question_id: "2037"
question: "使每位学生都有座位的最少移动次数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-moves-to-seat-everyone/"
difficulty: "Easy"
rating: 1357
created: "2022-05-04T17:53:03+08:00"
updated: "2022-05-04T17:53:03+08:00"
upvotes: 1
comments: 0
---

# 2037. 使每位学生都有座位的最少移动次数

> **[yiduobo的每日leetcode 2037.使每位学生都有座位的最少移动次数](https://zhuanlan.zhihu.com/p/509202678) · 知乎 · 2022-05-04 · 赞同 1**
> 力扣：[2037. 使每位学生都有座位的最少移动次数](https://leetcode.cn/problems/minimum-number-of-moves-to-seat-everyone/) · Easy · 灵茶山艾府：[排序+贪心](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2037.使每位学生都有座位的最少移动次数

[力扣](https://leetcode-cn.com/problems/minimum-number-of-moves-to-seat-everyone/)

将最靠边的学生安排到最靠边的座位上是非常直观的，因此可以将座位和学生都从小到大排序，然后一趟遍历逐个将学生安排到对应的座位上。

最后附上python代码：

```python
class Solution(object):
    def minMovesToSeat(self, seats, students):
        """
        :type seats: List[int]
        :type students: List[int]
        :rtype: int
        """

        sorted_seats = sorted(seats)
        sorted_students = sorted(students)

        res = 0
        for index in range(len(sorted_seats)):
            res += abs(sorted_seats[index] - sorted_students[index])
        
        return res
```
