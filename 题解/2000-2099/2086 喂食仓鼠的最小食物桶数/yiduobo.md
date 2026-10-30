---
title: "2086. 从房屋收集雨水需要的最少水桶数"
aliases: ["yiduobo的每日leetcode 2086.从房屋收集雨水需要的最少水桶数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/string", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/518153221"
zhihu_id: "518153221"
zhihu_title: "yiduobo的每日leetcode 2086.从房屋收集雨水需要的最少水桶数"
question_id: "2086"
question: "喂食仓鼠的最小食物桶数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-food-buckets-to-feed-the-hamsters/"
difficulty: "Medium"
rating: 1623
created: "2022-05-22T12:10:22+08:00"
updated: "2022-05-22T12:10:22+08:00"
upvotes: 0
comments: 0
---

# 2086. 从房屋收集雨水需要的最少水桶数

> **[yiduobo的每日leetcode 2086.从房屋收集雨水需要的最少水桶数](https://zhuanlan.zhihu.com/p/518153221) · 知乎 · 2022-05-22 · 赞同 0**
> 力扣：[2086. 喂食仓鼠的最小食物桶数](https://leetcode.cn/problems/minimum-number-of-food-buckets-to-feed-the-hamsters/) · Medium · 灵茶山艾府：[贪心：O(n) 一次遍历 + O(1) 额外空间](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2086.从房屋收集雨水需要的最少水桶数

[力扣](https://leetcode.cn/problems/minimum-number-of-buckets-required-to-collect-rainwater-from-houses/)

题目要求每一栋房子都有水桶相邻，那么不妨从最左侧且没有相邻水桶的房子来考虑。对于这栋房子，需要在其左侧或者右侧安置一个水桶。很明显，如果其右侧可以安置水桶，那么就应该将水桶安置在其右侧，因为这样一来这个水桶还有可能惠及到下一栋房子，而如果将水桶安置在左侧，那么这个水桶就只能收集到这一栋房子的雨水了。

根据上面的结论，可以从左向右一趟遍历，对于当前的房子，先判断其左侧是否已经有了水桶。若有，那么无需再为这栋房子安排水桶，直接跳过考虑下一栋房子，否则的话先尝试在这栋房子的右侧安置一个水桶，并更新答案。若这栋房子的右侧无法安置水桶，那么就尝试在其左侧安置一个水桶，并更新答案。若其左侧也无法安置水桶，那么这栋房子的雨水无法收集，直接返回-1。

最后附上python代码：

```python
class Solution(object):
    def minimumBuckets(self, street):
        """
        :type street: str
        :rtype: int
        """

        street_list = list(street)
        res = 0
        n = len(street_list)
        for index in range(n):
            if street_list[index] == 'H':
                if index - 1 >= 0 and street_list[index - 1] == 'B':
                    continue

                if index + 1 < n and street_list[index + 1] == '.':
                    street_list[index + 1] = 'B'
                elif index - 1 >= 0 and street_list[index - 1] == '.':
                    street_list[index - 1] = 'B'
                else:
                    return -1
                
                res += 1
        
        return res
```
