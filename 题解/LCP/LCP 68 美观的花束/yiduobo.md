---
title: "LCP 68. 美观的花束"
aliases: ["yiduobo的每日leetcode LCP68.美观的花束"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/580213177"
zhihu_id: "580213177"
zhihu_title: "yiduobo的每日leetcode LCP68.美观的花束"
question_id: "LCP 68"
question: "美观的花束"
problem_url: "https://leetcode.cn/problems/1GxJYY/"
difficulty: "Medium"
created: "2022-11-03T23:13:29+08:00"
updated: "2022-11-03T23:13:29+08:00"
upvotes: 0
comments: 0
---

# LCP 68. 美观的花束

> **[yiduobo的每日leetcode LCP68.美观的花束](https://zhuanlan.zhihu.com/p/580213177) · 知乎 · 2022-11-03 · 赞同 0**
> 力扣：[LCP 68. 美观的花束](https://leetcode.cn/problems/1GxJYY/) · Medium · 灵茶山艾府：[不定长滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP68.美观的花束

[力扣](https://leetcode.cn/problems/1GxJYY/description/)

经典的边长滑动窗口的题目。使用一个哈希表cnt_dict记录当前窗口内每种花出现的次数，接下来从左向右一趟遍历，逐步将窗口的右边界向右移动。

当窗口右边界移动时，会有新的话加入到窗口中，因此需要更新这种花的出现的次数。若这个次数超过了cnt，此时就需要缩小窗口范围，将左边界跟着向右移动，直到这种花出现的次数不在大于cnt为止。

接下来，对于当前的窗口，以窗口中任意位置为起点，窗口右边界为终点的区间都是美观的区间，也就是说此时能带来数量等于窗口长度的美观区间，那么就应该使用窗口长度更新答案，然后重复上面的过程直到遍历完所有可能的区间右边界为止。

最后附上python代码：

```python
class Solution(object):
    def beautifulBouquet(self, flowers, cnt):
        """
        :type flowers: List[int]
        :type cnt: int
        :rtype: int
        """

        p = 0
        cnt_dict = {}
        cnt_dict[flowers[0]] = 1
        res = 1
        mod = 10 ** 9 + 7

        for index in range(1, len(flowers)):
            cnt_dict[flowers[index]] = cnt_dict.get(flowers[index], 0) + 1
            while cnt_dict[flowers[index]] > cnt:
                cnt_dict[flowers[p]] -= 1
                p += 1
            
            res += index - p + 1
            if res >= mod:
                res -= mod
        
        return res
```
