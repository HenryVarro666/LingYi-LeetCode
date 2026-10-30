---
title: "2999. 统计强大整数的数目"
aliases: ["yiduobo的每日leetcode 2999.统计强大整数的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/692887338"
zhihu_id: "692887338"
zhihu_title: "yiduobo的每日leetcode 2999.统计强大整数的数目"
question_id: "2999"
question: "统计强大整数的数目"
problem_url: "https://leetcode.cn/problems/count-the-number-of-powerful-integers/"
difficulty: "Hard"
rating: 2351
created: "2024-04-17T04:00:13+08:00"
updated: "2024-04-17T04:00:13+08:00"
upvotes: 3
comments: 0
---

# 2999. 统计强大整数的数目

> **[yiduobo的每日leetcode 2999.统计强大整数的数目](https://zhuanlan.zhihu.com/p/692887338) · 知乎 · 2024-04-17 · 赞同 3**
> 力扣：[2999. 统计强大整数的数目](https://leetcode.cn/problems/count-the-number-of-powerful-integers/) · Hard · 灵茶山艾府：[【模板】上下界数位 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2999.统计强大整数的数目

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-the-number-of-powerful-integers/description/)

数位动态规划的题目，但是本题相比之前遇到的其实要简单很多。

首先对于给出的s，其必须镶嵌在找出来的整数末尾，也就是说这里数位动态规划其实只需要针对强大整数的前缀来进行构造。另一方面，当s小于等于上界finish的后缀时，构造出来的前缀就可以压着finish的前缀来构造，否则构造出来的前缀必须小于finish的前缀；同样的，当s大于等于下界start的后缀时，构造出来的前缀就可以压着start的前缀来构造，否则构造出来的前缀必须大于start的前缀。

接下来则是通过数位动态规划来构造强大整数的前缀。由于本题没有对前缀做其他的限制，那么在这里直接使用f[index][state]表示能构造出来前index位，且与start和finish上下界状态为state的可行方案数。

具体来说，当state为0时，表示当前构造的前index位处于上界和下界前index位之间；当state为1时，表示当期那构造的前index位与下界的前index位相同，但是小于上界的前index位；当state为2时则是前index位与上界相同，但是大于下界；最后当state为3时，则是前index位与上下界的前index位都相同。

那么对于f[index][state]，就可以从0到limit之间枚举下一位填充的数字v：

1、对于f[index][0]：

首先无论v取什么值，f[index][0]都可以在f[index - 1][0]的基础上添加数字v，因为此前的f[index - 1][0]的高位没有压线，所以v无论如何取值，后续的数都是处于start和finish之间的。

接下来，若v大于start[index]，那么f[index][0]就可以在f[index - 1][1]的基础上添加数字v，因为此时的f[index - 1]的高位压着下界且小于上界，此时如果添加v，就可以保证后续的数处于start和finish之间。

同样的，若v小于finish[index]，那么f[index][0]就可以在f[index - 1][2]的基础上添加数字v。

最后，若v同时满足大于start[index]且小于finish[index]，那么f[index][0]就可以在f[index - 1][3]的基础上添加数字v，因此此时的f[index - 1][3]的高位与上界和下界的高位相同，而此时添加的v则处于上界和下界之间，那么后续的数也必然处于start和finish之间。

2、对于f[index][1]：

为了使得在index这一位也压住下限start，那么在上一位也必须压住下限start，也就是说在这里v必须要等于start[index]。另外，如果在上一位同时压住了上限和下限，同时v也等于finish[index]，那么在这一位也同时压住了上限和下限，此时的f[index][1]就只能通过f[index - 1][1]来进行转移，反之，若v小于finish[index]，那么就可以同时通过f[index - 1][1]以及f[index - 1][3]来进行转移。

3、对于f[index][2]：

与上面的情况对称，若v等于finish[index]，那么当v也等于start[index]时，f[index][2]只能通过f[index - 1][2]来进行转移，反之则可以通过f[index - 1][2]以及f[index - 1][3]来进行转移。

4、对于f[index][3]：

这种情况最直观。只有当v与start[index]和finish[index]都相等时，f[index][3]才可以通过f[index - 1][3]来进行转移。

前缀的部分计算完成完成后，则还需要考虑拼上limit之后的数是否处于start和finish之间。具体来说：

1、无论s和start以及finish的后缀时什么关系，当前缀没有压线时，拼上s后得到的数也必然处于start和finish之间，因此就应该将f[-1][0]累加到答案中。

2、当s大于等于start的后缀时，前缀就可以压着start的前缀，因此可以将f[-1][1]累加到答案中。

3、当s小于等于finish的后缀时，前缀就可以压着finish的前缀，因此可以将f[-1][2]累加到答案中。

4、当同时满足条件2和条件3时，前缀就可以同时压着start和finish的前缀，因此可以将f[-1][3]累加到答案中。

另外，由于f每一轮的状态只和上一轮有关，因此在这里可以用过滚动数组优化掉index这一维。还有一点就是在这里应该可以通过分析上下界对应位上的数值以及limit，配合当前的state直接计算出可以填充的v的数量，从而实现O(1)的转移，但是我简单考虑了一下，感觉情况会非常多，因此在这里依然是采用从0到limit枚举v的方式来进行转移。

最后附上python代码：

```python
class Solution(object):
    def numberOfPowerfulInt(self, start, finish, limit, s):
        """
        :type start: int
        :type finish: int
        :type limit: int
        :type s: str
        :rtype: int
        """

        fi = str(finish)
        n = len(fi)
        st = str(start)
        st = '0' * (n - len(st)) + st

        f = [0, 0, 0, 1]
        for index in range(n - len(s)):
            g = f[:]
            f = [0, 0, 0, 0]

            for v in range(limit + 1):
                if v == int(st[index]):
                    if v == int(fi[index]):
                        f[1] += g[1]
                        f[2] += g[2]
                        f[3] += g[3]
                    else:
                        f[1] += g[1]
                        f[1] += g[3]
                elif v == int(fi[index]):
                    f[2] += g[2]
                    f[2] += g[3]
                
                f[0] += g[0]
                if int(st[index]) < v:
                    f[0] += g[1]
                if v < int(fi[index]):
                    f[0] += g[2]
                if int(st[index]) < v < int(fi[index]):
                    f[0] += g[3]

        l_flag = u_flag = False
        if st[-len(s):] <= s:
            l_flag = True
        if fi[-len(s):] >= s:
            u_flag = True

        res = f[0]
        if l_flag:
            res += f[1]
        if u_flag:
            res += f[2]
        if l_flag and u_flag:
            res += f[3]
        
        return res
```
