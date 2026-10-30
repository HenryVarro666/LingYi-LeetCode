---
title: "259. 较小的三数之和"
aliases: ["yiduobo的每日leetcode 259.较小的三数之和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/593237915"
zhihu_id: "593237915"
zhihu_title: "yiduobo的每日leetcode 259.较小的三数之和"
question_id: "259"
question: "较小的三数之和"
problem_url: "https://leetcode.cn/problems/3sum-smaller/"
created: "2022-12-20T22:20:31+08:00"
updated: "2022-12-20T22:20:31+08:00"
upvotes: 0
comments: 0
---

# 259. 较小的三数之和

> **[yiduobo的每日leetcode 259.较小的三数之和](https://zhuanlan.zhihu.com/p/593237915) · 知乎 · 2022-12-20 · 赞同 0**
> 力扣：[259. 较小的三数之和](https://leetcode.cn/problems/3sum-smaller/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

259.较小的三数之和

[力扣](https://leetcode.cn/problems/3sum-smaller/)

题目给出一个数组，问其中有多少个三元组满足三数之和小于target。

最直观的思路是枚举两个三元组中的两个数x、y，那么此时数组剩余的数中小于target - x - y的数都可以与x、y形成合法的三元组，那么在这里可以先统计每个数出现的次数cnt，然后对这个次数数组计算前缀和数组s，然后就可以通过s[target - x - y - 1]来高效获取小于target - x - y的数的数量了。

上面这个算法最大的问题就是可能出现重复的计算，需要想办法解决。

考察三元组的构成，可以将三元组分成三类：

1、三个相同的数。对于这种情况，可以从-100到100枚举这个数，不妨设为x。当x \* 3 \< target，且x出现次数cnt[x] >\= 3，那么就可以从这cnt[x]个x中任意选出3个构成一组合法的答案。这种情况下一共可以得到C(cnt[x], 3)种不同的三元组。

2、两个相同的数和另一个不同的数。对于这种情况，同样是从-100到100枚举这个相同的数，不妨设为x。当x \* 2 \< target时，另一个数就必须要小于r \= target - x \* 2，因此直观来看一共有C(cnt[x], 2) \* s[r - 1]种合法的情况。不过在这里需要注意的是，另一个数的取值不能等于x，因此当r - 1 >\= x时，合法情况的数量应该修正为C(cnt[x], 2) \* (s[r - 1] - cnt[x])。

3、最后一种情况就是三个不同的数。在这里需要使用最上面提到的算法，枚举x和y，然后通过s[target - x - y - 1]来更新答案。设最后一个数为v，那么v必须要小于r \= target - x - y。为了避免重复，不妨规定x \< y \< v，那么就有x \< y \< v \< r，可以发现，这里v的取值范围就是y + 1到r - 1，因此这种情况下合法情况的数量就应该是cnt[x] \* cnt[y] \* (s[r - 1] - s[y])，即利用前缀和来计算区间和。

再具体实现上，如果想使用数组下标而非哈希表，那么一开始需要对数组中的每个数加上100，将其变为非负数，同时将target加上300来适配这个变化。

最后附上python代码：

```python
class Solution(object):
    def threeSumSmaller(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """

        cnt = [0] * 201
        for num in nums:
            cnt[num + 100] += 1

        target += 300

        s = [cnt[0]]
        for v in range(1, 201):
            s.append(s[-1] + cnt[v])

        res = 0
        for x in range(0, min(200, target) + 1):
            if cnt[x] >= 3 and x * 3 < target:
                res += cnt[x] * (cnt[x] - 1) * (cnt[x] - 2) / 6

            if cnt[x] >= 2 and x * 2 < target:
                r = target - x * 2
                tmp = s[r - 1]
                if r - 1 >= x:
                    tmp -= cnt[x]
                res += (cnt[x] * (cnt[x] - 1) / 2) * tmp

            if cnt[x] > 0:
                for y in range(x + 1, min(200, target - x) + 1):
                    if cnt[y] > 0:
                        r = target - x - y
                        if r > y:
                            res += cnt[x] * cnt[y] * (s[r - 1] - s[y])

        return res
```
