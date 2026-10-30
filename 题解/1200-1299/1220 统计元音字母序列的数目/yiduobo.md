---
title: "1220. 统计元音字母序列的数目"
aliases: ["yiduobo的每日leetcode 1220.统计元音字母序列的数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/383054537"
zhihu_id: "383054537"
zhihu_title: "yiduobo的每日leetcode 1220.统计元音字母序列的数目"
question_id: "1220"
question: "统计元音字母序列的数目"
problem_url: "https://leetcode.cn/problems/count-vowels-permutation/"
created: "2021-06-22T22:25:55+08:00"
updated: "2021-06-22T22:25:55+08:00"
upvotes: 1
comments: 0
---

# 1220. 统计元音字母序列的数目

> **[yiduobo的每日leetcode 1220.统计元音字母序列的数目](https://zhuanlan.zhihu.com/p/383054537) · 知乎 · 2021-06-22 · 赞同 1**
> 力扣：[1220. 统计元音字母序列的数目](https://leetcode.cn/problems/count-vowels-permutation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1220.统计元音字母序列的数目

[力扣](https://leetcode-cn.com/problems/count-vowels-permutation/)

动态规划算法是很容易想到。令f[j][0]、f[j][1]、f[j][2]、f[j][3]、f[j][4]分别表示长度为j，且最后一个字符为a、e、i、o、u的字母序列的数目。

那么：

1、对于f[j][0]，由于a只能出现在e、i或者u后面，因此就有

f[j][0] \= f[j - 1][1] + f[j - 1][2] + f[j - 1][4]

2、对于f[j][1]，由于e只能出现在a或者i后面，因此就有

f[j][1] \= f[j - 1][0] + f[j - 1][2]

3、对于f[j][2]，由于i只能出现在e或者o后面，因此就有

f[j][2] \= f[j - 1][1] + f[j - 1][3]

4、对于f[j][3]，由于o只能出现在i后面，因此就有

f[j][3] \= f[j - 1][2]

5、对于f[j][4]，由于u只能出现在i或者o后面，因此就有

f[j][4] \= f[j - 1][2] + f[j - 1][3]

另外，这里的状态转移方程是可以写成矩阵的形式的，即

[a, e, i, o, u] \* M \= [a', e', i', o', u']

通过上面的状态转移方程可以解得M为

\[\[0, 1, 0, 0, 0\],

[1, 0, 1, 0, 0],

[1, 1, 0, 1, 1],

[0, 0, 1, 0, 1],

\[1, 0, 0, 0, 0\]\]

这里有一个小技巧。当前后的值矩阵的元素系数都是1时，那么可以将每一位对应的转移方程的系数竖着拼起来，就可以得到矩阵M。例如M的第一列为0, 1, 1, 0, 1，恰好就对应f[j][0]状态转移方程

f[j][0] \= 0 \* f[j - 1][0] + 1 \* f[j - 1][1] + 1 \* f[j - 1][2] + 0 \* f[j - 1][3] + 1 \* f[j - 1][4]

得到M之后，就可以使用快速幂来进行加速了。快速幂完成之后得到最终的转移矩阵，由于初始状态下a、e、i、o、u的数目都是1，因此最终答案就是转移矩阵中所有元素之和。

最后附上python代码：

```python
class Solution(object):
    def countVowelPermutation(self, n):
        """
        :type n: int
        :rtype: int
        """

        if n == 1:
            return 5

        mod = 10 ** 9 + 7

        f = [[0, 1, 0, 0, 0],
             [1, 0, 1, 0, 0],
             [1, 1, 0, 1, 1],
             [0, 0, 1, 0, 1],
             [1, 0, 0, 0, 0]]

        final = self.quick_pow(f, n - 1, mod)
        res = 0
        for line in final:
            for num in line:
                res += num
                res %= mod
        
        return res
    
    def quick_pow(self, base, n, mod):
        if n == 1:
            return base
        
        tmp = self.quick_pow(base, n / 2, mod)
        l = len(base)
        res = [[0] * l for _ in range(l)]
        for i in range(l):
            for j in range(l):
                for k in range(l):
                    res[i][j] += tmp[i][k] * tmp[k][j]
                    res[i][j] %= mod

        if n % 2 == 0:
            return res

        tmp = [[0] * l for _ in range(l)]
        for i in range(l):
            for j in range(l):
                for k in range(l):
                    tmp[i][j] += res[i][k] * base[k][j]
                    tmp[i][j] %= mod
        
        return tmp
```
