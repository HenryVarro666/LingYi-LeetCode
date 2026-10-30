---
title: "1010. 总持续时间内可被60整除的歌曲"
aliases: ["yiduobo的每日leetcode 1010.总持续时间内可被60整除的歌曲"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/array", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/367333274"
zhihu_id: "367333274"
zhihu_title: "yiduobo的每日leetcode 1010.总持续时间内可被60整除的歌曲"
question_id: "1010"
question: "总持续时间可被 60 整除的歌曲"
problem_url: "https://leetcode.cn/problems/pairs-of-songs-with-total-durations-divisible-by-60/"
difficulty: "Medium"
created: "2021-04-23T21:05:38+08:00"
updated: "2021-04-23T21:05:38+08:00"
upvotes: 0
comments: 0
---

# 1010. 总持续时间内可被60整除的歌曲

> **[yiduobo的每日leetcode 1010.总持续时间内可被60整除的歌曲](https://zhuanlan.zhihu.com/p/367333274) · 知乎 · 2021-04-23 · 赞同 0**
> 力扣：[1010. 总持续时间可被 60 整除的歌曲](https://leetcode.cn/problems/pairs-of-songs-with-total-durations-divisible-by-60/) · Medium · 灵茶山艾府：[「两数之和」的本质是什么？（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

1010.总持续时间内可被60整除的歌曲

[力扣](https://leetcode-cn.com/problems/pairs-of-songs-with-total-durations-divisible-by-60/)

对于歌曲j而言，设k \= time[j] % 60：

1、当k\=0时，需要找到满足time[i] % 60 \= 0的所有i

2、当k>0时，需要找到满足time[i] % 60 \= 60 - k的所有i

那么一个自然的想法就是使用一个dict来统计time[i] % 60的余数，然后从头到尾一趟遍历，求解匹配的i的数量，同时使用当前的余数更新dict即可

最后附上python代码：

```python
class Solution(object):
    def numPairsDivisibleBy60(self, time):
        """
        :type time: List[int]
        :rtype: int
        """

        rem_dict = {}
        res = 0
        for num in time:
            num %= 60
            if num > 0:
                res += rem_dict.get(60 - num, 0)
            else:
                res += rem_dict.get(num, 0)
                
            rem_dict[num] = rem_dict.get(num, 0) + 1
        
        return res
```
