---
title: "1467. 两个盒子中球的颜色数相同的概率"
aliases: ["yiduobo的每日leetcode 1467.两个盒子中球的颜色数相同的概率"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/413977222"
zhihu_id: "413977222"
zhihu_title: "yiduobo的每日leetcode 1467.两个盒子中球的颜色数相同的概率"
question_id: "1467"
question: "两个盒子中球的颜色数相同的概率"
problem_url: "https://leetcode.cn/problems/probability-of-a-two-boxes-having-the-same-number-of-distinct-balls/"
created: "2021-09-25T23:40:15+08:00"
updated: "2021-09-25T23:40:15+08:00"
upvotes: 1
comments: 0
---

# 1467. 两个盒子中球的颜色数相同的概率

> **[yiduobo的每日leetcode 1467.两个盒子中球的颜色数相同的概率](https://zhuanlan.zhihu.com/p/413977222) · 知乎 · 2021-09-25 · 赞同 1**
> 力扣：[1467. 两个盒子中球的颜色数相同的概率](https://leetcode.cn/problems/probability-of-a-two-boxes-having-the-same-number-of-distinct-balls/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1467.两个盒子中求的颜色数相同的概率

[力扣](https://leetcode-cn.com/problems/probability-of-a-two-boxes-having-the-same-number-of-distinct-balls/)

看上去应该可以用组合数学的方法直接把答案算出来，但是没有想出来具体的做法，只好老老实实用动态规划去做。

注意到这里一共只有8种球，每种球的个数在0到6之间，这也就意味着可以使用一个8位7进制的数来表示当前选择的球并进行动态规划。这种做法的时间复杂度为O(7^n \* n)，在极限情况下是比较危险的。

注意到这里其实并不需要关心具体拿球的方案，而只需要直到两个盒子中球颜色的差值，那么可以重新设定状态为f[i][j][k]表示从前i中颜色的球中拿出j个放入盒子一，剩下的放入盒子二，且两个盒子中球的颜色数相差为k时所有的方案数，那么对于f[i][j][k]：

1、第i种球一个都不放到盒子一当中，此时这一共balls[i]个球就要全部放到盒子二当中。不妨设前i种球一共有s[i]个，根据状态的定义，此时盒子一当中有j个球，于是在加入这balls[i]个球之后盒子二中应该有s[i] - j个球，即加入这balls[i]个球之前盒子二中有s[i] - j - balls[i]个球。

此时就有

f[i][j][k] \= f[i - 1][j][k + 1] \* p

这里k + 1的理由是由于这种颜色的球全部加入了盒子二当中，因此将会产生一种颜色差。

p则表示对于f[i - 1][j][k + 1]对应的的盒子二一共s[i] - j - balls[i]个球所形成的的各种排列，新插入balls[i]个球能得到的方案数目。

现在考虑求解p：第一个球有s[i] - j - balls[i] + 1个位置可以插入，第二个球在这个基础上有s[i] - j - balls[i] + 2个位置可以插入，依次类推，即

(s[i] - j - balls[i] + 1) \* (s[i] - j - balls[i] + 2) \* ... \* (s[i] - j - balls[i] + balls[i])

也就是(s[i] - j)！/ (s[i] - j - balls[i])！

另外，上面这些插入方法会出现重复，这是由于新插入这种球应该是组合而不是排列，于是此时还需要除以一个balls[i]！

那么综合起来，此时转移方程就可以写成

f[i][j][k] \= f[i - 1][j][k + 1] \* (s[i] - j)！ / (s[i] - j - balls[i])！ / (balls[i])！

2、第i种球全部放到盒子一当中，那么就有

f\[i\]\[j\]\[k\] \= f\[i - 1\]\[j - balls\[i\]\]\[k - 1\] \* p

与情况1类似，此时同样产生了一种颜色差，因此是从k - 1转移而来。这里的p表示的则是将balls[i]个球插入到j - balls[i]个球之间的方案数，那么就有

f[i][j][k] \= f[i - 1][j][k + 1] \* j！ / (j - balls[i])！ / balls[i]！

3、选择choose个第i种球放到盒子一当中，剩下的balls[i] - choose种球放到盒子二当中，那么就有

f[i][j][k] \= f[i - 1][j - choose][k] \* p

这里没有产生颜色差，因此是从k转移而来。p的定义则是融合了上面两种情况，既需要考虑盒子一中将choose个球插入到j - choose个球之间的方案数，也需要考虑盒子二中将balls[i] - choose个球插入到s[i] - j - (balls[i] - choose)个球之间的方案数，那么就有

f[i][j][k] \= f[i - 1][j - choose][k] \* j！ / (j - choose)！ / choose！) \* ((s[i] - j)！ / (s[i] - j - (balls[i] - choose))！ / (balls[i] - choose)！)

动态规划完成后，最终将i种球取一半放进盒子一的方案总数就是sum(f[-1][s[-1] / 2])，而两个盒子中颜色一样的方案数则是f[-1][s[-1]/2][0]，后者除以前者即为最终答案。

注意到这里每一轮的状态只与上一轮有关，因此可以利用滚动数组优化掉i这一维。另外，在python中由于负数下标的独特含义，因此这里k这一维的取值范围需要从[-n, n]移动到[0, 2n]，即加上一个offset \= n来保证下标为正数。

最后附上python代码：

```python
class Solution(object):
    def getProbability(self, balls):
        """
        :type balls: List[int]
        :rtype: float
        """

        n = len(balls)
        s = sum(balls)
        g = [[0] * (n + n + 1) for _ in range(s / 2 + 1)]
        g[0][n] = 1
        now_s = 0

        fact = [1]
        for index in range(1, s + 1):
            fact.append(fact[-1] * index)

        for i in range(n):
            now_s += balls[i]
            f = [[0] * (n + n + 1) for _ in range(s / 2 + 1)]
            for j in range(s / 2 + 1):
                for k in range(n + n + 1):
                    f[j][k] = 0
                    p = 1
                    for choose in range(balls[i] + 1):
                        if choose == 0:
                            if k + 1 <= n + n:
                                f[j][k] += g[j][k + 1] * fact[now_s - j] / fact[now_s - j - balls[i]] / fact[balls[i]]
                        elif j >= choose:
                            if choose == balls[i]:
                                if k - 1 >= 0:
                                    f[j][k] += g[j - choose][k - 1] * fact[j] / fact[j - balls[i]] / fact[balls[i]]
                            else:
                                f[j][k] += g[j - choose][k] * fact[j] / fact[j - choose] / fact[choose] * fact[now_s - j] / fact[now_s - j - balls[i] + choose] / fact[balls[i] - choose]

            g = f[:]

        return f[-1][n] * 1.0 / sum(f[-1])
```
