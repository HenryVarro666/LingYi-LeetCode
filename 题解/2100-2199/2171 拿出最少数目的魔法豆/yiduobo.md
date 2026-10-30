---
title: "2171. 拿出最少数目的魔法豆"
aliases: ["yiduobo的每日leetcode 2171.拿出最少数目的魔法豆"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/534075631"
zhihu_id: "534075631"
zhihu_title: "yiduobo的每日leetcode 2171.拿出最少数目的魔法豆"
question_id: "2171"
question: "拿出最少数目的魔法豆"
problem_url: "https://leetcode.cn/problems/removing-minimum-number-of-magic-beans/"
difficulty: "Medium"
rating: 1748
created: "2022-06-26T20:15:19+08:00"
updated: "2022-06-26T20:15:19+08:00"
upvotes: 0
comments: 0
---

# 2171. 拿出最少数目的魔法豆

> **[yiduobo的每日leetcode 2171.拿出最少数目的魔法豆](https://zhuanlan.zhihu.com/p/534075631) · 知乎 · 2022-06-26 · 赞同 0**
> 力扣：[2171. 拿出最少数目的魔法豆](https://leetcode.cn/problems/removing-minimum-number-of-magic-beans/) · Medium · 灵茶山艾府：[枚举最后袋子中魔法豆的数目（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2171.拿出最少数目的魔法豆

[力扣](https://leetcode.cn/problems/removing-minimum-number-of-magic-beans/)

由于单个袋子中魔法豆的数目小于等于十万，那么可以枚举得到最终答案时袋子中剩余的魔法豆数目cnt。对于豆子数小于cnt的袋子，这些袋子中的豆子将被拿光，而对于豆子数大于等于cnt的袋子则会留下cnt个豆子。设有k个袋子中的豆子数大于等于cnt，那么最终剩下的豆子数就是cnt \* k，而拿走的豆子数目就是sum(beans) - cnt \* k。对于每种cnt的取值求出这种情况下拿走的豆子数，其中最小值就是最终答案。

到了这里，题目就变成了找到一种枚举cnt的方法，能在枚举的同时高效得到豆子数大于等于cnt的袋子数目k。

对于这个问题可以将beans从小到大进行排序，然后从头开始向后枚举。对于当前枚举到的cnt，设其在排序后数组中的下标为index，那么下标从index到n - 1的这些袋子中豆子数目都是大于等于cnt的，因此对应的k就是n - 1 - index + 1 \= n - index，此时需要拿走的豆子数就是sum(beans) - cnt \* (n - index)。

最后附上python代码：

```python
class Solution(object):
    def minimumRemoval(self, beans):
        """
        :type beans: List[int]
        :rtype: int
        """

        res = None
        s = sum(beans)
        res = s
        n = len(beans)
        for index, b in enumerate(sorted(beans)):
            res = min(res, s - (n - index) * b)
        
        return res
```
