---
title: "551. 学生出勤记录I"
aliases: ["yiduobo的每日leetcode 551.学生出勤记录I"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string", "leetcode/string-matching"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/261750210"
zhihu_id: "261750210"
zhihu_title: "yiduobo的每日leetcode 551.学生出勤记录I"
question_id: "551"
question: "学生出勤记录 I"
problem_url: "https://leetcode.cn/problems/student-attendance-record-i/"
difficulty: "Easy"
created: "2020-10-10T22:53:24+08:00"
updated: "2020-10-10T22:53:24+08:00"
upvotes: 0
comments: 0
---

# 551. 学生出勤记录I

> **[yiduobo的每日leetcode 551.学生出勤记录I](https://zhuanlan.zhihu.com/p/261750210) · 知乎 · 2020-10-10 · 赞同 0**
> 力扣：[551. 学生出勤记录 I](https://leetcode.cn/problems/student-attendance-record-i/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

551.学生出勤记录I <https://leetcode-cn.com/problems/student-attendance-record-i/>

比较基础的题目，直接一趟遍历，统计A和连续出现的L的个数即可。

最后附上python代码：

```python
class Solution(object):
    def checkRecord(self, s):
        """
        :type s: str
        :rtype: bool
        """

        absent = 0
        late = 0
        for char in s:
            if char == 'A':
                absent += 1
                if absent > 1:
                    return False
                late = 0
            elif char == 'L':
                late += 1
                if late > 2:
                    return False
            else:
                late = 0

        return True
```
