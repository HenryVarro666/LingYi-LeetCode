---
title: "1753. 移除石子的最大得分"
aliases: ["yiduobo的每日leetcode 1753.移除石子的最大得分"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/458702976"
zhihu_id: "458702976"
zhihu_title: "yiduobo的每日leetcode 1753.移除石子的最大得分"
question_id: "1753"
question: "移除石子的最大得分"
problem_url: "https://leetcode.cn/problems/maximum-score-from-removing-stones/"
difficulty: "Medium"
rating: 1488
created: "2022-01-17T23:34:04+08:00"
updated: "2022-01-17T23:34:04+08:00"
upvotes: 1
comments: 0
---

# 1753. 移除石子的最大得分

> **[yiduobo的每日leetcode 1753.移除石子的最大得分](https://zhuanlan.zhihu.com/p/458702976) · 知乎 · 2022-01-17 · 赞同 1**
> 力扣：[1753. 移除石子的最大得分](https://leetcode.cn/problems/maximum-score-from-removing-stones/) · Medium · 灵茶山艾府：[结论题（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1753.移除石子的最大得分

[力扣](https://leetcode-cn.com/problems/maximum-score-from-removing-stones/)

题目的数据规模并不大，那么按照每次都从当前剩余石子最多的两堆当中去拿这个策略也是可以的，不过在这里可以根据这个策略来直接推算出最终结果，而不需要去具体地模拟每一步的操作。

由于三堆石子是等价的，那么为了方便起见，不妨设a >\= b >\= c。

首先考虑最特殊的情况，即a \= b \= c。此时应该按照(a, b)，(a, c)，(b, c)这样的顺序进行操作，这样一来就相当于在一轮操作之后从每堆石子中的都拿走了两颗。若石子初始情况下是偶数颗，那么就可以按照这个策略全部拿完，若初始为奇数颗，则会剩下一颗式子落单。无论是那种情况，最终得分的表示都是(a + b + c) / 2，这里的除法为整除。

接下来考虑其他的情况：

1、若a \= b >\= c，那么此时执行若干轮(a, b)之后，就可以来到a \= b \= c的局面，那么此时的答案同样是(a + b + c) / 2

2、若a > b：

2-1）若a > b > c，那么首先应该执行若干轮(a, b)，使得b \= c。这里执行的轮次k就等于b - c，而执行完k轮之后新的a' \= a - k，b' \= b - k。此时应该初始化答案为k，同时问题就转化成了下面的a' > b' \= c这种情况了。

2-2）若a > b \= c，那么应该是按照(a', b')，(a', c)的顺序来执行。这里又可以分成两种情况。

若a' > b' + c，那么在b'和c全部拿完之后a还有剩余，此时可以执行的轮次就是b' + c，因此得分就是b' + c。

若a' \<\= b' + c，那么在若干轮之后可以再次得到a' \= b' >\= c这种状态，因此这里的得分同样是(a + b + c) / 2

注意到第二种情况当中，对于2-1而言，无论其最终是走到了k + (a' + b' + c) / 2这种情况，还是k + b' + c这种情况，都可以将式子转化回去。

对于k + (a' + b' + c) / 2而言，由于k \= a - a' \= b - b'，那么k + (a' + b' + c) / 2 \= (a + b + c) / 2

而对于k + b' + c而言，则同样有k + b' + c \= b + c

也就是说最终根本就没必要考虑2-1这种情况，直接对比a和b + c的大小，就能知道答案是什么了。

更进一步的，对于a \= b这种情况而言，其必然也满足a \<\= b + c，因此实际上最终可以转化为唯一一种情况：

若a \<\= b + c，那么答案就是(a + b + c) / 2，否则答案就是b + c

最后附上python代码：

```python
class Solution(object):
    def maximumScore(self, a, b, c):
        """
        :type a: int
        :type b: int
        :type c: int
        :rtype: int
        """

        max_num = max(a, b, c)
        if max_num <= a + b + c - max_num:
            return (a + b + c) / 2
        else:
            return a + b + c - max_num
```
