---
title: "914. 卡牌分组"
aliases: ["yiduobo的每日leetcode 914.卡牌分组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/355080589"
zhihu_id: "355080589"
zhihu_title: "yiduobo的每日leetcode 914.卡牌分组"
question_id: "914"
question: "卡牌分组"
problem_url: "https://leetcode.cn/problems/x-of-a-kind-in-a-deck-of-cards/"
created: "2021-03-06T16:16:15+08:00"
updated: "2021-03-06T16:16:15+08:00"
upvotes: 0
comments: 0
---

# 914. 卡牌分组

> **[yiduobo的每日leetcode 914.卡牌分组](https://zhuanlan.zhihu.com/p/355080589) · 知乎 · 2021-03-06 · 赞同 0**
> 力扣：[914. 卡牌分组](https://leetcode.cn/problems/x-of-a-kind-in-a-deck-of-cards/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

914.卡牌分组

[力扣](https://leetcode-cn.com/problems/x-of-a-kind-in-a-deck-of-cards/)

题目要求每一组的卡牌都是一样的，那么对于某种卡牌，设其有k张，那么只有当满足k是x的倍数时才能进行分组。每种卡牌的数量都是x的倍数，且x要最大，那么问题要求的实际上就是每种卡牌数的最大公约数。

最后附上python代码：

```python
class Solution(object):
    def hasGroupsSizeX(self, deck):
        """
        :type deck: List[int]
        :rtype: bool
        """

        if len(deck) == 1:
            return False

        cnt_dict = {}
        for num in deck:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        
        if len(cnt_dict) == 1:
            return True

        cnt_list = cnt_dict.values()
        res = self.gcd(cnt_list[0], cnt_list[1])
        if res == 1:
            return False
        for cnt in cnt_list[2:]:
            res = self.gcd(res, cnt)
            if res == 1:
                return False
        
        return True
    
    def gcd(self, x, y):
        while y:
            x, y = y, x % y
        
        return x
```
