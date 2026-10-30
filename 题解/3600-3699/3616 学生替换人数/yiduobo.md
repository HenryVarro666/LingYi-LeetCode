---
title: "3616. 学生替换人数"
aliases: ["yiduobo的每日leetcode 3616.学生替换人数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1943840630011823752"
zhihu_id: "1943840630011823752"
zhihu_title: "yiduobo的每日leetcode 3616.学生替换人数"
question_id: "3616"
question: "学生替换人数"
problem_url: "https://leetcode.cn/problems/number-of-student-replacements/"
created: "2025-08-27T01:12:05+08:00"
updated: "2025-08-27T01:12:05+08:00"
upvotes: 0
comments: 0
---

# 3616. 学生替换人数

> **[yiduobo的每日leetcode 3616.学生替换人数](https://zhuanlan.zhihu.com/p/1943840630011823752) · 知乎 · 2025-08-27 · 赞同 0**
> 力扣：[3616. 学生替换人数](https://leetcode.cn/problems/number-of-student-replacements/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3616.学生替换人数

[3616. 学生替换人数 - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-student-replacements/description/)

题目给出一个整数数组ranks，其中ranks[index]表示第index个按顺序到达的学生排名。数字越低表示排名越好。在一开始，默认选中第一个学生。当一名排名严格更好的学生到来时，会发生替换，并取代当前的选择。问替换的总次数。

使用一个变量记录当前选择的学生排名now，然后一趟遍历，若遇到了更好的排名，就将now更新为这个排名，然后将答案加上1即可。

最后附上python代码：

```python
class Solution(object):
    def totalReplacements(self, ranks):
        """
        :type ranks: List[int]
        :rtype: int
        """
        
        now = ranks[0]
        res = 0
        for r in ranks[1:]:
            if r < now:
                now = r
                res += 1
        
        return res
```
