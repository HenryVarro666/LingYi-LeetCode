---
title: "4014. 应用折扣后的最低总价"
aliases: ["yiduobo的每日leetcode 4014.应用折扣后的最低总价"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/math", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2070338266264500022"
zhihu_id: "2070338266264500022"
zhihu_title: "yiduobo的每日leetcode 4014.应用折扣后的最低总价"
question_id: "4014"
question: "应用折扣后的最低总价"
problem_url: "https://leetcode.cn/problems/minimum-total-price-after-applying-discounts/"
difficulty: "Medium"
rating: 1192
created: "2026-08-11T02:48:05+08:00"
updated: "2026-08-11T02:48:08+08:00"
upvotes: 0
comments: 0
---

# 4014. 应用折扣后的最低总价

> **[yiduobo的每日leetcode 4014.应用折扣后的最低总价](https://zhuanlan.zhihu.com/p/2070338266264500022) · 知乎 · 2026-08-11 · 赞同 0**
> 力扣：[4014. 应用折扣后的最低总价](https://leetcode.cn/problems/minimum-total-price-after-applying-discounts/) · Medium · 灵茶山艾府：[排序不等式，避免浮点运算的写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4014.应用折扣后的最低总价

<https://leetcode.cn/problems/minimum-total-price-after-applying-discounts/description/>

题目给出两个整数数组prices和discounts。

prices[index]表示第index件商品的价格，discounts[index]则表示一个折扣百分比。

现在可以按照一下规则使用折扣：

- 每个折扣最多只能用于一件商品
- 每件商品最多最能使用一个折扣
- 商品也可以不适用任何折扣

如果将d%的折扣应用于价格为p的商品，则其最终价格为(p \* (100 - d)) / 100，最终价格不进行四舍五入。

请以最优方式分配折扣，并返回所有商品最终价格之和的最小值。与实际答案的误差在10^(-5)以内的结果将被接受。

首先可以明确的是，折扣应该是能用就用，而且应该把最大的先用掉，这样才能使得最终答案最小。

另一方面，具体的使用方法则可以这样来进行分析：

对于两件商品的价格p和q，不妨设p \< q，同时有两个折扣a和b，满足a \< b，那么有两种方案，分别是p用a，q用b，以及p用b，q用a，最终的花销分别为

p \* (100 - a) / 100 + q \* (100 - b) / 100 \= p + q - (ap + bq) / 100

p \* (100 - b) / 100 + q \* (100 - a) / 100 \= p + q - (bp + aq) / 100

可以发现，实际上最终对比的就是ap + bq以及bp + aq的大小，移项后就是(a - b)p与(a - b)q的大小，显然是右侧更大，因此ap + bq \< bp + aq，也就是说第二个式子更小，是更优的，即更大力度的折扣应该应用在价格更贵的物品上，这也是符合直觉的。

基于以上的结论，就可以将商品和折扣都按从大到小的顺序进行排序，然后遍历所有商品。若当前商品还有可用的折扣，那么就用剩余折扣中最大的那个，否则就原价购买。

最后附上python代码：

```python
class Solution(object):
    def minPrice(self, prices, discounts):
        """
        :type prices: List[int]
        :type discounts: List[int]
        :rtype: float
        """

        prices.sort(reverse=True)
        discounts.sort(reverse=True)

        res = 0
        for index in range(len(prices)):
            if index < len(discounts):
                res += prices[index] * (100 - discounts[index]) * 1.0 / 100
            else:
                res += prices[index]
        
        return res
```
