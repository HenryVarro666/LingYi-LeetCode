---
title: "2019. 解出数学表达式的学生分数"
aliases: ["yiduobo的每日leetcode 2019.解出数学表达式的学生分数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/八-区间-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/506284598"
zhihu_id: "506284598"
zhihu_title: "yiduobo的每日leetcode 2019.解出数学表达式的学生分数"
question_id: "2019"
question: "解出数学表达式的学生分数"
problem_url: "https://leetcode.cn/problems/the-score-of-students-solving-math-expression/"
difficulty: "Hard"
rating: 2584
created: "2022-04-27T23:18:00+08:00"
updated: "2022-04-27T23:18:00+08:00"
upvotes: 0
comments: 0
---

# 2019. 解出数学表达式的学生分数

> **[yiduobo的每日leetcode 2019.解出数学表达式的学生分数](https://zhuanlan.zhihu.com/p/506284598) · 知乎 · 2022-04-27 · 赞同 0**
> 力扣：[2019. 解出数学表达式的学生分数](https://leetcode.cn/problems/the-score-of-students-solving-math-expression/) · Hard · 灵茶山艾府：[区间 DP+哈希表](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2019.解出数学表达式的学生分数

[力扣](https://leetcode-cn.com/problems/the-score-of-students-solving-math-expression/)

本题需要找出表达式的正确的表达式结果以及所有运算顺序下的可能表达式结果，对于这两个问题分开来看。

首先是正确结果。由于题目中仅有加号和乘号，而乘号的优先级较高，那么按处理表达式的常规做法，使用一个栈来辅助运算。从头开始向后一趟遍历，当出现加号时，由于另一个值还不能确定，因此需要将当前的结果压入栈中。当出现乘号时，另一个值必然是下一个数，因此可以直接执行乘法运算。全部遍历完成后，将当前值与栈中的值累加起来，就是最终的正确结果。

接下来是所有可能的结果。这是一个经典的区间动态规划问题，令f[i][j]表示第i到第j个数可能得到的所有可能运算结果。对于f[i][j]：

1、当i \= j时，f[i][j]就是区间内唯一的这个数

2、当i \= j - 1时，f[i][j]就是区间这两个数执行加法或者乘法的结果

3、其他情况下，则需要枚举分割点cut_pos，然后枚举f[i][cut_pos]以及f[cut_pos + 1][j]中的所有数对，并将相应的运算结果加入到f[i][j]中。在这里有一个小优化是由于题目保证了答案小于等于1000，那么f[i][j]中也只需要保留小于等于1000的数

动态规划完成后，f[0][n - 1]就是所有可能的运算结果。

接下来只需要遍历answer中的所有值，按照题目给的打分规则计算最终得分即可。

最后附上python代码：

```python
class Solution(object):
    def scoreOfStudents(self, s, answers):
        """
        :type s: str
        :type answers: List[int]
        :rtype: int
        """

        num_list = []
        op_list = []
        now = 0
        for char in s:
            if char == '+' or char == '*':
                num_list.append(now)
                op_list.append(char)
                now = 0
            else:
                now = now * 10 + int(char)
            
        num_list.append(now)
        now = num_list[0]
        stack = []
        n = len(num_list)
        for index in range(1, n):
            if op_list[index - 1] == '+':
                stack.append(now)
                now = num_list[index]
            else:
                now *= num_list[index]
        
        correct_ans = now + sum(stack)
        
        f = [[set() for _ in range(n)] for _ in range(n)]
        for l in range(1, n + 1):
            for left in range(n - l + 1):
                right = left + l - 1
                if left == right:
                    f[left][right].add(num_list[left])
                else:
                    for cut_pos in range(left, right):
                        for x in f[left][cut_pos]:
                            for y in f[cut_pos + 1][right]:
                                if op_list[cut_pos] == '+':
                                    if x + y <= 1000:
                                        f[left][right].add(x + y)
                                else:
                                    if x * y <= 1000:
                                        f[left][right].add(x * y)

        res = 0
        for ans in answers:
            if ans == correct_ans:
                res += 5
            elif ans in f[0][n - 1]:
                res += 2
        
        return res
```
