---
title: "964. 表示数字的最少运算符"
aliases: ["yiduobo的每日leetcode 964.表示数字的最少运算符"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/361439384"
zhihu_id: "361439384"
zhihu_title: "yiduobo的每日leetcode 964.表示数字的最少运算符"
question_id: "964"
question: "表示数字的最少运算符"
problem_url: "https://leetcode.cn/problems/least-operators-to-express-number/"
created: "2021-03-31T23:26:00+08:00"
updated: "2021-03-31T23:26:00+08:00"
upvotes: 0
comments: 0
---

# 964. 表示数字的最少运算符

> **[yiduobo的每日leetcode 964.表示数字的最少运算符](https://zhuanlan.zhihu.com/p/361439384) · 知乎 · 2021-03-31 · 赞同 0**
> 力扣：[964. 表示数字的最少运算符](https://leetcode.cn/problems/least-operators-to-express-number/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

964.表示数字的最少运算符

[力扣](https://leetcode-cn.com/problems/least-operators-to-express-number/)

由于这里不能使用括号，因此实际上符号的组合就很少了。注意到target为整数，那么这里除法的唯一作用就是通过x / x来得到1，那么此时问题就转化成了使用加法和减法，通过1、x、x^2、...、x^p来组成target的最小代价是什么。考虑加号和减号的代价，我们可以认为1的代价为2，x的代价为1，而之后x^k的代价都为k。最终计算出总代价之后还需要减去1，因为整个式子的第一个部分是不需要前置加号的。

接下来，注意到这里的x大于等于2，因此对于构成x^k这样一个目标，使用x个x^(k - 1)的代价必然是大于等于直接构造x^k的，因此实际上我们对于构造target这样一个目标就只有两种选择。我们首先计算出最大的p，这里的p满足x^p \<\= target，那么我们可以：

1、选择构造t1个x^p，这里的t1为满足t1 \* x^p \<\= target的最大整数，然后此时的问题就转化成了如何得到target - t1 \* x^p

2、也可以反向先构造一个x^(p + 1)，然后此时的问题就转化成了如何得到

d \= x^(p + 1) - target

对于d而言，此时再构造一个x^(p + 1)然后做减法显然是没有意义的，那么就只能通过t2个x^p先进行构造，这里的t2定义类似，为满足t1 \* x^p \<\= d的最大整数，然后此时的问题就转化成了如何得到d % x^p

如果在x进制下看上面的操作，那么每一轮操作都会将target的位数缩小一位，因此实际上的状态数并不多，完全可以使用dict来进行动态规划。

设f[i]表示构造i最少需要多少次操作，那么对于f[i]：

1、如果构造x^p，设构造一个的代价为w[p]，t1则等于i / x^p，那么就有

f[i] \= min(f[i], t1 \* w[p] + f[i % x^p]

2、如果构造x^(p + 1)，设构造一个的代价为w[p + 1]，此时的t2等于(x^(p + 1) - i) / x^p，那么就有

f[i] \= min(f[i], t2 \* w[p] + w[p + 1] + f[(x^(p + 1) - i) % x^p])

这里的w可以根据最上面的计算方法先预处理出来，那么最终答案就是f[target] - 1。

最后附上python代码：

```python
class Solution(object):
    def leastOpsExpressTarget(self, x, target):
        """
        :type x: int
        :type target: int
        :rtype: int
        """

        if target == 1:
            return 1

        power = [[1, 1], [x, 0]]
        while power[-1][0] < target:
            power.append([power[-1][0] * x, power[-1][1] + 1])
        
        f = {0 : 0}
        for x, cnt in power:
            f[x] = cnt + 1
            
        return self.dfs(target, power, f) - 1
    
    def dfs(self, now, power, f):
        if now not in f:
            p = len(power) - 1
            while power[p][0] > now:
                p -= 1
            
            t1 = now / power[p][0]
            f[now] = t1 * (power[p][1] + 1) + self.dfs(now % power[p][0], power, f)

            t2 = (power[p + 1][0] - now) / power[p][0]
            f[now] = min(f[now], t2 * (power[p][1] + 1) + power[p + 1][1] + 1 + self.dfs((power[p + 1][0] - now) % power[p][0], power, f))
        
        return f[now]
```
