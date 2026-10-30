---
title: "3800. 使二进制字符串相等的最小成本"
aliases: ["yiduobo的每日leetcode 3800.使二进制字符串相等的最小成本"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/bit-manipulation", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1992282965338771586"
zhihu_id: "1992282965338771586"
zhihu_title: "yiduobo的每日leetcode 3800.使二进制字符串相等的最小成本"
question_id: "3800"
question: "使二进制字符串相等的最小成本"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-make-two-binary-strings-equal/"
difficulty: "Medium"
rating: 1841
created: "2026-01-09T01:34:33+08:00"
updated: "2026-01-09T01:34:37+08:00"
upvotes: 0
comments: 0
---

# 3800. 使二进制字符串相等的最小成本

> **[yiduobo的每日leetcode 3800.使二进制字符串相等的最小成本](https://zhuanlan.zhihu.com/p/1992282965338771586) · 知乎 · 2026-01-09 · 赞同 0**
> 力扣：[3800. 使二进制字符串相等的最小成本](https://leetcode.cn/problems/minimum-cost-to-make-two-binary-strings-equal/) · Medium · 灵茶山艾府：[分类讨论（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3800.使二进制字符串相等的最小成本

<https://leetcode.cn/problems/minimum-cost-to-make-two-binary-strings-equal/description/>

题目给出两个长度为n的二进制字符串s和t，以及三个正整数flipCost、swapCost以及crossCost。

现在可以对s和t应用一下操作任意次，顺序不限：

- 选择任意下标index，翻转s\[index\]或者t\[index\](将'0'变为'1'或者将'1'变为'0')。此操作的成本为flipCost
- 选择两个不同的下标p和q，交换s[p]和s[q]，或者t[p]和t[q]。此操作的成本为swapCost
- 选择一个下标index，交换s[index]和t[index]。此操作的成本为crossCost

问将s和t变为相同的最小总成本。

首先分析下每种操作的作用。

对于flip，其可以修正任意不匹配位置，花费是flipCost。

对于swap，其可以修正两个互补的不匹配位置，花费是swapCost。需要注意swap操作只有运用在互补的不匹配位置上才有意义，否则的话执行swap操作并不会使得不匹配位置的数量变少。

最后是cross，乍一看感觉没什么作用，但是其可以与swap搭配执行。对于两个同向的不匹配位置，先对其中一个位置执行cross操作，这样一来这两个不匹配位置就变成了一组互补的不匹配位置，接下来就可以执行swap操作了。也就是说，在这里是使用swapCost + crossCost，来修正两个同向的不匹配位置。

接下来可以先一趟遍历，计算s中对应值为'0'的不匹配位置数量zero，以及对应值为'1'的不匹配位置数量one。然后就可以分析如何执行操作了：

首先，若flipCost \* 2 \<\= swapCost，那么在这里就应该全部使用flipCost，此时的答案就是(one + zero) \* flipCost。

接下来，若flipCost \* 2 > swapCost，那么则应该先尽量对互补的不匹配位置对执行swap操作。互补的不匹配位置对的数量为min(one, zero)，因此这一步的花销为swapCost \* min(one, zero)。处理完成后，可能还会剩下一些同向的不匹配位置，数量r \= abs(one - zero)，此时则需要考虑是执行两次flip划算，还是组合执行cross和swap划算。

也就是说，若flipCost \* 2 > swapCost + crossCost，那么就应该组合执行，花销为(swapCost + crossCost) \* (r // 2)。需要注意的是，若此时的r为奇数，那么最后落单的这一个位置必须执行一次flip操作。

反之，若flipCost \* 2 \<\= swapCost + crossCost，那么就应该全部执行flip操作。

最后附上python代码：

```python
class Solution(object):
    def minimumCost(self, s, t, flipCost, swapCost, crossCost):
        """
        :type s: str
        :type t: str
        :type flipCost: int
        :type swapCost: int
        :type crossCost: int
        :rtype: int
        """
        
        zero = 0
        one = 0
        for cs, ct in zip(s, t):
            if cs != ct:
                if cs == '0':
                    zero += 1
                else:
                    one += 1
        
        if flipCost * 2 <= swapCost:
            return flipCost * (zero + one)
        
        res = swapCost * min(zero, one)
        r = abs(zero - one)
        if flipCost * 2 > swapCost + crossCost:
            res += r // 2 * (swapCost + crossCost)
        else:
            res += r // 2 * flipCost * 2
        
        r %= 2
        return res + r * flipCost
```
