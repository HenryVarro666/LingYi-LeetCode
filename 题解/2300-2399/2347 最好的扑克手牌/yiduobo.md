---
title: "2347. 最好的扑克手牌"
aliases: ["yiduobo的每日leetcode 2347.最好的扑克手牌"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/560715814"
zhihu_id: "560715814"
zhihu_title: "yiduobo的每日leetcode 2347.最好的扑克手牌"
question_id: "2347"
question: "最好的扑克手牌"
problem_url: "https://leetcode.cn/problems/best-poker-hand/"
difficulty: "Easy"
created: "2022-09-02T21:38:56+08:00"
updated: "2022-09-02T21:38:56+08:00"
upvotes: 0
comments: 0
---

# 2347. 最好的扑克手牌

> **[yiduobo的每日leetcode 2347.最好的扑克手牌](https://zhuanlan.zhihu.com/p/560715814) · 知乎 · 2022-09-02 · 赞同 0**
> 力扣：[2347. 最好的扑克手牌](https://leetcode.cn/problems/best-poker-hand/) · Easy · 灵茶山艾府：[模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2347.最好的扑克牌

[力扣](https://leetcode.cn/problems/best-poker-hand/)

这出题人一看就没打过牌，懂不懂四条、顺子、福尔豪斯的含金量啊。

首先遍历一趟花色，判断所有牌的花色是否相同。若相同，那么答案就是同花，否则就需要遍历一趟点数，统计同一点数最多出现多少次，然后根据这个次数判断最终答案是三条、对子还是高牌。

最后附上python代码：

```python
class Solution(object):
    def bestHand(self, ranks, suits):
        """
        :type ranks: List[int]
        :type suits: List[str]
        :rtype: str
        """

        flag = True
        for index in range(4):
            if suits[index] != suits[index + 1]:
                flag = False
                break
        
        if flag:
            return 'Flush'
        
        cnt_dict = {}
        max_cnt = 0
        for rank in ranks:
            cnt_dict[rank] = cnt_dict.get(rank, 0) + 1
            max_cnt = max(max_cnt, cnt_dict[rank])
        
        if max_cnt >= 3:
            return 'Three of a Kind'
        elif max_cnt >= 2:
            return 'Pair'
        else:
            return 'High Card'
```
