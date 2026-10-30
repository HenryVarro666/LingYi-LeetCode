---
title: "2933. 高访问员工"
aliases: ["yiduobo的每日leetcode 2933.高访问员工"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/690670866"
zhihu_id: "690670866"
zhihu_title: "yiduobo的每日leetcode 2933.高访问员工"
question_id: "2933"
question: "高访问员工"
problem_url: "https://leetcode.cn/problems/high-access-employees/"
difficulty: "Medium"
created: "2024-04-04T02:40:00+08:00"
updated: "2024-04-04T02:40:00+08:00"
upvotes: 1
comments: 0
---

# 2933. 高访问员工

> **[yiduobo的每日leetcode 2933.高访问员工](https://zhuanlan.zhihu.com/p/690670866) · 知乎 · 2024-04-04 · 赞同 1**
> 力扣：[2933. 高访问员工](https://leetcode.cn/problems/high-access-employees/) · Medium · 灵茶山艾府：[按照名字分组+排序（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2933.高访问员工

[. - 力扣（LeetCode）](https://leetcode.cn/problems/high-access-employees/description/)

题目要求找出所有在某一小时至少访问系统三次的所有员工，那么就可以用哈希表将单个员工所有的访问时间收集起来形成list，然后从小到大进行排序。接下来对于单个员工，从该员工访问时间list的第3个时间点开始向后遍历，对于当前遍历到的时间点，若其上上个时间点与当前时间点的时间差在一小时以内，那么说明当前时间点、上一个时间点以及上上个时间点这三次访问出现在一小时内，也就是说当前员工是高访问员工。

为了方便计算，在这里可以将时间由小时-分钟的形式转化为纯的分钟。

最后附上python代码：

```python
class Solution(object):
    def findHighAccessEmployees(self, access_times):
        """
        :type access_times: List[List[str]]
        :rtype: List[str]
        """

        times_dict = {}
        for name, t in access_times:
            if name not in times_dict:
                times_dict[name] = []
            times_dict[name].append(int(t[:2]) * 60 + int(t[2:]))
        
        res = []
        for name in times_dict:
            times_list = sorted(times_dict[name])
            for i in range(2, len(times_list)):
                if times_list[i] - times_list[i - 2] < 60:
                    res.append(name)
                    break
        
        return res
```
