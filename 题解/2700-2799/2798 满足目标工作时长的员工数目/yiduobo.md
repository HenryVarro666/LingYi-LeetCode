---
title: "2798. 满足目标工作时长的员工数目"
aliases: ["yiduobo的每日leetcode 2798.满足目标工作时长的员工数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/657051684"
zhihu_id: "657051684"
zhihu_title: "yiduobo的每日leetcode 2798.满足目标工作时长的员工数目"
question_id: "2798"
question: "满足目标工作时长的员工数目"
problem_url: "https://leetcode.cn/problems/number-of-employees-who-met-the-target/"
difficulty: "Easy"
created: "2023-09-19T04:03:02+08:00"
updated: "2023-09-19T04:03:02+08:00"
upvotes: 0
comments: 0
---

# 2798. 满足目标工作时长的员工数目

> **[yiduobo的每日leetcode 2798.满足目标工作时长的员工数目](https://zhuanlan.zhihu.com/p/657051684) · 知乎 · 2023-09-19 · 赞同 0**
> 力扣：[2798. 满足目标工作时长的员工数目](https://leetcode.cn/problems/number-of-employees-who-met-the-target/) · Easy · 灵茶山艾府：[遍历（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2798.满足目标工作时长的员工数目

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/number-of-employees-who-met-the-target/description/)

比较入门的题目。直接一趟遍历，统计数组中大于等于target的数的个数即可。

最后附上python代码：

```python
class Solution(object):
    def numberOfEmployeesWhoMetTarget(self, hours, target):
        """
        :type hours: List[int]
        :type target: int
        :rtype: int
        """

        res = 0
        for h in hours:
            if h >= target:
                res += 1
        
        return res
```
