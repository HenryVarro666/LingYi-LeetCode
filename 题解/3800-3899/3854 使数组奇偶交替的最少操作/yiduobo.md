---
title: "3854. 使数组奇偶交替的最少操作"
aliases: ["yiduobo的每日leetcode 3854.使数组奇偶交替的最少操作"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2012567898594485263"
zhihu_id: "2012567898594485263"
zhihu_title: "yiduobo的每日leetcode 3854.使数组奇偶交替的最少操作"
question_id: "3854"
question: "使数组奇偶交替的最少操作"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-array-parity-alternating/"
difficulty: "Medium"
rating: 2095
created: "2026-03-06T01:44:00+08:00"
updated: "2026-03-06T01:44:00+08:00"
upvotes: 1
comments: 0
---

# 3854. 使数组奇偶交替的最少操作

> **[yiduobo的每日leetcode 3854.使数组奇偶交替的最少操作](https://zhuanlan.zhihu.com/p/2012567898594485263) · 知乎 · 2026-03-06 · 赞同 1**
> 力扣：[3854. 使数组奇偶交替的最少操作](https://leetcode.cn/problems/minimum-operations-to-make-array-parity-alternating/) · Medium · 灵茶山艾府：[贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3854.使数组奇偶交替的最少操作

<https://leetcode.cn/problems/minimum-operations-to-make-array-parity-alternating/description/>

题目给出一个整数数组nums。

对于数组中满足0 \<\= index \< n - 1的任意下标index，若nums[index]与nums[index + 1]的奇偶性不同，则称该数组是奇偶交替的。

在一次操作中，可以选择任意下标index，让nums[index]加上1或者减去1。

要求返回一个长度为2的整数数组answer，其中

- answer[0]表示使得数组变为奇偶交替所需的最少操作次数
- answer[1]表示通过最少的操作次数使得nums变为奇偶交替的前提下，max(nums) - min(nums)的最小可能值

为了使得数组奇偶交替，那么数组最后一定是奇-偶-奇-偶-...的形式，或者偶-奇-偶-奇-...的形式，于是可以先对nums进行一趟遍历，使用数组f记录在偶数下标上的偶数，以及在奇数下标上的奇数，使用数组g记录在偶数下班上的奇数，以及在奇数下标上的偶数。接下来，只需要修改f中所有元素的奇偶性，或者修改g中所有元素的奇偶性，就能让数组变得奇偶交替了。

为了使得修改的次数最短，在这里就应该先比较f和g的长度，选择修改长度较短的那一个。若二者长度相同，则两种情况都需要考虑。方便起见，在这里记保持不变的数组为ori，需要修改的数组为modify，接下来就需要考虑如何修改modify，使得修改后max(max(ori), max(modify)) - min(min(ori), min(modify))最小。

由于ori中的元素保持不变，因此可以先对ori进行一趟遍历，记录其中的最大值ma_o以及最小值mi_o。

接下来需要分情况讨论如何进行修改。

1、当ma_o严格大于mi_o时：

对于这种情况，可以进一步分情况讨论modify中的元素x与ma_o与mi_o的大小关系。

若x \<\= mi_o，就应该将x变为x + 1，这样一来可以使得数组的最小值尽可能大，同时这个x + 1也不会超过ma_o

若x >\= ma_o，就应该将x变为x - 1，这样一来可以使得数组的最大值尽可能小，同时这个x - 1也不会小于mi_o

若mi_o \< x \< ma_o，此时可以对x进行任意操作，因为x都不可能越过mi_o以及ma_o

综合上面的结论，此时就应该将modify中小于等于mi_o的元素都加上1，取其中的最小值，再与mi_o取较小值，就得到了最终数组中的最小值。同理，取modify中大于等于ma_o的元素减去1之后的最大值，再与ma_o取较小值，就得到了最终数组中的最大值。

更进一步的，上面的过程可以简化成先取modify中的最小值，加上1然后与mi_o取较小值，以及取modify中的最大值，减去1然后与ma_o取较大值。

方便起见，在这里可以也先对modify进行一趟遍历，记录其中的最大值ma_m以及最小值mi_m，那么当ma_o > mi_o时，最终数组的最大值就是max(ma_o, ma_m - 1)，最小值就是min(mi_o, mi_m - 1)

2、当ma_o等于mi_o时：

ma_o等于mi_o隐藏的信息其实非常多。

首先，ma_o等于mi_o，意味着ori中所有元素的奇偶性都相同，而它们都属于ori，因此这些元素都位于奇数下标，或者偶数下标。另一方面，由于ori的长度天然大于等于modify的长度，因此ori必然覆盖了所有的奇数下标或者偶数下标。

对于modify而言，其中所有元素的奇偶性都需要进行调整，而这些元素都属于非ori占据的另一种下标，也就是说modify中所有元素的奇偶性与ori是相同的。更进一步的，对于modify中的两个不同元素x和y，二者之差至少为2。

需要注意，这种情况下，若modify中的某个元素x恰好等于ma_o时，其操作的方向就比较复杂了，因为此时的x变成x - 1或者x + 1都会影响到数组的上下界，而这个界应该要配合其他元素一起决定，例如当其他元素都小于ma_o时，将x变为x - 1显然更优。因此，在这里还需要结合ma_m以及mi_m的大小进行讨论。

2-1）若ma_m等于mi_m：

这种情况下，尽量让ma_m向ma_o靠拢就行了。具体来说，若ma_m更小，答案就是ma_o - (ma_m + 1)，若ma_o更小，答案就是(ma_m - 1) - ma_o，若二者相等，答案就是1

2-2）若mi_m \< ma_m \<\= ma_o：

由于modify中不同元素之差至少为2，因此在这里就应该将modify中所有等于mi_m的元素都加上1，其他元素都减去1，这样可以保证所有元素都不超过ma_o，同时最小值也最大，为mi_m + 1，因此最终答案为ma_o - (mi_m + 1)

2-3）若ma_o \<\= mi_m \< ma_m：

与2-2对称，此时就应该将modify中所有等于ma_m的元素减去1，其他元素都加上1，此时的最大值就是ma_m - 1，最终答案就是(ma_m - 1) - ma_o

2-4）若mi_m \< ma_o \< ma_m：

回顾之前的讨论，ori中的元素与modify中的元素奇偶性相同，因此mi_m与ma_o的差至少为2，ma_o与ma_m的差也至少为2，因此在这里就应该将modify中所有等于mi_m的元素加上1，所有等于ma_m的元素减去1，其他元素则可以任意操作，而最终答案就是ma_m - 1 - (mi_m + 1)

最后附上python代码：

```python
class Solution(object):
    def makeParityAlternating(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        
        def calc(ori, modify):
            ma_o, mi_o = ori[0], ori[0]
            for v in ori[1:]:
                ma_o = max(ma_o, v)
                mi_o = min(mi_o, v)
            
            if not modify:
                return ma_o - mi_o
            
            ma_m, mi_m = modify[0], modify[0]
            for v in modify[1:]:
                ma_m = max(ma_m, v)
                mi_m = min(mi_m, v)
            
            if ma_o > mi_o:
                mi = min(mi_o, mi_m + 1)
                ma = max(ma_o, ma_m - 1)
                return ma - mi
            
            if ma_m == mi_m:
                if ma_m < ma_o:
                    return ma_o - ma_m - 1
                elif ma_m == ma_o:
                    return 1
                else:
                    return ma_m - ma_o - 1
            
            if ma_m <= ma_o:
                return ma_o - mi_m - 1
            elif ma_o <= mi_m:
                return ma_m - ma_o - 1
            else:
                return ma_m - mi_m - 2

        f = []
        g = []
        for index, v in enumerate(nums):
            if index % 2 == v % 2:
                f.append(v)
            else:
                g.append(v)
        
        

        if len(f) > len(g):
            return [len(g), calc(f, g)]
        elif len(f) < len(g):
            return [len(f), calc(g, f)]
        else:
            return [len(f), min(calc(f, g), calc(g, f))]
```
