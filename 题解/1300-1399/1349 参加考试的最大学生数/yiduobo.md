---
title: "1349. 参加考试的最大学生数"
aliases: ["yiduobo的每日leetcode 1349.参加考试的最大学生数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/图论算法", "题单/动态规划/九-状态压缩-DP-状压-DP", "题单/图论算法/八-网络流"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/397616058"
zhihu_id: "397616058"
zhihu_title: "yiduobo的每日leetcode 1349.参加考试的最大学生数"
question_id: "1349"
question: "参加考试的最大学生数"
problem_url: "https://leetcode.cn/problems/maximum-students-taking-exam/"
difficulty: "Hard"
rating: 2386
created: "2021-08-08T17:46:35+08:00"
updated: "2021-08-08T17:46:35+08:00"
upvotes: 1
comments: 0
---

# 1349. 参加考试的最大学生数

> **[yiduobo的每日leetcode 1349.参加考试的最大学生数](https://zhuanlan.zhihu.com/p/397616058) · 知乎 · 2021-08-08 · 赞同 1**
> 力扣：[1349. 参加考试的最大学生数](https://leetcode.cn/problems/maximum-students-taking-exam/) · Hard · 灵茶山艾府：[教你一步步思考动态规划：从记忆化搜索到递推（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1349.参加考试的最大学生数

[力扣](https://leetcode-cn.com/problems/maximum-students-taking-exam/)

动态规划的题目。由于每一行最多只有8个位置，那么可以使用二进制表示来进行状态压缩，那么状态就是f[i][state]表示前i行，最后一行座位状态为state时可以参加考试的最大学生数。

接下来，我们考虑如何从f[i][state]得到f[i + 1][state']。一个自然的想法是枚举下一行中所有的可能状态，一共是256种，然后检测枚举的状态state'是否和上一行的state兼容，若兼容，那么就用f[i][state] + v(state')来更新f[i + 1][state']，其中v(state')表示state'二进制表示下1的数目，也就是对应了新的一行的学生数目。

我在这里采用的是使用搜索回溯来寻找f[i + 1][state']中合法的state'，具体为从左向右逐个扫描，尝试跳过这个位置或者在这个位置上安排学生，具体为：

1、若当前处理的位置p \= n，那么说明这一行已经安排好了，那么同样地，使用f[i][state] + v(state')来更新f[i +1][state']

2、若当前处理的位置p \< n，那么可以直接跳过这个位置，那么此时的state'不发生变化

3、若当前处理的位置p \< n，那么也可以尝试安排学生坐到这个位置上。

根据题目要求，当前位置的座位必须是好的，因此先需要满足

seats[i][p] \= '.'

接下来，由于上一行的第p - 1和第p + 1个位置不能坐人，因此需要满足

state & (1 \<\< (p - 1)) \= 0，state&(1 \<\< (p + 1)) \= 0

另外，本行的第p - 1个位置也不能坐人，因此还需要满足

state' & (1 \<\< (p - 1)) \= 0

若满足上面的几个条件，那么我们就可以在第p个位置是安排学生，此时就需要更新state'

无论当前位置是否安排的学生，我们都要继续处理第p + 1个位置

全部计算完成后，答案就是max(f[-1])

另外，注意到这里每一行的状态只与上一行有关，因此可以省去i这一维，使用滚动数组来优化空间。

最后附上python代码：

```python
class Solution(object):
    def maxStudents(self, seats):
        """
        :type seats: List[List[str]]
        :rtype: int
        """

        m = len(seats)
        n = len(seats[0])
        g = [None] * (1 << n)
        g[0] = 0
        for level in range(m):
            f = [None] * (1 << n)
            for state in range(1 << n):
                if g[state] is not None:
                    self.dfs(0, n, 0, 0, state, g[state], f, seats[level])
        
            g = f[:]
        
        return max(g)
    
    def dfs(self, p, n, now_state, now_v, last_state, last_v, f, seats):
        if p == n:
            if f[now_state] is None or f[now_state] < now_v + last_v:
                f[now_state] = now_v + last_v
            return
        
        self.dfs(p + 1, n, now_state, now_v, last_state, last_v, f, seats)
        if seats[p] == '.':
            if p > 0 and (last_state & (1 << (p - 1))):
                return
            if p < n - 1 and (last_state & (1 << (p + 1))):
                return
            if p > 0 and (now_state & (1 << (p - 1))):
                return
            self.dfs(p + 1, n, now_state | (1 << p), now_v + 1, last_state, last_v, f, seats)
```
