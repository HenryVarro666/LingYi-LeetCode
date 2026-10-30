---
title: "LCP 40. 心算挑战"
aliases: ["yiduobo的每日leetcode LCP40.心算挑战"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/quickselect", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/575698386"
zhihu_id: "575698386"
zhihu_title: "yiduobo的每日leetcode LCP40.心算挑战"
question_id: "LCP 40"
question: "心算挑战"
problem_url: "https://leetcode.cn/problems/uOAnQW/"
difficulty: "Easy"
created: "2022-10-21T00:24:42+08:00"
updated: "2022-10-21T00:24:42+08:00"
upvotes: 0
comments: 0
---

# LCP 40. 心算挑战

> **[yiduobo的每日leetcode LCP40.心算挑战](https://zhuanlan.zhihu.com/p/575698386) · 知乎 · 2022-10-21 · 赞同 0**
> 力扣：[LCP 40. 心算挑战](https://leetcode.cn/problems/uOAnQW/) · Easy · 灵茶山艾府：[排序+贪心（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP40.心算挑战

[力扣](https://leetcode.cn/problems/uOAnQW/)

题目要求最终选出来的数字和为偶数，那么最后答案一定是由偶数个奇数卡牌以及部分偶数卡牌组成。为了使得答案最大，就应该优先选择数值较大的卡牌。于是可以分奇偶从大到小进行排序，然后枚举最终选择的奇数卡牌数量odd_cnt。这种情况下，选择的卡牌就是最大的odd_cnt张奇数卡牌以及最大的cnt - odd_cnt张偶数卡牌，使用这些卡牌的和更新答案即可。

另外需要注意的是，当cnt - odd_cnt大于偶数卡牌的总数时是无法进行选择的。

最后附上python代码：

```python
class Solution(object):
    def maxmiumScore(self, cards, cnt):
        """
        :type cards: List[int]
        :type cnt: int
        :rtype: int
        """

        odd = []
        even = []
        for num in cards:
            if num % 2 == 0:
                even.append(num)
            else:
                odd.append(num)
        
        even.sort(reverse=True)
        odd.sort(reverse=True)

        even_s = [0]
        for num in even:
            even_s.append(even_s[-1] + num)
        odd_s = [0]
        for num in odd:
            odd_s.append(odd_s[-1] + num)
        
        res = 0
        for odd_cnt in range(0, min(len(odd), cnt) + 1, 2):
            if cnt - odd_cnt > len(even):
                continue

            res = max(res, odd_s[odd_cnt] + even_s[cnt - odd_cnt])
        
        return res
```
