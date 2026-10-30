---
title: "1700. 无法吃午餐的学生数量"
aliases: ["yiduobo的每日leetcode 1700.无法吃午餐的学生数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/447846649"
zhihu_id: "447846649"
zhihu_title: "yiduobo的每日leetcode 1700.无法吃午餐的学生数量"
question_id: "1700"
question: "无法吃午餐的学生数量"
problem_url: "https://leetcode.cn/problems/number-of-students-unable-to-eat-lunch/"
created: "2021-12-20T23:54:18+08:00"
updated: "2021-12-20T23:54:18+08:00"
upvotes: 0
comments: 0
---

# 1700. 无法吃午餐的学生数量

> **[yiduobo的每日leetcode 1700.无法吃午餐的学生数量](https://zhuanlan.zhihu.com/p/447846649) · 知乎 · 2021-12-20 · 赞同 0**
> 力扣：[1700. 无法吃午餐的学生数量](https://leetcode.cn/problems/number-of-students-unable-to-eat-lunch/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1700.无法吃午餐的学生数量

[力扣](https://leetcode-cn.com/problems/number-of-students-unable-to-eat-lunch/)

由于题目的规模很小，直接模拟也是可以的，不过还有更好的做法。注意到学生这里是轮流查询的，也就是说对于当前栈顶的三明治，只要学生当中还有一位学生喜欢这种三明治，那么这个三明治就一定会被吃掉。换言之，只有当栈顶三明治为1，学生全都是0，或者栈顶三明治为0，学生全都是1时才会出现无法吃午餐的状况。也就是说，从栈顶开始计数，如果某一时刻三明治0的数量大于学生0的数量，或者三明治1的数量大于学生1的数量，那么此时栈顶的三明治就没人吃了，那么此时剩下的三明治数量即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def countStudents(self, students, sandwiches):
        """
        :type students: List[int]
        :type sandwiches: List[int]
        :rtype: int
        """

        n = len(students)
        one_students = sum(students)
        zero_students = n - one_students

        one = zero = 0
        for index in range(n):
            sandwich = sandwiches[index]
            if sandwich == 0:
                zero += 1
            else:
                one += 1
            
            if one > one_students or zero > zero_students:
                return n - index
        
        return 0
```
