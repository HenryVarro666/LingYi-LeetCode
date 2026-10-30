---
title: "3457. 吃披萨"
aliases: ["yiduobo的每日leetcode 3457.吃披萨"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1894470920032196392"
zhihu_id: "1894470920032196392"
zhihu_title: "yiduobo的每日leetcode 3457.吃披萨"
question_id: "3457"
question: "吃披萨"
problem_url: "https://leetcode.cn/problems/eat-pizzas/"
difficulty: "Medium"
rating: 1704
created: "2025-04-12T19:50:33+08:00"
updated: "2025-04-12T19:50:33+08:00"
upvotes: 0
comments: 0
---

# 3457. 吃披萨

> **[yiduobo的每日leetcode 3457.吃披萨](https://zhuanlan.zhihu.com/p/1894470920032196392) · 知乎 · 2025-04-12 · 赞同 0**
> 力扣：[3457. 吃披萨](https://leetcode.cn/problems/eat-pizzas/) · Medium · 灵茶山艾府：[贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3457.吃披萨

[3457. 吃披萨 - 力扣（LeetCode）](https://leetcode.cn/problems/eat-pizzas/description/)

题目给出一个长度为n的整数数组pizzas，其中n为4的倍数，pizzas[index]表示第index个披萨的重量。每天需要吃掉其中的4个披萨，若当前是第奇数天，那么体重将会增加当天吃掉的披萨中的最大重量；若当前是第偶数天，那么体重将会增加当天吃掉的披萨中的第二大的重量。

问如何吃披萨才能使得体重增加得最多。

按照题目的描述，每天吃掉的4个披萨中只有一个的重量会被累加到答案中，因此对于白吃的另外三个披萨，就应该让这些披萨的重量尽可能的小。

对于奇数天是很好处理的，只需吃掉最重的披萨以及最轻的三个披萨就行了。

而对于偶数天，当天吃掉的最重的披萨实际上是浪费了，但是为了保全第二种的披萨，在这里依然应该让第二大的披萨尽量重。不过考虑到最终的披萨浪费掉了，相比之下奇数天的方案是更赚的，简单的证明如下：

如果某个偶数天吃掉的最重的披萨重量大于某个奇数天吃掉的最重的披萨重量，那么交换这两个最重的披萨后得到的总重量显然是更大的，因此在这里就可以确定奇数天吃掉的一定是最终的那些披萨。

而对于满足奇数天的吃法后剩下的披萨，再每次取其中最重的两个，配合最轻的两个披萨在偶数天吃掉即可。

这样一来，就可以将披萨按从大到小的顺序排序，接下来将会度过even \= n // 2个偶数天，以及odd \= n - even个奇数天，因此在这里就应该将最重的odd个披萨在奇数天吃掉，增长的体重为最重的odd个披萨重量之和。接下来，所有的偶数天就吃掉剩下的披萨中最重的两个，增长的体重则为第odd + 2重、第odd + 4重、第odd + 6重、...的披萨的重量之和。

最后附上python代码：

```python
class Solution(object):
    def maxWeight(self, pizzas):
        """
        :type pizzas: List[int]
        :rtype: int
        """
        
        pizzas.sort(reverse=True)
        n = len(pizzas)
        n //= 4
        even = n // 2
        odd = n - even

        res = 0
        for index in range(odd):
            res += pizzas[index]
        for index in range(even):
            res += pizzas[odd + index * 2 + 1]
        
        return res
```
