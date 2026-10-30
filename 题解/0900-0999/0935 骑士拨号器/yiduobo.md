---
title: "935. 骑士拨号器"
aliases: ["yiduobo的每日leetcode 935.骑士拨号器"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "leetcode/matrix", "题单/动态规划", "题单/动态规划/六-状态机-DP", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/357643959"
zhihu_id: "357643959"
zhihu_title: "yiduobo的每日leetcode 935.骑士拨号器"
question_id: "935"
question: "骑士拨号器"
problem_url: "https://leetcode.cn/problems/knight-dialer/"
difficulty: "Medium"
created: "2021-03-16T23:41:48+08:00"
updated: "2021-03-16T23:41:48+08:00"
upvotes: 0
comments: 0
---

# 935. 骑士拨号器

> **[yiduobo的每日leetcode 935.骑士拨号器](https://zhuanlan.zhihu.com/p/357643959) · 知乎 · 2021-03-16 · 赞同 0**
> 力扣：[935. 骑士拨号器](https://leetcode.cn/problems/knight-dialer/) · Medium · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推到矩阵快速幂！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

935.骑士拨号器

[力扣](https://leetcode-cn.com/problems/knight-dialer/)

动态规划的方法是很容易想到的，令f[i][j]表示长度为i + 1，以j结尾的电话号码有多少种，那么对于f[i][j]：

当j \= 5时，只有当i等于0时才有意义，当号码长度大于1时不可能以5结尾

对于其他的号码，则可以列出下面的式子：

f[i][0] \= f[i - 1][4] + f[i - 1][6]

f[i][1] \= f[i - 1][6] + f[i - 1][8]

f[i][2] \= f[i - 1][7] + f[i - 1][9]

f[i][3] \= f[i - 1][4] + f[i - 1][8]

f[i][4] \= f[i - 1][3] + f[i - 1][9] + f[i - 1][0]

f[i][6] \= f[i - 1][1] + f[i - 1][7] + f[i - 1][0]

f[i][7] \= f[i - 1][2] + f[i - 1][6]

f[i][8] \= f[i - 1][1] + f[i - 1][3]

f[i][9] \= f[i - 1][2] + f[i - 1][4]

到了这里，就得到了一种时间复杂度O(n)，空间复杂度O(n)的做法了。

当然，这里很自然可以想到使用矩阵乘法进行加速，但是在当前的状态转移方程下，每一轮都有10个变量，意味着需要构造一个10 \* 10的转移矩阵，而这个矩阵乘法就需要1000次运算了，显然是不合算的，因此需要想办法进行优化。

注意到这里的拨号键盘左右应该是完全对称的，那么就有

f[i][1] \= f[i][3]

f[i][4] \= f[i][6]

f[i][7] \= f[i][9]

接下来，对于f[i][8]和f[i][2]就有

f[i][8] \= f[i - 1][1] + f[i - 1][3] \= 2 \* f[i - 1][1]

f[i][2] \= f[i - 1][7] + f[i - 1][9] \= 2 \* f[i - 1][7]

再往下迭代一轮，可以发现

f[i][8] \= 2 \* f[i - 1][1] \= 2 \* (f[i - 2][6] + f[i - 2][8])

f[i][2] \= 2 \* f[i - 1][7] \= 2 \* (f[i - 1][2] + f[i - 1][6])

由于f[0][2] \= f[0][8]，而且也很容易得知f[1][2] \= f[1][8]，那么就可以推出f[i][2] \= f[i][8]

更一步地，对于f[1]和f[7]，

f[i][1] \= f[i - 1][6] + f[i - 1][8]

f[i][7] \= f[i - 1][2] + f[i - 1][6]

就有f[i][1] \= f[i][7]

至此，就有了三组等式

f[i][1] \= f[i][3] \= f[i][7] \= f[i][9]

f[i][2] \= f[i][8]

f[i][4] \= f[i][6]

那么我们最终就只需要求出f[I][0]、f[i][1]、f[i][2]、f[i][4]的值即可，此时的状态转移方程为：

f[i][0] \= f[i - 1][4] + f[i - 1][6] \= 2 \* f[i - 1][4]

f[i][1] \= f[i - 1][6] + f[i - 1][8] \= f[i - 1][4] + f[i - 1][2]

f[i][2] \= f[i - 1][7] + f[i - 1][9] \= 2 \* f[i - 1][1]

f[i][4] \= f[i - 1][3] + f[i - 1][9] + f[i - 1][0] \= 2 \* f[i - 1][1] + f[i - 1][0]

这样一来，就可以通过构造一个4\*4的状态转移矩阵来进行矩阵乘法了。根据上面的式子，有

f[i][0] \= 0 \* f[i - 1][0] + 0 \* f[i - 1][1] + 0 \* f[i - 1][2] + 2 \* f[i - 1][4]

f[i][1] \= 0 \* f[i - 1][0] + 0 \* f[i - 1][1] + 1 \* f[i - 1][2] + 1 \* f[i - 1][4]

f[i][2] \= 0 \* f[i - 1][0] + 2 \* f[i - 1][1] + 0 \* f[i - 1][2] + 0 \* f[i - 1][4]

f[i][4] \= 1 \* f[i - 1][0] + 2 \* f[i - 1][1] + 0 \* f[i - 1][2] + 0 \* f[i - 1][4]

可以得知状态转移矩阵为

[0, 0, 0, 2]

[0, 0, 1, 1]

[0, 2, 0, 0]

[1, 2, 0, 0]

接下来，就是对上面这个矩阵进行快速幂，设快速幂完成之后得到的矩阵为A，由于初始的f为4个1，因此最终的f应该是sum(A[0])，sum(A[1])，sum(A[2])以及sum(A[3])。

又由于最终的答案需要计算1次f[0]，4次f[1]，2次f[2]以及2次f[4]，因此最终答案就是

sum(A[0]) + 4 \* sum(A[1]) + 2 \* sum(A[2]) + 2 \* sum(A[3])

到了这里，就得到了一种O(log(n))的做法了

最后附上python代码：

```python
class Solution(object):
    def knightDialer(self, n):
        """
        :type n: int
        :rtype: int
        """

        if n == 1:
            return 10

        mod = 10 ** 9 + 7

        #f[i][0] = 2f[i - 1][4]
        #f[i][1] = f[i - 1][4] + f[i - 1][2]
        #f[i][2] = 2f[i - 1][1]
        #f[i][4] = 2f[i - 1][1] + f[i - 1][0]

        x = [[0, 0, 0, 2], [0 ,0, 1, 1], [0, 2, 0, 0], [1, 2, 0, 0]]
        now = self.quickPow(n - 1, x, mod)
        return (sum(now[0]) + 4 * sum(now[1]) + 2 * sum(now[2]) + 2 * sum(now[3])) % mod

    def quickPow(self, n, base, mod):
        if n == 1:
            return base[:]
        
        now = self.quickPow(n / 2, base, mod)
        l = len(base)
        tmp = [[0] * l for _ in range(l)]
        for i in range(l):
            for j in range(l):
                for k in range(l):
                    tmp[i][j] += now[i][k] * now[k][j]
                tmp[i][j] %= mod
        
        if n % 2 == 0:
            return tmp[:]
        
        now = [[0] * l for _ in range(l)]
        for i in range(l):
            for j in range(l):
                for k in range(l):
                    now[i][j] += tmp[i][k] * base[k][j]
                now[i][j] %= mod
        return now[:]
```
