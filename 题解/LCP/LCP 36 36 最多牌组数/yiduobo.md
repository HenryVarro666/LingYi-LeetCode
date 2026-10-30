---
title: "LCP 36. 最多牌组数"
aliases: ["yiduobo的每日leetcode LCP36.最多牌组数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/574959242"
zhihu_id: "574959242"
zhihu_title: "yiduobo的每日leetcode LCP36.最多牌组数"
question_id: "LCP 36"
question: "最多牌组数"
created: "2022-10-19T03:00:51+08:00"
updated: "2022-10-19T03:00:51+08:00"
upvotes: 0
comments: 1
---

# LCP 36. 最多牌组数

> **[yiduobo的每日leetcode LCP36.最多牌组数](https://zhuanlan.zhihu.com/p/574959242) · 知乎 · 2022-10-19 · 赞同 0**
> 力扣：LCP 36. 最多牌组数

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP36.最多牌组数

[力扣](https://leetcode.cn/problems/Up5XYM/)

打过国标麻将的同学都知道，对于三组同色的顺子，可以从一色三同顺和一色三节高里面选一种计分，即对于三组123万，既可以选择原样计算3组123万的一色三同顺，也可以选择计算1万、2万、3万形成的3组刻子。虽然计分上都是24番，但是前者可以配合平胡等，后者则可以配合碰碰胡等，总的来说就是，怎么算赢得多就怎么算。

对于本题，则是怎么算方便怎么算。很明显，计算3组123就不如分别计算3个1、2、3来得方便，那么在这里就可以默认，以k结尾的k - 2、k - 1、k形成的顺子不会超过两组。这样一来，就可以得到一种动态规划的状态表示，即对于排序并聚合过的牌来说，f[i][state]表示前i种牌，以第i - 1种牌结尾的顺子数量以及第i种牌记为的顺子数量组成的状态为state时，可以得到的最多牌组数，那么这里state的取值范围就是一个两位三进制数，取值范围为0到8，其中高位的3进制数表示以第i - 1种牌结尾的顺子数量，而低位的3进制数则表示以第i种牌结尾的顺子数量。

于是可以先将所有牌按牌面聚合起来，然后从小到大进行排序。设第i种牌的大小为v[i]，数量为cnt[i]，那么对于f[i]：

1、首先考虑边界情况。当i \< 2时，不可能形成任何顺子，于是有f[0][0] \= cnt[0] / 3，f[1][0] \= f[0][0] + cnt[1] / 3，表示v[0]和v[1]这两种牌形成的刻子数量。对于其他的state，则全部初始化为0。

2、接下来是一般情况。首先从0到8枚举state，那么对于f[i][state]，可以先通过state分别计算出以v[i]和v[i - 1]结尾的顺子数量，分别记为now_straight和last_straight。接下来：

2-1）若now_straight比cnt[i]还要大，那么就不可能凑够now_straight个以v[i]结尾的顺子，此时有f[i][state] \= 0

2-2）同样的，若now_straight + last_straight比cnt[i - 1]还要大，那么同样是f[i][state] \= 0

2-3）若now_straight大于0，且v[i]、v[i - 1]、v[i - 2]并不是相差为1的等差数列，那么就不可能形成以v[i]结尾的任何顺子，此时同样有f[i][state] \= 0

如果上述三种情况都不满足，那么就从0到2枚举以v[i - 2]结尾的顺子数量two_round_straight，通过two_round_straight以及last_straight计算出上一轮的状态last_state，然后尝试用f[i - 1][last_state]来更新当前f[i][state]的最大值。对于当前的two_round_straight：

2-4）与2-1以及2-2相同，在这里也需要检测now_straight + last_straight + two_round_straight是否大于cnt[i - 2]，若大于，那么说明v[i - 2]的数量不足以支撑f[i - 1][last_state]以及f[i][state]这两个状态同时存在，也就不可能从f[i - 1][last_state]转移到f[i][state]了

2-5）否则在面上看来，在f[i - 1][last_state]的基础上，形成了now_straight组顺子，以及(cnt[i] - now_straight]) / 3组刻子，那么可以使用三者之和

tmp \= f[i - 1][last_state] + now_straight + (cnt[i] - now_straight) / 3

来更新f[i][state]。不过需要注意的是，这里形成的now_straight组顺子消耗掉了等量的v[i - 1]以及v[i - 2]，虽然上面的前置计算保证了last_straight和two_round_straight不受影响，但是可能会影响到f[i - 1][last_state]中刻子的数量，即拆开了其中的刻子才能组成以v[i]结尾的顺子。

一种比较简单的计算思路就是，对于last_straight而言，其消耗掉了等量的v[i - 1]，那么剩余的v[i - 1]的数量就是cnt[i - 1] - last_straight。对于这些v[i - 1]，将会3个一组形成刻子，那么剩下空闲的v[i - 1]就是(cnt[i - 1] - last_straight) % 3。首先可以尝试使用这些v[i - 1]来凑now_straight，若数量不够，则需要拆开一个v[i - 1]形成的刻子，此时tmp应该减去1。

同样的，对于last_straight和two_round_straight而言，其消耗掉了二者之和个v[i - 2]，那么剩余的v[i - 2]就是cnt[i - 2] - last_straight - two_round_straight。组成刻子后剩余的数量同样是模3，同这个剩余的数量想来凑now_straight，若不够，那么还需要拆开一个v[i - 2]形成的刻子，此时tmp应该减去1。

得到最终的tmp后，就可以使用tmp来更新f[i][state]了。

全部计算完成后，max(f[-1])就是最终答案了。另外，就直观感受来说，2-5中拆刻子凑顺子的行为似乎是不赚的，因为这样相当于浪费了前面的v[i - 1]和v[i - 2]。如果保留原来的刻子，那么本轮虽然没有凑出顺子，但是保留了v[i]可能可以供后续使用。所以对于上述的状态表示应该还存在一定的优化空间，不过O(9n)的复杂度已经足够应付本题了，我就没有继续往下思考了。

最后附上python代码：

```python
class Solution(object):
    def maxGroupNumber(self, tiles):
        """
        :type tiles: List[int]
        :rtype: int
        """

        cnt_dict = {}
        for tile in tiles:
            cnt_dict[tile] = cnt_dict.get(tile, 0) + 1
        
        cnt_info = sorted(cnt_dict.items(), key=lambda d:d[0])
        if len(cnt_info) <= 2:
            res = 0
            for tile, cnt in cnt_info:
                res += cnt / 3
            return res
        
        n = len(cnt_info)
        f = [[0] * 9 for _ in range(n)]
        f[0][0] = cnt_info[0][1] / 3
        f[1][0] = f[0][0] + cnt_info[1][1] / 3
        for i in range(2, n):
            tile, cnt = cnt_info[i]
            for state in range(9):
                now_straight = state % 3
                last_straight = state / 3
                if now_straight > cnt:
                    continue
                if now_straight + last_straight > cnt_info[i - 1][1]:
                    continue
                if now_straight > 0 and (cnt_info[i][0] != cnt_info[i - 1][0] + 1 or cnt_info[i - 1][0] != cnt_info[i - 2][0] + 1):
                    continue

                for two_round_straight in range(3):
                    if two_round_straight + last_straight + now_straight > cnt_info[i - 2][1]:
                        continue
                    last_state = two_round_straight * 3 + last_straight
                    tmp = f[i - 1][last_state] + now_straight + (cnt - now_straight) / 3
                    if (cnt_info[i - 1][1] - last_straight) % 3 < now_straight:
                        tmp -= 1
                    if (cnt_info[i - 2][1] - last_straight - two_round_straight) % 3 < now_straight:
                        tmp -= 1
                    f[i][state] = max(f[i][state], tmp)

        return max(f[-1])
```
