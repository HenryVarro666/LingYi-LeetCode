---
title: "3186. 施咒的最大总伤害"
aliases: ["yiduobo的每日leetcode 3186.施咒的最大总伤害"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/hash-table", "leetcode/dynamic-programming", "leetcode/sorting", "题单/动态规划", "题单/动态规划/一-入门-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/706189180"
zhihu_id: "706189180"
zhihu_title: "yiduobo的每日leetcode 3186.施咒的最大总伤害"
question_id: "3186"
question: "施咒的最大总伤害"
problem_url: "https://leetcode.cn/problems/maximum-total-damage-with-spell-casting/"
difficulty: "Medium"
rating: 1841
created: "2024-06-30T00:47:43+08:00"
updated: "2024-06-30T00:48:05+08:00"
upvotes: 0
comments: 0
---

# 3186. 施咒的最大总伤害

> **[yiduobo的每日leetcode 3186.施咒的最大总伤害](https://zhuanlan.zhihu.com/p/706189180) · 知乎 · 2024-06-30 · 赞同 0**
> 力扣：[3186. 施咒的最大总伤害](https://leetcode.cn/problems/maximum-total-damage-with-spell-casting/) · Medium · 灵茶山艾府：[【套路】值域打家劫舍（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3186.施咒的最大总伤害

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-total-damage-with-spell-casting/)

题目给出一个由正整数构成的数组power，表示现在有若干种具有伤害的咒语，power中的伤害值可能相同。当魔法师使用其中伤害值为power[i]的咒语时，就不能再使用伤害值为power[i] - 2、power[i] - 1、power[i] + 1以及power[i] + 2的咒语，问如何施放咒语可以使得伤害值最大。

注意到使用了伤害值为power\[i\]的咒语后，依然可以继续使用伤害值为power\[i\]的咒语，因此对于某种伤害值的咒语，要么都用，要么都不用。于是可以使用哈希表为power去重，将其重新整理为二维数组power\[i\] \= \[p\[i\], f\[i\]\]，表示伤害值为p\[i\]的咒语可以使用f\[i\]次。

接下来，由于施放咒语仅受到伤害值的限制，与原始在数组中的下标顺序无关，那么在这里就可以先将power按照伤害值从小到大进行排序，然后令g[i]表示前i种咒语可以造成的最大伤害值，初始情况下有g[0] \= 0，表示不选择任何咒语时伤害值为0。

接下来对于g\[i\]，其对应的咒语是power\[i - 1\] \= \[p\[i - 1\], f\[i - 1\]\]。

第一种选项是不选择这个咒语，那么就有g[i] \= g[i - 1]。

而如果想要选择这个咒语，那么在之前就不能选择伤害值为p[i - 1] - 1和p[i - 1] - 2的咒语，于是就有g[i] \= max(g[i], g[q + 1] + p[i - 1] \* f[i - 1])，其中的q满足0 \<\= q \< i - 1且p[q] \< p[i] - 2。需要注意这里的下标是q + 1，因为p[q]对应的是第q + 1种咒语。

上面的算法是O(n^2)的，还需要进行优化。

通过上面的第一种选择可以发现，g数组必然是单调不减的，也就是说对于第二种选择中的q，只需要找出最大的满足p[q] \< p[i] - 2的q就行了，此时对应的g[q + 1]也必然是最优的。另一方面，由于power是按照p排序的，那么随着i的增长，q也是单调不减的，因此每一轮都只需要在上一轮q的基础上更新q就行了。

最后附上python代码：

```python
class Solution(object):
    def maximumTotalDamage(self, power):
        """
        :type power: List[int]
        :rtype: int
        """

        power = sorted(Counter(power).items())
        g = [0]
        q = -1
        for p, f in power:
            g.append(g[-1])
            while power[q + 1][0] < p - 2:
                q += 1
            g[-1] = max(g[-1], g[q + 1] + p * f)

        return g[-1]
```
