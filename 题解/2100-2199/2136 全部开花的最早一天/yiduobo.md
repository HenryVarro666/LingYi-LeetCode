---
title: "2136. 全部开花的最早一天"
aliases: ["yiduobo的每日leetcode 2136.全部开花的最早一天"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/527768100"
zhihu_id: "527768100"
zhihu_title: "yiduobo的每日leetcode 2136.全部开花的最早一天"
question_id: "2136"
question: "全部开花的最早一天"
problem_url: "https://leetcode.cn/problems/earliest-possible-day-of-full-bloom/"
difficulty: "Hard"
rating: 2033
created: "2022-06-12T16:31:50+08:00"
updated: "2022-06-12T16:31:50+08:00"
upvotes: 0
comments: 0
---

# 2136. 全部开花的最早一天

> **[yiduobo的每日leetcode 2136.全部开花的最早一天](https://zhuanlan.zhihu.com/p/527768100) · 知乎 · 2022-06-12 · 赞同 0**
> 力扣：[2136. 全部开花的最早一天](https://leetcode.cn/problems/earliest-possible-day-of-full-bloom/) · Hard · 灵茶山艾府：[贪心及其证明（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2136.全部开花的最早一天

[力扣](https://leetcode.cn/problems/earliest-possible-day-of-full-bloom/)

首先可以明确的是，播种的行为必然不会穿插进行，证明也很简单。对于两个种子i和j，播种的总时间固定为plantTime[i] + plantTime[j]。

如果是按照先播种一个再播种另一个的方式来进行播种：如果先播种i，那么播种完成的时间就分别是plantTime[i]和plantTime[i] + plantTime[j]；如果先播种j，那么播种完成的时间就分别是plantTime[i] + plantTime[j]和plantTime[j]。

如果穿插进行，且i先完成播种，那么i完成的时间就是plantTime[i] + useTime[j]，j完成的时间依然是plantTime[i] + plantTime[j]；若果是j先完成播种，那么二者完成的时间则分别是plantTime[i] + plantTime[j]和useTime[i] + plantTime[j]。

可以发现，穿插播种显然是不优的。

接下来则需要考虑安排播种的顺序。一个直观的想法就是哪朵花开得慢就先播种哪朵花。这个思路是正确的，简单的证明如下：

如果按照当前播种的顺序，最晚开花的是开花时间排第k的花，那么：

1、若k \= 1，那么此时已经没有优化的余地的

2、若k > 1，那么为了让这朵花更快地开花，可以尝试将其播种的顺序往前挪。但是这样一来，前面1到k - 1中的某朵花就会被挤下来，成为第k朵播种的花。由于播种完成第k朵花的总时间不变，且前面挤下来的花的开花时间比当前这个第k多花的开花时间更长，那么这种调整反而会让最终的答案变大。换言之，当前这种按开花时间从大到小播种的做法就已经是最优了。

于是只需将所有花按开花时间从大到小排序，然后一趟遍历计算完成播种和最终开花时间并更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def earliestFullBloom(self, plantTime, growTime):
        """
        :type plantTime: List[int]
        :type growTime: List[int]
        :rtype: int
        """

        res = 0
        now = 0
        for p, g in sorted(zip(plantTime, growTime), key=lambda d:d[1], reverse=True):
            now += p
            res = max(res, now + g)
        
        return res
```
