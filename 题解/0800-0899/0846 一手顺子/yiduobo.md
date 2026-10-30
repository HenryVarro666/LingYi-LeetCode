---
title: "846. 一手顺子"
aliases: ["yiduobo的每日leetcode 846.一手顺子"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/348058899"
zhihu_id: "348058899"
zhihu_title: "yiduobo的每日leetcode 846.一手顺子"
question_id: "846"
question: "一手顺子"
problem_url: "https://leetcode.cn/problems/hand-of-straights/"
created: "2021-01-30T10:18:26+08:00"
updated: "2021-01-30T10:18:26+08:00"
upvotes: 0
comments: 0
---

# 846. 一手顺子

> **[yiduobo的每日leetcode 846.一手顺子](https://zhuanlan.zhihu.com/p/348058899) · 知乎 · 2021-01-30 · 赞同 0**
> 力扣：[846. 一手顺子](https://leetcode.cn/problems/hand-of-straights/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

846.一手顺子

[力扣](https://leetcode-cn.com/problems/hand-of-straights/)

首先，题目要求将手上的卡片按W一组分为若干组，那么若len(hand)不是W的倍数，就可以直接返回false了。

接下来，由于这里的一组是连续的，因此如果我们知道了一组的起点num，那么这一组的终点就必然是num + W - 1，于是一个自然的想法就是将手上的卡片按数值从小到大进行排序，然后每次选取剩下卡片中最小的数作为起点，检测剩下的卡片中是否还存在足量的卡片可以形成长度为W的顺子。若存在，则将这些卡片从中去除，然后继续进行检测；若期间出现卡片不足的情况，那么返回false。

如果到最后所有卡片都被正常使用掉，那么就返回true。

不过注意到这里的检测经常会有重叠的部分，因此可以使用一个变量now来表示当前有多少个尚未完结的顺子。我们同样是将卡片按点数从小到大进行排序，但是这里我们将同样点数的卡片归在一起，并记录起数量。

接下来我们从小到大枚举所有卡片，设当前卡片为num，一共有cnt张：

1、若cnt \< now，说明当前剩下的cnt张值为num的卡片不足以供给now个未完结的顺子，因此返回false

2、若cnt>\=now，说明此时值为num的卡片是足够的，但是可能会有剩余。

那么当cnt > now时，设delta \= cnt - now。

对于多余的这delta张值为num的卡片，我们必须额外构造delta个以num为起点，num+W-1为终点的顺子。此时需要先检测是否有足量的值为num+W-1的卡片，若不足，则返回false，否则我们设stop[num+W-1]为delta，表示将有delta个顺子在num+W-1这里完结。

最后，当前的now就变成了cnt - stop[num]，表示此时应该有cnt个顺子，但是其中有stop[num]个顺子将在num这里完结，因此还剩下cnt - stop[num]个尚未完结的顺子。

在遍历完成后，若未完结的顺子数量为0，即now\=0，那么就返回true，否则返回false。

最后附上python代码：

```python
class Solution(object):
    def isNStraightHand(self, hand, W):
        """
        :type hand: List[int]
        :type W: int
        :rtype: bool
        """

        n = len(hand)
        if n % W != 0:
            return False
        
        cnt_dict = {}
        stop_dict = {}
        num_list = []
        for num in sorted(hand):
            if num not in cnt_dict:
                cnt_dict[num] = 1
                num_list.append(num)
            else:
                cnt_dict[num] += 1
        
        now = 0
        for num in num_list:
            if cnt_dict[num] < now:
                return False
            else:
                if cnt_dict[num] > now:
                    stop_num = num + W - 1
                    if cnt_dict.get(stop_num, 0) < cnt_dict[num] - now:
                        return False
                    stop_dict[stop_num] = cnt_dict[num] - now
                now = cnt_dict[num] - stop_dict.get(num, 0)
        
        return now == 0
```
