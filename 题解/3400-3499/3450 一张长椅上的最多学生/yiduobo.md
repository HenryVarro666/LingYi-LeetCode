---
title: "3450. 一张长椅上的最多学生"
aliases: ["yiduobo的每日leetcode 3450.一张长椅上的最多学生"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1893407382723343455"
zhihu_id: "1893407382723343455"
zhihu_title: "yiduobo的每日leetcode 3450.一张长椅上的最多学生"
question_id: "3450"
question: "一张长椅上的最多学生"
problem_url: "https://leetcode.cn/problems/maximum-students-on-a-single-bench/"
created: "2025-04-09T21:26:16+08:00"
updated: "2025-04-09T21:26:16+08:00"
upvotes: 0
comments: 0
---

# 3450. 一张长椅上的最多学生

> **[yiduobo的每日leetcode 3450.一张长椅上的最多学生](https://zhuanlan.zhihu.com/p/1893407382723343455) · 知乎 · 2025-04-09 · 赞同 0**
> 力扣：[3450. 一张长椅上的最多学生](https://leetcode.cn/problems/maximum-students-on-a-single-bench/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3450.一张长椅上的最多学生

[3450. 一张长椅上的最多学生 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-students-on-a-single-bench/description/)

题目给出一个二维数组students，其中students[i] \= [stutend_id, bench_id]，表示学生student_id正坐在长椅bench_id上。现在要求返回单个长椅上坐着的不同学生的最大数量，如果没有，则返回0。

输入中可能出现一个学生出现在同一张长椅上多次的情况，但是每张长椅的每个学生只能计算一次。

一趟遍历，对每张长椅都使用一个集合记录当前长椅上有哪些学生，其中最大的集合大小就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxStudentsOnBench(self, students):
        """
        :type students: List[List[int]]
        :rtype: int
        """
        
        cnt = {}
        for student, bench in students:
            if bench not in cnt:
                cnt[bench] = set()
            cnt[bench].add(student)
        
        res = 0
        for bench in cnt:
            res = max(res, len(cnt[bench]))
        return res
```
