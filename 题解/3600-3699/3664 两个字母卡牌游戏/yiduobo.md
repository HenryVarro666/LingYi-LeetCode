---
title: "3664. 两个字母卡牌游戏"
aliases: ["yiduobo的每日leetcode 3664.两个字母卡牌游戏"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/enumeration", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1950296425037566715"
zhihu_id: "1950296425037566715"
zhihu_title: "yiduobo的每日leetcode 3664.两个字母卡牌游戏"
question_id: "3664"
question: "两个字母卡牌游戏"
problem_url: "https://leetcode.cn/problems/two-letter-card-game/"
difficulty: "Medium"
rating: 2158
created: "2025-09-16T22:36:32+08:00"
updated: "2025-09-16T22:36:32+08:00"
upvotes: 1
comments: 0
---

# 3664. 两个字母卡牌游戏

> **[yiduobo的每日leetcode 3664.两个字母卡牌游戏](https://zhuanlan.zhihu.com/p/1950296425037566715) · 知乎 · 2025-09-16 · 赞同 1**
> 力扣：[3664. 两个字母卡牌游戏](https://leetcode.cn/problems/two-letter-card-game/) · Medium · 灵茶山艾府：[两种方法：枚举 / 直接计算（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3664.两个字母卡牌游戏

[3664. 两个字母卡牌游戏 - 力扣（LeetCode）](https://leetcode.cn/problems/two-letter-card-game/description/)

题目给出一副由字符串数组cards表示的牌，每张牌上都显示两个小写字母。

另外给出一个字母x，现在要求两张两张地从中移除cards中的牌。要求移除的牌对应的字符串都包含x，且这两个字符串恰好有一个位置上的字母是不同的。

问最多可以移除多少轮。

由于移除的牌对必须都包含x，因此可以直接忽略掉不包含x的卡牌。对于剩下的卡牌，根据其中x所在的位置可以分为三类，分别是xy、yx以及xx这三类。其中形如xy的卡牌只能与xx，或者与另一张形如xy且y不同的卡牌形成牌对。同样的，形如yx的卡牌只能与xx，或者与另一张形如yx且y不同的卡牌形成牌对。而对于形如xx的卡牌，其可以与任意xy或者yx形成牌对，但是不能与另一张xx形成牌对。

基于以上的规则，可以先处理特殊情况：当xx的数量特别多，超出所有的xy与yx的数量之和时，可以让xx与所有的xy或者yx都形成牌对，而剩下的xx则无法使用了，此时的答案就是所有xy与yx的数量之和。

反之，若xx的数量没那么多，则需要优先在xy和yx的内部进行配对，而xx则应该作为补位的卡牌来使用。

接下来考虑形如xy的卡牌内部应该如何配对。由于对称性，形如yx的卡牌配对也可以选择相同的方案。

对于所有形如xy的卡牌，由于每次需要选择两个恰好有一个位置不同的卡牌对，而x是固定好了的，换言之，在这里就必须选择两张y不同的卡牌进行配对。对于这个问题，之前应该有个类似的但是忘记题号了，不过结论也很简单：若其中某种卡牌出现的次数大于总数的一半，那么即使让这种卡牌与其他所有的卡牌一一配对，依然会预留一些无法配对的，配对的总数就是卡牌总数减去这种卡牌出现的次数，剩下的卡牌可以考虑与xx进行配对；反之，则可以通过每次选择出现次数最多的两种卡牌进行配对的方式来完成配对，可以形成的配对数量就是卡牌总数整除2，若总数为奇数，则还会余下一张，可以考虑与xx进行配对。

而对于所有没有内部匹配的卡牌，可以尝试将这些卡排与xx进行配对。若xx的数量不够多，那么有多少匹配多少；如果xx的数量够多，则可以尝试将已经内部配对的xy或者yx拆散，然后与xx进行配对，将所有xx的作用都发挥出来。

基于以上的结论，就得到了一种做法：

将xy的总数，内部可以配对的卡牌对数量，以及内部配对后剩余的卡牌数量分别记为tot_xy，pair_xy以及rest_xy，而对于yx则分别记录tot_yx，pair_yx，rest_yx，同时记录xx的数量，那么：

1、若tot_xy + tot_yx \< xx：

此时就是xx特别多的情况，答案就是tot_xy + tot_yx

2、若tot_xy + tot_yx >\= xx：

此时先进行内部配对，配对的数量为pair_xy + pair_yx。对于剩下的rest_xy以及rest_yx，考虑可以通过xx形成的额外配对数量：

2-1）若rest_xy + rest_yx > xx：

此时说明xx的数量不够多，尽量去匹配剩下的xy和yx，一共也只能匹配xx对，因此额外配对数量就是xx对

2-2）若rest_xy + rest_yx \<\= xx：

此时xx的数量足够多，在满足了所有rest_xy以及rest_yx的配对需求后，剩下的xx则可以通过拆分已经内部配对的xy或者yx来实现配对。由于此时有一个大前提是tot_xy + tot_yx >\= xx，因此在这里必然不会出现不够拆的情况，也就是xx可以全部用上，因此额外配对数量就是(rest_xy + rest_yx + xx) // 2

最后附上python代码：

```python
class Solution(object):
    def score(self, cards, x):
        """
        :type cards: List[str]
        :type x: str
        :rtype: int
        """
        
        xx = 0
        xy = {}
        yx = {}
        for c in cards:
            if c[0] == x:
                if c[1] == x:
                    xx += 1
                else:
                    xy[c] = xy.get(c, 0) + 1
            elif c[1] == x:
                yx[c] = yx.get(c, 0) + 1

        def calc(cnt):
            tot = 0
            ma = 0
            for v in cnt.values():
                tot += v
                ma = max(ma, v)

            if tot - ma >= ma:
                pair = tot // 2
            else:
                pair = tot - ma
            rest = tot - pair * 2
            return tot, pair, rest

        tot_xy, pair_xy, rest_xy = calc(xy)
        tot_yx, pair_yx, rest_yx = calc(yx)

        if tot_xy + tot_yx < xx:
            return tot_xy + tot_yx
        
        res = pair_xy + pair_yx
        if rest_xy + rest_yx > xx:
            res += xx
        else:
            res += (rest_xy + rest_yx + xx) // 2
        
        return res
```
