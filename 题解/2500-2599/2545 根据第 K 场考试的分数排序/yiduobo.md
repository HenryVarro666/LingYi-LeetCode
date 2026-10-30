---
title: "2545. 根据第K场考试的分数排序"
aliases: ["yiduobo的每日leetcode 2545.根据第K场考试的分数排序"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/637873641"
zhihu_id: "637873641"
zhihu_title: "yiduobo的每日leetcode 2545.根据第K场考试的分数排序"
question_id: "2545"
question: "根据第 K 场考试的分数排序"
problem_url: "https://leetcode.cn/problems/sort-the-students-by-their-kth-score/"
difficulty: "Medium"
created: "2023-06-21T21:55:45+08:00"
updated: "2023-06-21T21:55:45+08:00"
upvotes: 0
comments: 0
---

# 2545. 根据第K场考试的分数排序

> **[yiduobo的每日leetcode 2545.根据第K场考试的分数排序](https://zhuanlan.zhihu.com/p/637873641) · 知乎 · 2023-06-21 · 赞同 0**
> 力扣：[2545. 根据第 K 场考试的分数排序](https://leetcode.cn/problems/sort-the-students-by-their-kth-score/) · Medium · 灵茶山艾府：[自定义排序，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2545.根据第K场考试的分数排序

[力扣](https://leetcode.cn/problems/sort-the-students-by-their-kth-score/)

题目给出一个二维数组，要求使用第k列作为关键字进行排序。如果使用python的话，直接使用lambda表达式就行了，而对于不具有相关特性的语言，则需要先将第k列单独抽出来，携带着行号一起排序后再将当前的序反向映射回行的下标，再将行填充到答案数组中。

最后附上python代码：

```python
class Solution(object):
    def sortTheStudents(self, score, k):
        """
        :type score: List[List[int]]
        :type k: int
        :rtype: List[List[int]]
        """

        return sorted(score, key=lambda d:-d[k])
```
