---
title: "902. 最大为N的数字组合"
aliases: ["yiduobo的每日leetcode 902.最大为N的数字组合"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/353581756"
zhihu_id: "353581756"
zhihu_title: "yiduobo的每日leetcode 902.最大为N的数字组合"
question_id: "902"
question: "最大为 N 的数字组合"
problem_url: "https://leetcode.cn/problems/numbers-at-most-n-given-digit-set/"
difficulty: "Hard"
rating: 1990
created: "2021-02-28T20:38:08+08:00"
updated: "2021-02-28T20:38:08+08:00"
upvotes: 0
comments: 0
---

# 902. 最大为N的数字组合

> **[yiduobo的每日leetcode 902.最大为N的数字组合](https://zhuanlan.zhihu.com/p/353581756) · 知乎 · 2021-02-28 · 赞同 0**
> 力扣：[902. 最大为 N 的数字组合](https://leetcode.cn/problems/numbers-at-most-n-given-digit-set/) · Hard · 灵茶山艾府：[数位 DP 通用模板 + 详细注释 + 题单（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

902.最大为N的数字组合

[力扣](https://leetcode-cn.com/problems/numbers-at-most-n-given-digit-set/)

题目未限制每个数字的使用次数，但需要保证拼出来的数字小于等于n，那么一个自然的想法就是考虑n的最高位。设n一共有l位，那么n的最高位也就是n[l - 1]。

接下来，我们枚举D中的每个数字x，对于x以及n[l - 1]，可能出现下列三种情况：

1、x \< n[l - 1]：此时说明以x为最高位的l位数必然都是小于n的，因此后续的l - 1位可以随便选择。每一位都有len(D)种选择，因此这里可以提供len(D) ^ (l - 1)种可行的答案。

2、x > n[l - 1]：与情况1相反，此时无论如何以x为最高位的l位数都是大于n的，因此此时不能提供可行的答案。

3、x \= n[l - 1]：此时可以视为用D中数构造一个l - 1位，同时大小要小于等于n去除最高位后剩下的数有多少种方案，转化为了一个子问题。

综合起来，就是若D中有k个数小于n[l - 1]，那么可以提供k \* (len(D) ^ (l - 1))种可行的方案。另外，若n[l - 1]出现在D中，那么还需要继续向后考虑n[l - 2]。

于是现在就有了一种做法。从n的最高位开始往后遍历，对于当前这一位char，我们枚举D中的所有数，设当前枚举到num。那么对于num和char，我们可以根据上面这三种情况分别进行处理。若出现了num等于char的情况，我们就继续向后遍历n，否则就可以直接退出了。

需要注意的是，若n本身是由D中的数字构成，那么最终答案还需要加上1，表示的就是恰好相等这种情况。

最后附上python代码：

```python
class Solution(object):
    def atMostNGivenDigitSet(self, digits, n):
        """
        :type digits: List[str]
        :type n: int
        :rtype: int
        """

        l = len(str(n))
        power = [1]
        res = 0
        for index in range(l - 1):
            power.append(power[-1] * len(digits))
            res += power[-1]
        
        for index, char in enumerate(str(n)):
            cnt = 0
            flag = False
            for num in digits:
                if num == char:
                    flag = True
                elif num < char:
                    cnt += 1
            res += cnt * power[l - index - 1]
            if not flag:
                break
        
        if flag:
            res += 1

        return res
```
