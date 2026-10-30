---
title: "690. 员工的重要性"
aliases: ["yiduobo的每日leetcode 690.员工的重要性"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/tree", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/hash-table", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/308481280"
zhihu_id: "308481280"
zhihu_title: "yiduobo的每日leetcode 690.员工的重要性"
question_id: "690"
question: "员工的重要性"
problem_url: "https://leetcode.cn/problems/employee-importance/"
difficulty: "Medium"
created: "2020-11-23T21:30:08+08:00"
updated: "2020-11-23T21:30:08+08:00"
upvotes: 0
comments: 0
---

# 690. 员工的重要性

> **[yiduobo的每日leetcode 690.员工的重要性](https://zhuanlan.zhihu.com/p/308481280) · 知乎 · 2020-11-23 · 赞同 0**
> 力扣：[690. 员工的重要性](https://leetcode.cn/problems/employee-importance/) · Medium · 灵茶山艾府：[哈希表+DFS（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

690.员工的重要性

[力扣](https://leetcode-cn.com/problems/employee-importance/)

题目保证每个员工最多有一个上级，可能有多个下级，那么如果将员工视为节点，那么这就是由多棵树组成的森林。题目要求的员工的重要性，就是森林中某棵子树的节点元素之和，于是从该节点开始向下bfs或者dfs即可。

最后附上python代码：

```python
"""
# Definition for Employee.
class Employee(object):
    def __init__(self, id, importance, subordinates):
    	#################
        :type id: int
        :type importance: int
        :type subordinates: List[int]
        #################
        self.id = id
        self.importance = importance
        self.subordinates = subordinates
"""

class Solution(object):
    def getImportance(self, employees, id):
        """
        :type employees: List[Employee]
        :type id: int
        :rtype: int
        """

        emp_dict = {}
        for emp in employees:
            emp_dict[emp.id] = emp

        l = 0
        r = 1
        res = 0
        q = [emp_dict[id]]
        while l < r:
            now = q[l]
            l += 1
            res += now.importance
            for sub in now.subordinates:
                q.append(emp_dict[sub])
                r += 1
        
        return res
```
