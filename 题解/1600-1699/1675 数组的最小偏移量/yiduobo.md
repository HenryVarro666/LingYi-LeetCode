---
title: "1675. 数组的最小偏移量"
aliases: ["yiduobo的每日leetcode 1675.数组的最小偏移量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/444432521"
zhihu_id: "444432521"
zhihu_title: "yiduobo的每日leetcode 1675.数组的最小偏移量"
question_id: "1675"
question: "数组的最小偏移量"
problem_url: "https://leetcode.cn/problems/minimize-deviation-in-array/"
created: "2021-12-12T20:43:28+08:00"
updated: "2021-12-12T20:43:28+08:00"
upvotes: 1
comments: 0
---

# 1675. 数组的最小偏移量

> **[yiduobo的每日leetcode 1675.数组的最小偏移量](https://zhuanlan.zhihu.com/p/444432521) · 知乎 · 2021-12-12 · 赞同 1**
> 力扣：[1675. 数组的最小偏移量](https://leetcode.cn/problems/minimize-deviation-in-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1675.数组的最小偏移量

[力扣](https://leetcode-cn.com/problems/minimize-deviation-in-array/)

看到题目数据的规模就知道只能用贪心法来做，但是贪心的标准不太好找，需要仔细分析题目中的两种变换存在什么规律。

对于数组中的奇数x，其可以保持不变，或者变换成x \* 2

对于数组中的偶数，将其2的因子提出来之后可以写成a \* 2^b的形式，那么其取值的范围就是a \* 2^k，其中k为0到b之间的整数。

实际上，奇数也可以写成a \* 2^b的形式，这里的b等于0，而取值范围则是a \* 2^0或者a \* 2^1

首先考察边界情况。如果将所有的数写成a \* 2^b这种形式之后所有的a都一样，那么就可以将所有数都转换成a，此时的答案就是0。

接下来考虑一般的情况。如果不满足所有的a都一样，那么答案必然大于0。不妨记答案中的最大值为maximum，最小值为minimum，那么答案就是maximum - minimum。

可以明确的一点是，最终答案不可能都是偶数。如果所有的数都是偶数，那么完全可以将所有数都除以2，此时的最大值和最小值就变成了maximum / 2以及minimum / 2，这里都是可以整除的，而二者的差就变成了(maximun - minimun) / 2，这个值必然小于之前的maximum - minimum。

那么是否答案中都是奇数呢？同样是不成立的，例如[3, 5]就不如[6, 5]。

也就是说，最终答案中存在奇数，但是并不要求全都是奇数。于是一个很自然的想法就是，在任意情况下是否存在某一类奇数必然出现在答案中，考虑的方向就只有将所有数写成a \* 2^b这种形式后最大的a以及最小的a。

最小的a直接就可以排除掉，例如上面[3, 5]不如[6, 5]的例子，3不是必须的。

接下来考察最大的a是否一定会出现在答案中。由于找不出反例，那么需要想办法证明。记最大的a为max_a，那么若某种情况下max_a没有出现在答案中，由于答案中至少要有一个奇数，那么必然存在一个a' \< max_a存在于答案中，而max_a则是通过max_a \* 2^b的形式存在，这里的b大于等于1。

如果将其转化为max_a：

此时maximum可能会变小，但这个maximum依然大于a'

此时minimum不会发生变化，因为有mimimun \<\= a' \< a

换言之，此时如果将max_a \* 2^b转换成max_a，答案可能更优但不会更差，这就说明max_a一定会存在于最优的答案中。

根据上面的结论，就可以先将每个数写成a \* 2^b的形式，然后从中选出最大的a，记为max_a。此时需要初始化答案中可能的最大值p_max以及可能的最小值p_min为max_a。

为了使得答案最小，就应该让其他的数尽量靠近max_a，此时又可以分成下面几种情况：

1、当前的num为奇数，且num >\= max_a：

此时应该让num保持不变。另外由于num可能就是答案中的最大值，因此需要使用num来更新p_max

2、当前的num为奇数，且num \* 2 \< max_a：

此时应该让num乘以2。类似的，需要用num \* 2来更新p_min

3、当前的num为奇数，且num \< max_a，num \* 2 > max_a：

就单从num的角度而言，根据max_a - num以及num \* 2 - max_a的大小是可以判断应该如何处理的，但是可能存在其他的数覆盖住了差值较大的那一侧。

例如[2, 3, 5]，此时的max_a为5。对于3而言，保持不动时与5的差为2，乘以2之后变成6，与5的差为1。虽然但从3的角度而言应该选择变成6，但是实际上由于还存在一个2覆盖住了3，因此此时的3应该保持不变。

也就是说，对于这种情况在当前是无法给出判断的，因此需要将num加入到待定数组tdb_list当中，之后再对这个数组中的数一并考虑

4、当前的num为偶数，且num \< max_a：

此时应该让num保持不变。需要用num来更新p_min

5、当前num为偶数，且num > max_a：

将num写成a \* 2^b，若此时的a等于max_a，那么自然是将num转化成max_a的形式，之后无需进行任何操作。其他情况下，必然与a \< max_a，那么必然存在一个k，满足a \* 2^k \< max_a \< a \* 2^(k + 1)

与情况3类似，此时应该以a \* 2^k还是a \* 2^(k + 1)存在于答案中还无法确定，因此需要将a \* 2^k加入到tbd_list中

若tbd_list为空，那么说明所有数都已经确定了最终形态，此时的最大值就是p_max，而最小值就是p_min，答案就是p_max - p_min。

接下来考虑tbd_list不为空的情况。

可以发现，tbd_list中的数都满足其自然小于max_a，但其乘以2之后大于max_a。换言之，如果tdb_list中的数保持不变，那么可能影响到最小值，如果其乘以2，那么可能影响到最大值。

对于tdb_list中的两个数x和y，若x \< y，那么单独对y执行乘以2是没有必要的。用y \* 2替代y之后，此时的最大值可能变得更大，但此时的最小值由于有x保底，那么必然是不变的。这样来看的话单独对y执行乘以2操作只会让差值变得更大。换言之，若最终对y执行了乘以2操作，那么也必须要对x执行乘以2操作。

根据上面的结论，实际上就是需要找到一个threshold，对于小于等于threshold的数执行乘以2操作，大于threshold的数保持不变，使得最终的偏移量最小。

那么可以对tbd_list从小到大进行排序。初始情况自然是所有数都不乘以2，此时的最大值max_now就等于max(p_max, tdb_list[-1])，而最小值min_now就等于min(p_min, tdb_list[0])。使用max_now - min_now来初始化答案。

接下来从头开始枚举tbd_list的数，并选择这个数作为threshold，那么对于第index个数而言，tbd_list中的数当前的形态就是

tdb_list[0] \* 2, tdb_list[1] \* 2, ..., tdb_list[index] \* 2以及tdb_list[index + 1], ..., tdb_list[-1]

此时的最大值max_now就是max(p_max, tdb_list[index] \* 2, tdb_list[-1])

此时的最小值min_now则是min(p_min, tdb_list[0] \* 2, tdb_list[index + 1])

然后使用max_now - min_now来更新答案即可

另外需要注意另一侧的边界情况，即index到达tdb_list末尾时，此时是不存在tdb_list[-1]和tdb_list[index + 1]

最后附上python代码：

```python
class Solution(object):
    def minimumDeviation(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        max_a = 0
        flag = True
        for index, num in enumerate(nums):
            while num & 1 == 0:
                num >>= 1
            
            if max_a != 0 and max_a != num:
                flag = False
            max_a = max(max_a, num)
        
        if flag:
            return 0

        p_max = p_min = max_a
        tbd_list = []
        for index, num in enumerate(nums):
            if num & 1:
                if num >= max_a:
                    p_max = max(p_max, num)
                elif num * 2 < max_a:
                    p_min = min(p_min, num * 2)
                else:
                    tbd_list.append(num)
            else:
                if num < max_a:
                    p_min = min(p_min, num)
                else:
                    while num & 1 == 0 and num > max_a:
                        num >>= 1
                    
                    if num == max_a:
                        continue
                    tbd_list.append(num)

        if not tbd_list:
            return p_max - p_min

        tbd_list.sort()
        res = max(p_max, tbd_list[-1]) - min(p_min, tbd_list[0])

        for index, num in enumerate(tbd_list):
            now_min = min(p_min, tbd_list[0] * 2)
            now_max = max(p_max, num * 2)
            if index < len(tbd_list) - 1:
                now_min = min(now_min, tbd_list[index + 1])
                now_max = max(now_max, tbd_list[-1])
            
            res = min(res, now_max - now_min)
        
        return res
```
