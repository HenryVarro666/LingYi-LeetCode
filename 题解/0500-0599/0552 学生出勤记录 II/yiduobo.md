---
title: "552. 学生出勤记录II"
aliases: ["yiduobo的每日leetcode 552.学生出勤记录II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "leetcode/matrix", "题单/动态规划", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/261248921"
zhihu_id: "261248921"
zhihu_title: "yiduobo的每日leetcode 552.学生出勤记录II"
question_id: "552"
question: "学生出勤记录 II"
problem_url: "https://leetcode.cn/problems/student-attendance-record-ii/"
difficulty: "Hard"
created: "2020-10-11T14:03:07+08:00"
updated: "2020-10-11T14:03:07+08:00"
upvotes: 1
comments: 0
---

# 552. 学生出勤记录II

> **[yiduobo的每日leetcode 552.学生出勤记录II](https://zhuanlan.zhihu.com/p/261248921) · 知乎 · 2020-10-11 · 赞同 1**
> 力扣：[552. 学生出勤记录 II](https://leetcode.cn/problems/student-attendance-record-ii/) · Hard · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推，再到矩阵快速幂优化！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

552.学生出勤记录II <https://leetcode-cn.com/problems/student-attendance-record-ii/>

动态规划的题目，首先理一理这里可能出现的状态：

0：没有缺席，且没有累积的迟到

1：没有缺席，但最近一天迟到了

2：没有缺席，但最近两条都迟到了

3：缺席一次，但没有累积的迟到

4：缺席一次，且最近一天迟到了

5：缺席一次，且最近两天都迟到了

那么可以使用f[i][j]表示第i天时达成状态j有多少种可能，其中j属于上面这6种中的一种。

对于f[i][j]：

0：想达成f[i][0]，就必须保证之前没有过缺席，且最近这一天是P，那么就有

f[i][0] \= f[i - 1][0] + f[i - 1][1] + f[i - 1][2]

即到昨天为止都没有过缺席，那么不管累积了几次迟到，今天的P都可以将其清零

1：想达成f[i][1]，那么之前必须没有过缺席，今天必须迟到且昨天没有累积过迟到，于是有

f[i][1] \= f[i - 1][0]

2：与上面类似，之前不能出现缺席，今天必须迟到且截止昨天累积了一次迟到，于是有

f[i][2] \= f[i - 1][1]

3：想达成f[i][3]，那么可以是之前从未缺席，但今天缺席了，或者截止至昨天缺席过一次，且今天正常出席，那么就有

f[i][3] \= f[i - 1][0] + f[i - 1][1] + f[i - 1][2] + f[i - 1][3] + f[i - 1][4] + f[i - 1][5]

前三项表示之前从未缺席，但今天缺席了，顺便抵消掉了之前累积的迟到。

后三项则表示之前缺席过一次，且今天正常出勤，那么累积的迟到清零。

4：与情况1类似，不同的是之前必须缺席过一次，于是有

f[i][4] \= f[i - 1][3]

5：与情况2类似，也是需要缺席过一次，于是有

f[i][5] \= f[i - 1][4]

到了这里，就有一个递推的做法了。

注意到这里的每天的状态都只与昨天的状态有关，因此可以滚动起来。不过注意到n最大可以到100000，那么这里采用矩阵乘法加快速幂的做法（可以参考这里：[yiduobo：yiduobo的每日leetcode 509.斐波那契数](https://zhuanlan.zhihu.com/p/259578419)）是更好的。

需要注意的是，与之前计算斐波那契数列不同，斐波那契数列需要之前的两项计算当前这一项，因此需要将之前两项都包含在矩阵中。而这一题则只需要前一天的状态，因此只需要将前一天的数据包含进来。但是相对的，前一天的状态有6维，因此最终需要整理成一个1 \* 6的矩阵的形式，即

A \= \[f\[i - 1\]\[0\], f\[i - 1\]\[1\], f\[i - 1\]\[2\], f\[i - 1\]\[3\], f\[i - 1\]\[4\], f\[i - 1\]\[5\]\]

目标状态同样是1 \* 6的形式，为

B \= \[f\[i\]\[0\], f\[i\]\[1\], f\[i\]\[2\], f\[i\]\[3\], f\[i\]\[4\], f\[i\]\[5\]\]

我们的目标就是找到一个6 \* 6的矩阵X，使得A \* X \= B

根据的定义，我们可以得到下面6个式子。为了简单起见，后续都省略掉A和B的第一维0：

B[0] \= ΣA[k] \* X[k][0]

B[1] \= ΣA[k] \* X[k][1]

B[2] \= ΣA[k] \* X[k][2]

B[3] \= ΣA[k] \* X[k][3]

B[4] \= ΣA[k] \* X[k][4]

B[5] \= ΣA[k] \* X[k][5]

将f带入A和B，就有

X[0][0] \= X[1][0] \= X[2][0] \= 1

X[0][1] \= 1

X[1][2] \= 1

X[0][3] \= X[1][3] \= X[2][3] \= X[3][3] \= X[4][3] \= X[5][3] \= 1

X[3][4] \= 1

X[4][5] \= 1

即X \= \[\[1, 1, 0, 1, 0, 0\],

[1, 0, 1, 1, 0, 0],

[1, 0, 0, 1, 0, 0],

[0, 0, 0, 1, 1, 0],

[0, 0, 0, 1, 0, 1],

\[0, 0, 0, 1, 0, 0\]\]

我们初始状态为A \= [1, 0, 0, 0, 0, 0]，而最终状态B \= A \* X \* X \* ... \* X，最终答案就是B中所有元素之后。那么我们可以对中间的n个X执行快速幂，求出最终的final_X。又由于A中只有第0个元素是1，因此答案就是final_X的第0列元素之和。

快速幂的做法可以参考上面的509题，这里就不再重复了。

提交之后发现只要52ms，相比O(n)的做法就体现出O(logn)做法的强大之处了。

最后附上python代码：

```python
class Solution(object):
    def checkRecord(self, n):
        """
        :type n: int
        :rtype: int
        """

        X = [[1, 1, 0, 1, 0, 0],
             [1, 0, 1, 1, 0, 0],
             [1, 0, 0, 1, 0, 0],
             [0, 0, 0, 1, 1, 0],
             [0, 0, 0, 1, 0, 1],
             [0, 0, 0, 1, 0, 0]]
        mod = 10 ** 9 + 7
        return sum(self.quick_pow(X, n, mod)[0]) % mod

    def quick_pow(self, base, p, mod):
        if p == 1:
            return base
        
        tmp = self.quick_pow(base, p / 2, mod)
        res = [[0] * 6 for _ in range(6)]
        for i in range(6):
            for j in range(6):
                for k in range(6):
                    res[i][j] += tmp[i][k] * tmp[k][j]
                    res[i][j] %= mod

        if p % 2 == 0:
            return res
        
        tmp = [[0] * 6 for _ in range(6)]
        for i in range(6):
            for j in range(6):
                for k in range(6):
                    tmp[i][j] += res[i][k] * base[k][j]
                    tmp[i][j] %= mod
        
        return tmp
```
