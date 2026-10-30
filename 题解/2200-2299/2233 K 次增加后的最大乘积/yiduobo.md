---
title: "2233. K次增加后的最大乘积"
aliases: ["yiduobo的每日leetcode 2233.K次增加后的最大乘积"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/heap", "leetcode/greedy", "leetcode/math", "leetcode/you-xian-dui-lie", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/544211148"
zhihu_id: "544211148"
zhihu_title: "yiduobo的每日leetcode 2233.K次增加后的最大乘积"
question_id: "2233"
question: "K 次增加后的最大乘积"
problem_url: "https://leetcode.cn/problems/maximum-product-after-k-increments/"
difficulty: "Medium"
rating: 1686
created: "2022-07-21T01:15:17+08:00"
updated: "2022-07-21T01:15:17+08:00"
upvotes: 0
comments: 0
---

# 2233. K次增加后的最大乘积

> **[yiduobo的每日leetcode 2233.K次增加后的最大乘积](https://zhuanlan.zhihu.com/p/544211148) · 知乎 · 2022-07-21 · 赞同 0**
> 力扣：[2233. K 次增加后的最大乘积](https://leetcode.cn/problems/maximum-product-after-k-increments/) · Medium · 灵茶山艾府：[贪心：每次给最小的元素加一](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2233.K次增加后的最大乘积

[力扣](https://leetcode.cn/problems/maximum-product-after-k-increments/)

首先可以明确的一点是，每一次都应该将当前的最小值加1。一个简单的证明是假设当前这一轮的操作没有增加最小值，那么：

1、若后续的轮次操作了最小值，那么可以将这两轮的操作互换，视为当前这一轮操作了最小值。互换是不影响最终答案的

2、若后续的轮次都没有操作最小值，那么将任意一轮的操作改成操作最小值都可以使得乘积变得更大

有了这个结论，又由于操作的总次数k的规模是在可以遍历的范围内，因此可以使用一个最小堆来维护当前数组，堆顶元素即为每一轮的最小值。

我采用的做法是先统计每个数出现的次数，然后按数值的大小从小到大将这个次数数组进行排序，得到数组sorted_cnt，其中sorted_cnt[index][0]表示数组中第index小的数的数值，而sorted_cnt[index][1]则表示这个数值出现的次数。

接下来使用一个遍历now记录当前数组中最小值出现的次数，初始化就是sorted_cnt[0][1]。然后从下标1开始，从小到大遍历sorted_cnt。对于当前的index而言，sorted_cnt[index - 1][0]就是数组中的最小值，而sorted_cnt[index][0]则是数组中的次小值。根据最开始的结论，初始的操作必然是全部用在当前的最小值，也就是sorted_cnt[index - 1][0]上。于是可以计算需要多少次操作才能使得当前所有的sorted_cnt[index - 1][0]变为sorted_cnt[index][0]。

二者的差值diff \= sorted_cnt[index][0] - sorted_cnt[index - 1][0]，而当前一共有now个最小值，因此需要的操作数为diff \* now。接下来判断这个值与剩余的k的大小。若k还足够，那么就将所有的最小值都变为了sorted_cnt[index][0]，此时的now则变为了now + sorted_index][1]。若k不够了，那么就需要将这k次操作平均分给这now个sorted_cnt[index - 1][0]。

另外还有一种情况是数组中的所有数都变成原数组中的最大值，此时同样是要将剩余的操作次数平均分给数组中的每个数。

最后附上python代码：

```python
class Solution(object):
    def maximumProduct(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        cnt_dict = {}
        for num in nums:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        sorted_cnt = sorted(cnt_dict.items(), key=lambda d:d[0])

        mod = 10 ** 9 + 7
        now = sorted_cnt[0][1]
        for index in range(1, len(sorted_cnt)):
            diff = sorted_cnt[index][0] - sorted_cnt[index - 1][0]
            if diff * now <= k:
                k -= diff * now
                now += sorted_cnt[index][1]
            else:
                res = 1
                for num, cnt in sorted_cnt[index:]:
                    for _ in range(cnt):
                        res = res * num % mod
                
                delta = k / now
                k %= now
                for _ in range(k):
                    res = res * (sorted_cnt[index - 1][0] + delta + 1) % mod
                for _ in range(k, now):
                    res = res * (sorted_cnt[index - 1][0] + delta) % mod
                
                return res

        res = 1
        delta = k / now
        k %= now
        for _ in range(k):
            res = res * (sorted_cnt[-1][0] + delta + 1) % mod
        for _ in range(k, now):
            res = res * (sorted_cnt[-1][0] + delta) % mod
        
        return res
```
