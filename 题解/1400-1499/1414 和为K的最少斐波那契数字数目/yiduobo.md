---
title: "1414. 和为K的最少斐波那契数字数目"
aliases: ["yiduobo的每日leetcode 1414.和为K的最少斐波那契数字数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/406854950"
zhihu_id: "406854950"
zhihu_title: "yiduobo的每日leetcode 1414.和为K的最少斐波那契数字数目"
question_id: "1414"
question: "和为K的最少斐波那契数字数目"
problem_url: "https://leetcode.cn/problems/find-the-minimum-number-of-fibonacci-numbers-whose-sum-is-k/"
created: "2021-09-04T21:09:38+08:00"
updated: "2021-09-04T21:09:38+08:00"
upvotes: 0
comments: 0
---

# 1414. 和为K的最少斐波那契数字数目

> **[yiduobo的每日leetcode 1414.和为K的最少斐波那契数字数目](https://zhuanlan.zhihu.com/p/406854950) · 知乎 · 2021-09-04 · 赞同 0**
> 力扣：[1414. 和为K的最少斐波那契数字数目](https://leetcode.cn/problems/find-the-minimum-number-of-fibonacci-numbers-whose-sum-is-k/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1414.和为K的最少斐波那契数字数目

[力扣](https://leetcode-cn.com/problems/find-the-minimum-number-of-fibonacci-numbers-whose-sum-is-k/)

题目要求选出若干斐波那契数列中的数字，使得这些数字的和为K，且数字的个数最少。

首先，答案中必然不会出现相邻的两项，因为若存在相邻的两项f[k]以及f[k + 1]，由于存在f[k + 2] \= f[k] + f[k + 1]，因此使用f[k + 2]来替代f[k]和f[k + 1]显然是更好的做法。

那么此时的答案可以写成

k \= f[1] \* a[1] + f[2] \* a[2] + ... + f[n] \* a[n]

这里的f[n]是最大的小于等于k的数列项，且这里的不会出现相邻的相邻a同时大于0。

不妨设式子中的某一项t的系数a[t] > 1，那么就有

f[t] \* a[t] \= (f[t - 1] + f[t - 2]) + f[t] \* (a[t] - 1)

\= f[t - 2] + (f[t - 1] + f[t]) + f[t] \* (a[t] - 2)

\= f[t - 2] + f[t + 1] + f[t] \* (a[t] - 2)

更进一步的，若此时的a[t] > 2，那么就有

f[t] \* a[t] \= f[t - 2] + f[t + 1] + f[t] + f[t] \* (a[t] - 3)

\= f[t - 2] + f[t + 2] + f[t] \* (a[t] - 3])

这样一来，原始的a[t]项f[t]就可以转化成1 + 1+ a[t] - 3 \= a[t] - 1项，是更优的选取方案。这就说明了答案中的所有系数a都小于等于2。

另外，若当a[t] \= 2时，答案中的a[t + 2]必然为0，否则就有

f[t] \* 2 + f[t + 2] \= f[t - 2] + f[t + 1] + f[t + 2] \= f[t - 2] + f[t + 3]

相比之下直接使用f[t - 2]以及f[t + 3]是更优的方案，因此当a[t]等于2时，a[t + 2]必然为0。

接下来，可以证明这里的a[n]必然大于0。不妨设a[n]等于0，为了使得剩下的式子最大：

1、当n为奇数时：

rest \= f[n - 1] \* a[n - 1] + f[n - 3] \* a[n - 3] + ... + f[2] \* a[2]

首先，这里的a[n - 1]必然为1，因为a[n - 1]等于2时，可以写成a[n] + a[n - 2]的形式，也就是说相当于选择了一个a[n]，与前提不符。

接下来，根据上面a[t] \= 2时a[t + 2]必须为0的结论，式子中的a必然都为1，那么就有

rest \= f[n - 1] + f[n - 3] + ... + f[4] + f[2]

那么就有

rest + f[1] \= f[n - 1] + f[n - 3] + ... + f[4] + f[2] + f[1]

\= f[n - 1] + f[n - 3] + ... + f[4] + f[3]

\= f[n - 1] + f[n - 2]

\= f[n]

即rest \= f[n] - 1 \< f[n] \<\= k

这就说明如果不选择f[n]，剩下式子的和必然是小于k的，因此必须要选择f[n]

2、当n为偶数时：

rest \= f[n - 1] \* a[n - 1] + f[n - 3] \* a[n - 3] + ... + f[1] \* a[1]

同样地，这里的a必然都是1，即

rest \= f[n - 1] + f[n - 3] + ... + f[5] + f[3] + f[1]

由于f[1] \= f[2]，那么就有

rest \= f[n - 1] + f[n - 3] + ... + f[5] + f[3] + f[2]

\= f[n - 1] + f[n - 3] + ... + f[5] + f[4]

\= f[n - 1] + f[n - 2]

\= f[n]

当f[n]恰好就等于k时，显然单选一个f[n]是最优答案；当f[n] \< k时，rest \= f[n] \< k，也就是说不选择f[n]，剩下式子的和必然小于k，因此必须要选择f[n]。

根据上面的结论，我们每一轮都必须选择最大的，且小于等于k的数列项，然后更新k，直到k为0为止。于是我们可以先预处理出数列中的f[3]到f[n]，然后从n开始向下遍历，逐个选出符合条件的项。

最后附上python代码：

```python
class Solution(object):
    def findMinFibonacciNumbers(self, k):
        """
        :type k: int
        :rtype: int
        """

        f = [1, 1]
        while f[-1] < k:
            f.append(f[-1] + f[-2])
        
        res = 0
        p = 1
        while k > 0:
            while k < f[-p]:
                p += 1
            k -= f[-p]
            res += 1
        
        return res
```
