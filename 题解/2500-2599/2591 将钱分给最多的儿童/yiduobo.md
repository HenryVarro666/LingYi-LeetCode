---
title: "2591. 将钱分给最多的儿童"
aliases: ["yiduobo的每日leetcode 2591.将钱分给最多的儿童"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/fen-lei-tao-lun", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/643444194"
zhihu_id: "643444194"
zhihu_title: "yiduobo的每日leetcode 2591.将钱分给最多的儿童"
question_id: "2591"
question: "将钱分给最多的儿童"
problem_url: "https://leetcode.cn/problems/distribute-money-to-maximum-children/"
difficulty: "Easy"
rating: 1531
created: "2023-07-13T23:29:33+08:00"
updated: "2023-07-13T23:29:33+08:00"
upvotes: 0
comments: 0
---

# 2591. 将钱分给最多的儿童

> **[yiduobo的每日leetcode 2591.将钱分给最多的儿童](https://zhuanlan.zhihu.com/p/643444194) · 知乎 · 2023-07-13 · 赞同 0**
> 力扣：[2591. 将钱分给最多的儿童](https://leetcode.cn/problems/distribute-money-to-maximum-children/) · Easy · 灵茶山艾府：[分类讨论 + O(1) 做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

由于之前的2589题与之前的题出现了重复照搬了相同的做法，今天再额外追加一题。

2591.将钱分给最多的儿童

[力扣](https://leetcode.cn/problems/distribute-money-to-maximum-children/)

首先，由于每个人至少分到1美元，那么当初始的money小于children时，必然有人分不到，因此直接返回-1。

接下来，若初始的money足够，那么可以先将其减去children，表示每人先分到了1美元，接下来考虑的就是在不分出3美元的情况下尽量多地分出7美元。

令p \= money / 7，也就是说剩下的money最多可以分出p份7美元。

若这里的p大于children，说明剩余的钱太多了，最多分出p - 1个7美元，而多出来的部分则可以分给最后这个人，因此此时的答案就是p - 1。

若p恰好等于children，那么则需要检测p \* 7是否恰好等于money，因为p是通过整除计算出来的，money可能比p \* 7要大。若恰好相等，那么就说明可以每人都分到7美元，此时的答案就是p，否则就与上面的情况类似，需要将多出的前分给最后这个人，答案就是p - 1。

最后，若p小于children，那么理论上可以让p个人分到7美元，然后剩下的money - p \* 7则分给这p个人之外的人。此时需要注意的是，若剩下的money - p \* 7恰好是3美元，同时p恰好等于children - 1，也就是除了这p个人之外只剩一个人，那么此时这3美元就只能被迫分给这一个人了，这是不合法的。

对于这种情况，就只能让前面的p - 1个人分到7美元，剩下两个人来分最后的10美元，此时的答案就是p - 1。

对于其他情况，若剩余的钱不等于3，那么可以将其分给同一个人，反之若等于3且除p个人之外的人数大于1，那么可以将其按分给除p个人之外的另外两个人，这样的话就不会有3出现，此时的答案就是p。

最后附上python代码：

```python
class Solution(object):
    def distMoney(self, money, children):
        """
        :type money: int
        :type children: int
        :rtype: int
        """

        if money < children:
            return -1
        
        money -= children
        p = money / 7
        if p > children:
            return children - 1
        elif p == children:
            if p * 7 == money:
                return p
            else:
                return p - 1
        else:
            if money - p * 7 == 3 and p == children - 1:
                return p - 1
            else:
                return p
```
