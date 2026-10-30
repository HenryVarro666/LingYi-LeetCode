---
title: "1491. 去掉最低工资和最高工资后的工资平均值"
aliases: ["yiduobo的每日leetcode 1491.去掉最低工资和最高工资后的工资平均值"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/simulation", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/416698488"
zhihu_id: "416698488"
zhihu_title: "yiduobo的每日leetcode 1491.去掉最低工资和最高工资后的工资平均值"
question_id: "1491"
question: "去掉最低工资和最高工资后的工资平均值"
problem_url: "https://leetcode.cn/problems/average-salary-excluding-the-minimum-and-maximum-salary/"
difficulty: "Easy"
created: "2021-10-03T20:18:06+08:00"
updated: "2021-10-03T20:18:06+08:00"
upvotes: 0
comments: 0
---

# 1491. 去掉最低工资和最高工资后的工资平均值

> **[yiduobo的每日leetcode 1491.去掉最低工资和最高工资后的工资平均值](https://zhuanlan.zhihu.com/p/416698488) · 知乎 · 2021-10-03 · 赞同 0**
> 力扣：[1491. 去掉最低工资和最高工资后的工资平均值](https://leetcode.cn/problems/average-salary-excluding-the-minimum-and-maximum-salary/) · Easy · 灵茶山艾府：[编程基础题（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1491.去掉最低工资和最高工资后的工资平均值

[力扣](https://leetcode-cn.com/problems/average-salary-excluding-the-minimum-and-maximum-salary/)

比较基础的题目。一趟扫描，找出其中的最小值和最大值，并在这个过程中顺便求和。最后将这个和减去最小值和最大值，然后除以总数减二即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def average(self, salary):
        """
        :type salary: List[int]
        :rtype: float
        """

        tot = mi = ma = salary[0]
        for s in salary[1:]:
            tot += s
            mi = min(mi, s)
            ma = max(ma, s)

        tot -= mi + ma
        return tot * 1.0 / (len(salary) - 2)
```
